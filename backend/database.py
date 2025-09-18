from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional, List, Dict, Any
import os
import logging
from .models import User, Movie, Series, Sports, WatchlistItem

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.users: Optional[AsyncIOMotorCollection] = None
        self.movies: Optional[AsyncIOMotorCollection] = None
        self.series: Optional[AsyncIOMotorCollection] = None
        self.sports: Optional[AsyncIOMotorCollection] = None
        self.watchlist: Optional[AsyncIOMotorCollection] = None
    
    async def connect(self):
        """Connect to MongoDB"""
        mongo_url = os.environ['MONGO_URL']
        db_name = os.environ['DB_NAME']
        
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        
        # Initialize collections
        self.users = self.db.users
        self.movies = self.db.movies
        self.series = self.db.series
        self.sports = self.db.sports
        self.watchlist = self.db.watchlist
        
        logger.info("Connected to MongoDB")
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    # User operations
    async def create_user(self, user: User) -> User:
        """Create a new user"""
        user_dict = user.dict()
        await self.users.insert_one(user_dict)
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_doc = await self.users.find_one({"email": email})
        if user_doc:
            return User(**user_doc)
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        user_doc = await self.users.find_one({"id": user_id})
        if user_doc:
            return User(**user_doc)
        return None
    
    # Movies operations
    async def save_movies(self, movies: List[Movie]) -> List[Movie]:
        """Save movies to database (upsert based on tmdb_id)"""
        for movie in movies:
            movie_dict = movie.dict()
            if movie.tmdb_id:
                # Update existing or insert new
                await self.movies.update_one(
                    {"tmdb_id": movie.tmdb_id},
                    {"$set": movie_dict},
                    upsert=True
                )
            else:
                await self.movies.insert_one(movie_dict)
        
        return movies
    
    async def get_movies_by_category(self, category: str, limit: int = 20) -> List[Movie]:
        """Get movies by category"""
        cursor = self.movies.find({"categories": category}).limit(limit)
        movies = []
        
        async for movie_doc in cursor:
            movies.append(Movie(**movie_doc))
        
        return movies
    
    # Series operations
    async def save_series(self, series_list: List[Series]) -> List[Series]:
        """Save series to database (upsert based on tmdb_id)"""
        for series in series_list:
            series_dict = series.dict()
            if series.tmdb_id:
                await self.series.update_one(
                    {"tmdb_id": series.tmdb_id},
                    {"$set": series_dict},
                    upsert=True
                )
            else:
                await self.series.insert_one(series_dict)
        
        return series_list
    
    async def get_series_by_category(self, category: str, limit: int = 20) -> List[Series]:
        """Get series by category"""
        cursor = self.series.find({"categories": category}).limit(limit)
        series_list = []
        
        async for series_doc in cursor:
            series_list.append(Series(**series_doc))
        
        return series_list
    
    # Sports operations
    async def save_sports_events(self, events: List[Sports]) -> List[Sports]:
        """Save sports events to database"""
        for event in events:
            event_dict = event.dict()
            await self.sports.update_one(
                {"title": event.title, "start_time": event.start_time},
                {"$set": event_dict},
                upsert=True
            )
        
        return events
    
    async def get_sports_by_status(self, status: str, limit: int = 20) -> List[Sports]:
        """Get sports events by status"""
        cursor = self.sports.find({"status": status}).limit(limit)
        events = []
        
        async for event_doc in cursor:
            events.append(Sports(**event_doc))
        
        return events
    
    # Watchlist operations
    async def add_to_watchlist(self, watchlist_item: WatchlistItem) -> WatchlistItem:
        """Add item to user's watchlist"""
        # Check if already exists
        existing = await self.watchlist.find_one({
            "user_id": watchlist_item.user_id,
            "content_id": watchlist_item.content_id
        })
        
        if not existing:
            item_dict = watchlist_item.dict()
            await self.watchlist.insert_one(item_dict)
        
        return watchlist_item
    
    async def remove_from_watchlist(self, user_id: str, content_id: str) -> bool:
        """Remove item from user's watchlist"""
        result = await self.watchlist.delete_one({
            "user_id": user_id,
            "content_id": content_id
        })
        
        return result.deleted_count > 0
    
    async def get_user_watchlist(self, user_id: str) -> List[WatchlistItem]:
        """Get user's watchlist"""
        cursor = self.watchlist.find({"user_id": user_id})
        watchlist = []
        
        async for item_doc in cursor:
            watchlist.append(WatchlistItem(**item_doc))
        
        return watchlist
    
    # Search operations
    async def search_movies(self, query: str, limit: int = 20) -> List[Movie]:
        """Search movies by title"""
        cursor = self.movies.find({
            "title": {"$regex": query, "$options": "i"}
        }).limit(limit)
        
        movies = []
        async for movie_doc in cursor:
            movies.append(Movie(**movie_doc))
        
        return movies
    
    async def search_series(self, query: str, limit: int = 20) -> List[Series]:
        """Search series by title"""
        cursor = self.series.find({
            "title": {"$regex": query, "$options": "i"}
        }).limit(limit)
        
        series_list = []
        async for series_doc in cursor:
            series_list.append(Series(**series_doc))
        
        return series_list

# Global database instance
database = Database()