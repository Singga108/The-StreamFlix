import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Movie, Series

logger = logging.getLogger(__name__)

class TMDBService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        self.backdrop_base_url = "https://image.tmdb.org/t/p/w1280"
        
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to TMDB API"""
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"TMDB API error: {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"TMDB request failed: {str(e)}")
            return {}
    
    def _transform_movie(self, tmdb_movie: Dict[str, Any]) -> Movie:
        """Transform TMDB movie data to our Movie model"""
        genres = [genre['name'] for genre in tmdb_movie.get('genres', [])]
        if not genres:
            # If detailed genres not available, use genre_ids mapping
            genre_mapping = {
                28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
                80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
                14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
                9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
                10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
            }
            genres = [genre_mapping.get(gid, "Unknown") for gid in tmdb_movie.get('genre_ids', [])]
        
        thumbnail = f"{self.image_base_url}{tmdb_movie.get('poster_path', '')}" if tmdb_movie.get('poster_path') else ""
        backdrop = f"{self.backdrop_base_url}{tmdb_movie.get('backdrop_path', '')}" if tmdb_movie.get('backdrop_path') else ""
        
        return Movie(
            tmdb_id=tmdb_movie.get('id'),
            title=tmdb_movie.get('title', 'Unknown Title'),
            description=tmdb_movie.get('overview', 'No description available'),
            genre=genres,
            rating=tmdb_movie.get('vote_average', 0.0),
            year=int(tmdb_movie.get('release_date', '2023-01-01')[:4]) if tmdb_movie.get('release_date') else 2023,
            thumbnail=thumbnail,
            backdrop_image=backdrop,
            categories=["popular"],
            duration=f"{tmdb_movie.get('runtime', 120)} min" if tmdb_movie.get('runtime') else "120 min",
            popularity=tmdb_movie.get('popularity', 0.0)
        )
    
    def _transform_series(self, tmdb_series: Dict[str, Any]) -> Series:
        """Transform TMDB series data to our Series model"""
        genres = [genre['name'] for genre in tmdb_series.get('genres', [])]
        if not genres:
            genre_mapping = {
                10759: "Action & Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
                99: "Documentary", 18: "Drama", 10751: "Family", 10762: "Kids",
                9648: "Mystery", 10763: "News", 10764: "Reality", 10765: "Sci-Fi & Fantasy",
                10766: "Soap", 10767: "Talk", 10768: "War & Politics", 37: "Western"
            }
            genres = [genre_mapping.get(gid, "Unknown") for gid in tmdb_series.get('genre_ids', [])]
        
        thumbnail = f"{self.image_base_url}{tmdb_series.get('poster_path', '')}" if tmdb_series.get('poster_path') else ""
        backdrop = f"{self.backdrop_base_url}{tmdb_series.get('backdrop_path', '')}" if tmdb_series.get('backdrop_path') else ""
        
        return Series(
            tmdb_id=tmdb_series.get('id'),
            title=tmdb_series.get('name', 'Unknown Title'),
            description=tmdb_series.get('overview', 'No description available'),
            genre=genres,
            rating=tmdb_series.get('vote_average', 0.0),
            year=int(tmdb_series.get('first_air_date', '2023-01-01')[:4]) if tmdb_series.get('first_air_date') else 2023,
            thumbnail=thumbnail,
            backdrop_image=backdrop,
            categories=["series"],
            seasons=tmdb_series.get('number_of_seasons', 1),
            episodes=tmdb_series.get('number_of_episodes', 10)
        )
    
    async def get_trending_movies(self, page: int = 1) -> List[Movie]:
        """Get trending movies"""
        data = await self._make_request(f"trending/movie/week", {"page": page})
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["trending"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming movie: {str(e)}")
                continue
                
        return movies
    
    async def get_popular_movies(self, page: int = 1) -> List[Movie]:
        """Get popular movies"""
        data = await self._make_request(f"movie/popular", {"page": page})
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["popular"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming movie: {str(e)}")
                continue
                
        return movies
    
    async def get_trending_series(self, page: int = 1) -> List[Series]:
        """Get trending TV series"""
        data = await self._make_request(f"trending/tv/week", {"page": page})
        series_list = []
        
        for series_data in data.get('results', []):
            try:
                series = self._transform_series(series_data)
                series.categories = ["series"]
                series_list.append(series)
            except Exception as e:
                logger.error(f"Error transforming series: {str(e)}")
                continue
                
        return series_list
    
    async def search_content(self, query: str, page: int = 1) -> tuple[List[Movie], List[Series]]:
        """Search movies and TV shows"""
        # Search movies
        movies_data = await self._make_request("search/movie", {"query": query, "page": page})
        movies = []
        
        for movie_data in movies_data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming search movie: {str(e)}")
                continue
        
        # Search TV shows
        series_data = await self._make_request("search/tv", {"query": query, "page": page})
        series_list = []
        
        for series_data_item in series_data.get('results', []):
            try:
                series = self._transform_series(series_data_item)
                series_list.append(series)
            except Exception as e:
                logger.error(f"Error transforming search series: {str(e)}")
                continue
        
        return movies, series_list
    
    async def get_movie_details(self, movie_id: int) -> Optional[Movie]:
        """Get detailed movie information"""
        data = await self._make_request(f"movie/{movie_id}")
        
        if not data:
            return None
            
        try:
            return self._transform_movie(data)
        except Exception as e:
            logger.error(f"Error transforming movie details: {str(e)}")
            return None
    
    async def get_hindi_movies(self, page: int = 1) -> List[Movie]:
        """Get Hindi movies"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_original_language": "hi",
            "sort_by": "popularity.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["hindi"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming Hindi movie: {str(e)}")
                continue
                
        return movies
    
    async def get_old_hindi_movies(self, page: int = 1) -> List[Movie]:
        """Get old Hindi movies (before 2000)"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_original_language": "hi",
            "primary_release_date.lte": "2000-12-31",
            "sort_by": "popularity.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["old_hindi"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming old Hindi movie: {str(e)}")
                continue
                
        return movies
    
    async def get_trending_hindi_movies(self, page: int = 1) -> List[Movie]:
        """Get trending Hindi movies"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_original_language": "hi",
            "primary_release_date.gte": "2020-01-01",
            "sort_by": "vote_average.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["trending_hindi"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming trending Hindi movie: {str(e)}")
                continue
                
        return movies
    
    async def get_punjabi_movies(self, page: int = 1) -> List[Movie]:
        """Get Punjabi movies"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_original_language": "pa",
            "sort_by": "popularity.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["punjabi"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming Punjabi movie: {str(e)}")
                continue
        
        # If no results from TMDB, add some mock Punjabi movies
        if not movies:
            movies = self._get_mock_punjabi_movies()
                
        return movies
    
    async def get_old_punjabi_movies(self, page: int = 1) -> List[Movie]:
        """Get old Punjabi movies"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_original_language": "pa",
            "primary_release_date.lte": "2010-12-31",
            "sort_by": "popularity.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["old_punjabi"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming old Punjabi movie: {str(e)}")
                continue
        
        # Fallback to mock data if no results
        if not movies:
            movies = self._get_mock_old_punjabi_movies()
                
        return movies
    
    async def get_trending_punjabi_movies(self, page: int = 1) -> List[Movie]:
        """Get trending Punjabi movies"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_original_language": "pa",
            "primary_release_date.gte": "2018-01-01",
            "sort_by": "vote_average.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["trending_punjabi"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming trending Punjabi movie: {str(e)}")
                continue
        
        # Fallback to mock data if no results
        if not movies:
            movies = self._get_mock_trending_punjabi_movies()
                
        return movies
    
    async def get_anime_movies(self, page: int = 1) -> List[Movie]:
        """Get anime movies"""
        data = await self._make_request("discover/movie", {
            "page": page,
            "with_genres": "16",  # Animation genre
            "with_origin_country": "JP",
            "sort_by": "popularity.desc"
        })
        movies = []
        
        for movie_data in data.get('results', []):
            try:
                movie = self._transform_movie(movie_data)
                movie.categories = ["anime"]
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error transforming anime movie: {str(e)}")
                continue
                
        return movies
    
    async def get_web_series(self, page: int = 1) -> List[Series]:
        """Get popular web series"""
        data = await self._make_request("discover/tv", {
            "page": page,
            "sort_by": "popularity.desc",
            "vote_average.gte": 7.0
        })
        series_list = []
        
        for series_data in data.get('results', []):
            try:
                series = self._transform_series(series_data)
                series.categories = ["web_series"]
                series_list.append(series)
            except Exception as e:
                logger.error(f"Error transforming web series: {str(e)}")
                continue
                
        return series_list
    
    def _get_mock_punjabi_movies(self) -> List[Movie]:
        """Mock Punjabi movies data"""
        mock_data = [
            {
                "title": "Chal Mera Putt",
                "description": "A comedy-drama about Punjabi immigrants living in the UK and their struggles and friendships.",
                "year": 2019,
                "rating": 8.2,
                "genre": ["Comedy", "Drama"],
                "thumbnail": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=300&h=400&fit=crop&sat=1.2&hue=30",
                "backdrop_image": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=1280&h=720&fit=crop&sat=1.2&hue=30",
                "duration": "132 min"
            },
            {
                "title": "Qismat",
                "description": "A romantic drama about love, destiny, and the choices that shape our lives.",
                "year": 2018,
                "rating": 8.5,
                "genre": ["Romance", "Drama"],
                "thumbnail": "https://images.unsplash.com/photo-1572188863110-46d457c9234d?w=300&h=400&fit=crop&sat=1.3&hue=350",
                "backdrop_image": "https://images.unsplash.com/photo-1572188863110-46d457c9234d?w=1280&h=720&fit=crop&sat=1.3&hue=350",
                "duration": "141 min"
            },
            {
                "title": "Shadaa",
                "description": "A comedy about a man in his 30s who is still unmarried and the pressures he faces from family.",
                "year": 2019,
                "rating": 7.8,
                "genre": ["Comedy", "Romance"],
                "thumbnail": "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=300&h=400&fit=crop&sat=1.1&hue=60",
                "backdrop_image": "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=1280&h=720&fit=crop&sat=1.1&hue=60",
                "duration": "127 min"
            }
        ]
        
        movies = []
        for data in mock_data:
            movie = Movie(
                title=data["title"],
                description=data["description"],
                genre=data["genre"],
                rating=data["rating"],
                year=data["year"],
                thumbnail=data["thumbnail"],
                backdrop_image=data["backdrop_image"],
                categories=["punjabi"],
                duration=data["duration"]
            )
            movies.append(movie)
        
        return movies
    
    def _get_mock_old_punjabi_movies(self) -> List[Movie]:
        """Mock old Punjabi movies data"""
        mock_data = [
            {
                "title": "Maula Jatt",
                "description": "Classic Punjabi action film about a legendary warrior and his battles.",
                "year": 1979,
                "rating": 8.0,
                "genre": ["Action", "Drama"],
                "thumbnail": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=300&h=400&fit=crop&sat=0.8&contrast=1.2",
                "backdrop_image": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=1280&h=720&fit=crop&sat=0.8&contrast=1.2",
                "duration": "135 min"
            },
            {
                "title": "Putt Jattan De",
                "description": "A classic family drama showcasing Punjabi culture and traditions.",
                "year": 1982,
                "rating": 7.5,
                "genre": ["Drama", "Family"],
                "thumbnail": "https://images.unsplash.com/photo-1572188863110-46d457c9234d?w=300&h=400&fit=crop&sat=0.7&sepia=0.3",
                "backdrop_image": "https://images.unsplash.com/photo-1572188863110-46d457c9234d?w=1280&h=720&fit=crop&sat=0.7&sepia=0.3",
                "duration": "142 min"
            }
        ]
        
        movies = []
        for data in mock_data:
            movie = Movie(
                title=data["title"],
                description=data["description"],
                genre=data["genre"],
                rating=data["rating"],
                year=data["year"],
                thumbnail=data["thumbnail"],
                backdrop_image=data["backdrop_image"],
                categories=["old_punjabi"],
                duration=data["duration"]
            )
            movies.append(movie)
        
        return movies
    
    def _get_mock_trending_punjabi_movies(self) -> List[Movie]:
        """Mock trending Punjabi movies data"""
        mock_data = [
            {
                "title": "Honsla Rakh",
                "description": "A modern comedy-drama starring Diljit Dosanjh about single parenthood and love.",
                "year": 2021,
                "rating": 8.1,
                "genre": ["Comedy", "Romance"],
                "thumbnail": "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=300&h=400&fit=crop&brightness=1.1&hue=45",
                "backdrop_image": "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=1280&h=720&fit=crop&brightness=1.1&hue=45",
                "duration": "145 min"
            },
            {
                "title": "Sufna",
                "description": "A romantic drama about dreams, aspirations, and the journey of love.",
                "year": 2020,
                "rating": 8.3,
                "genre": ["Romance", "Drama"],
                "thumbnail": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=300&h=400&fit=crop&hue=320&sat=1.2",
                "backdrop_image": "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=1280&h=720&fit=crop&hue=320&sat=1.2",
                "duration": "130 min"
            }
        ]
        
        movies = []
        for data in mock_data:
            movie = Movie(
                title=data["title"],
                description=data["description"],
                genre=data["genre"],
                rating=data["rating"],
                year=data["year"],
                thumbnail=data["thumbnail"],
                backdrop_image=data["backdrop_image"],
                categories=["trending_punjabi"],
                duration=data["duration"]
            )
            movies.append(movie)
        
        return movies