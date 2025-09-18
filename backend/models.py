from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# User Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    password_hash: str
    watchlist: List[str] = Field(default_factory=list)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    watchlist: List[str]
    created_at: datetime

# Content Models
class Movie(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tmdb_id: Optional[int] = None
    title: str
    description: str
    genre: List[str]
    rating: float
    year: int
    thumbnail: str
    backdrop_image: str
    trailer_url: Optional[str] = None
    categories: List[str]
    duration: Optional[str] = None
    popularity: Optional[float] = None

class Series(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tmdb_id: Optional[int] = None
    title: str
    description: str
    genre: List[str]
    rating: float
    year: int
    thumbnail: str
    backdrop_image: str
    trailer_url: Optional[str] = None
    categories: List[str]
    seasons: Optional[int] = None
    episodes: Optional[int] = None

class Sports(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    sport: str
    status: str  # Live, Highlights, Upcoming
    teams: List[str] = Field(default_factory=list)
    venue: Optional[str] = None
    start_time: Optional[datetime] = None
    image: str
    description: Optional[str] = None

# Response Models
class MovieResponse(BaseModel):
    movies: List[Movie]
    total: int
    page: int

class SeriesResponse(BaseModel):
    series: List[Series]
    total: int
    page: int

class SportsResponse(BaseModel):
    events: List[Sports]
    total: int

# Watchlist Models
class WatchlistItem(BaseModel):
    user_id: str
    content_id: str
    content_type: str  # movie, series, sports
    added_at: datetime = Field(default_factory=datetime.utcnow)

class WatchlistAdd(BaseModel):
    content_id: str
    content_type: str

# Search Models
class SearchRequest(BaseModel):
    query: str
    page: Optional[int] = 1
    limit: Optional[int] = 20

class SearchResponse(BaseModel):
    movies: List[Movie]
    series: List[Series]
    total: int
    page: int