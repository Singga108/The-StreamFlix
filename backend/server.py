from fastapi import FastAPI, APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Optional, Annotated
from datetime import datetime

# Import our models and services
from models import (
    Movie, Series, Sports, User, UserCreate, UserLogin, UserResponse, 
    WatchlistAdd, WatchlistItem, SearchRequest, SearchResponse,
    MovieResponse, SeriesResponse, SportsResponse
)
from services.tmdb_service import TMDBService
from services.sports_service import SportsService
from services.auth_service import AuthService
from database import database

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Initialize services
TMDB_API_KEY = "c8dea14dc917687ac631a52620e4f7ad"  # Using provided TMDB key
tmdb_service = TMDBService(TMDB_API_KEY)
sports_service = SportsService()
auth_service = AuthService()

# Create the main app
app = FastAPI(title="StreamFlix API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        user_id = auth_service.get_current_user_id(token)
        if user_id:
            user = await database.get_user_by_id(user_id)
            return user
        return None
    except Exception:
        return None

# Optional auth dependency (doesn't raise error if no token)
async def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[User]:
    """Get current user from JWT token (optional)"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    try:
        token = authorization.split(" ")[1]
        user_id = auth_service.get_current_user_id(token)
        if user_id:
            user = await database.get_user_by_id(user_id)
            return user
        return None
    except Exception:
        return None

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "StreamFlix API is running", "version": "1.0.0"}

# Authentication routes
@api_router.post("/auth/register", response_model=dict)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await database.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = auth_service.hash_password(user_data.password)
        user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=hashed_password
        )
        
        # Save to database
        await database.create_user(user)
        
        # Create access token
        access_token = auth_service.create_access_token(user.id, user.email)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                watchlist=user.watchlist,
                created_at=user.created_at
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/auth/login", response_model=dict)
async def login_user(login_data: UserLogin):
    """Login user"""
    try:
        # Find user
        user = await database.get_user_by_email(login_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not auth_service.verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token = auth_service.create_access_token(user.id, user.email)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                watchlist=user.watchlist,
                created_at=user.created_at
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Movie routes
@api_router.get("/movies/trending", response_model=List[Movie])
async def get_trending_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get trending movies"""
    try:
        movies = await tmdb_service.get_trending_movies(page)
        # Save to database for future reference
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching trending movies: {str(e)}")
        # Fallback to database if API fails
        return await database.get_movies_by_category("trending", 20)

@api_router.get("/movies/popular", response_model=List[Movie])
async def get_popular_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get popular movies"""
    try:
        movies = await tmdb_service.get_popular_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching popular movies: {str(e)}")
        return await database.get_movies_by_category("popular", 20)

@api_router.get("/movies/hindi", response_model=List[Movie])
async def get_hindi_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get Hindi movies"""
    try:
        movies = await tmdb_service.get_hindi_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching Hindi movies: {str(e)}")
        return await database.get_movies_by_category("hindi", 20)

@api_router.get("/movies/hindi/old", response_model=List[Movie])
async def get_old_hindi_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get old Hindi movies"""
    try:
        movies = await tmdb_service.get_old_hindi_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching old Hindi movies: {str(e)}")
        return await database.get_movies_by_category("old_hindi", 20)

@api_router.get("/movies/hindi/trending", response_model=List[Movie])
async def get_trending_hindi_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get trending Hindi movies"""
    try:
        movies = await tmdb_service.get_trending_hindi_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching trending Hindi movies: {str(e)}")
        return await database.get_movies_by_category("trending_hindi", 20)

@api_router.get("/movies/punjabi", response_model=List[Movie])
async def get_punjabi_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get Punjabi movies"""
    try:
        movies = await tmdb_service.get_punjabi_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching Punjabi movies: {str(e)}")
        return await database.get_movies_by_category("punjabi", 20)

@api_router.get("/movies/punjabi/old", response_model=List[Movie])
async def get_old_punjabi_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get old Punjabi movies"""
    try:
        movies = await tmdb_service.get_old_punjabi_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching old Punjabi movies: {str(e)}")
        return await database.get_movies_by_category("old_punjabi", 20)

@api_router.get("/movies/punjabi/trending", response_model=List[Movie])
async def get_trending_punjabi_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get trending Punjabi movies"""
    try:
        movies = await tmdb_service.get_trending_punjabi_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching trending Punjabi movies: {str(e)}")
        return await database.get_movies_by_category("trending_punjabi", 20)

@api_router.get("/movies/anime", response_model=List[Movie])
async def get_anime_movies(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get anime movies"""
    try:
        movies = await tmdb_service.get_anime_movies(page)
        if movies:
            await database.save_movies(movies)
        return movies
    except Exception as e:
        logger.error(f"Error fetching anime movies: {str(e)}")
        return await database.get_movies_by_category("anime", 20)

@api_router.get("/movies/{movie_id}", response_model=Movie)
async def get_movie_details(movie_id: int, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get movie details"""
    try:
        movie = await tmdb_service.get_movie_details(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching movie details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Series routes
@api_router.get("/series/trending", response_model=List[Series])
async def get_trending_series(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get trending TV series"""
    try:
        series_list = await tmdb_service.get_trending_series(page)
        if series_list:
            await database.save_series(series_list)
        return series_list
    except Exception as e:
        logger.error(f"Error fetching trending series: {str(e)}")
        return await database.get_series_by_category("series", 20)

@api_router.get("/series/web", response_model=List[Series])
async def get_web_series(page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get popular web series"""
    try:
        series_list = await tmdb_service.get_web_series(page)
        if series_list:
            await database.save_series(series_list)
        return series_list
    except Exception as e:
        logger.error(f"Error fetching web series: {str(e)}")
        return await database.get_series_by_category("web_series", 20)

@api_router.get("/series/{series_id}", response_model=Series)
async def get_series_details(series_id: int, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get series details"""
    try:
        series = await tmdb_service.get_series_details(series_id)
        if not series:
            raise HTTPException(status_code=404, detail="Series not found")
        return series
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching series details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Sports routes
@api_router.get("/sports/live", response_model=List[Sports])
async def get_live_sports(current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get live sports events"""
    try:
        events = await sports_service.get_live_sports()
        await database.save_sports_events(events)
        return events
    except Exception as e:
        logger.error(f"Error fetching live sports: {str(e)}")
        return []

@api_router.get("/sports/highlights", response_model=List[Sports])
async def get_sports_highlights(current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get sports highlights"""
    try:
        events = await sports_service.get_highlights()
        await database.save_sports_events(events)
        return events
    except Exception as e:
        logger.error(f"Error fetching sports highlights: {str(e)}")
        return []

@api_router.get("/sports/upcoming", response_model=List[Sports])
async def get_upcoming_sports(current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get upcoming sports events"""
    try:
        events = await sports_service.get_upcoming_events()
        await database.save_sports_events(events)
        return events
    except Exception as e:
        logger.error(f"Error fetching upcoming sports: {str(e)}")
        return []

@api_router.get("/sports/all", response_model=List[Sports])
async def get_all_sports_content(current_user: Optional[User] = Depends(get_current_user_optional)):
    """Get all sports content (live + highlights + upcoming)"""
    try:
        events = await sports_service.get_all_sports_content()
        await database.save_sports_events(events)
        return events
    except Exception as e:
        logger.error(f"Error fetching all sports content: {str(e)}")
        return []

# Search routes
@api_router.get("/search", response_model=SearchResponse)
async def search_content(q: str, page: int = 1, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Search movies and TV shows"""
    try:
        # Search via TMDB API
        movies, series_list = await tmdb_service.search_content(q, page)
        
        # Also search local database
        db_movies = await database.search_movies(q, 10)
        db_series = await database.search_series(q, 10)
        
        # Combine results (remove duplicates by tmdb_id)
        all_movies = movies + [m for m in db_movies if m.tmdb_id not in [movie.tmdb_id for movie in movies]]
        all_series = series_list + [s for s in db_series if s.tmdb_id not in [series.tmdb_id for series in series_list]]
        
        return SearchResponse(
            movies=all_movies[:20],
            series=all_series[:20],
            total=len(all_movies) + len(all_series),
            page=page
        )
    except Exception as e:
        logger.error(f"Error searching content: {str(e)}")
        # Fallback to database search only
        db_movies = await database.search_movies(q, 10)
        db_series = await database.search_series(q, 10)
        
        return SearchResponse(
            movies=db_movies,
            series=db_series,
            total=len(db_movies) + len(db_series),
            page=page
        )

# Watchlist routes (require authentication)
@api_router.post("/user/watchlist", response_model=dict)
async def add_to_watchlist(watchlist_data: WatchlistAdd, current_user: User = Depends(get_current_user)):
    """Add item to user's watchlist"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        watchlist_item = WatchlistItem(
            user_id=current_user.id,
            content_id=watchlist_data.content_id,
            content_type=watchlist_data.content_type
        )
        
        await database.add_to_watchlist(watchlist_item)
        return {"message": "Added to watchlist successfully"}
    except Exception as e:
        logger.error(f"Error adding to watchlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/user/watchlist", response_model=List[WatchlistItem])
async def get_user_watchlist(current_user: User = Depends(get_current_user)):
    """Get user's watchlist"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        watchlist = await database.get_user_watchlist(current_user.id)
        return watchlist
    except Exception as e:
        logger.error(f"Error fetching watchlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/user/watchlist/{content_id}", response_model=dict)
async def remove_from_watchlist(content_id: str, current_user: User = Depends(get_current_user)):
    """Remove item from user's watchlist"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        removed = await database.remove_from_watchlist(current_user.id, content_id)
        if removed:
            return {"message": "Removed from watchlist successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found in watchlist")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from watchlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# User profile route
@api_router.get("/user/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get user profile"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        watchlist=current_user.watchlist,
        created_at=current_user.created_at
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection"""
    await database.connect()
    logger.info("StreamFlix API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection"""
    await database.disconnect()
    logger.info("StreamFlix API shutdown complete")
