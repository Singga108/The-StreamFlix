# StreamFlix Backend Development Contract

## 🎯 Project Overview
Transform StreamFlix from a frontend prototype with mock data to a fully functional entertainment streaming platform with real movie/sports data integration.

## 📡 API Contracts

### Backend Endpoints to Implement

#### 1. Movies & TV Shows
- `GET /api/movies/trending` - Get trending movies
- `GET /api/movies/popular` - Get popular movies  
- `GET /api/movies/search?q={query}` - Search movies/shows
- `GET /api/movies/{id}` - Get movie details
- `GET /api/series/trending` - Get trending TV series
- `GET /api/series/{id}` - Get series details

#### 2. Sports Content
- `GET /api/sports/live` - Get live sports events
- `GET /api/sports/highlights` - Get sports highlights
- `GET /api/sports/upcoming` - Get upcoming matches

#### 3. User Management
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/user/profile` - Get user profile
- `POST /api/user/watchlist` - Add to watchlist
- `GET /api/user/watchlist` - Get user's watchlist

## 🔄 Mock Data Replacement Plan

### Current Mock Data in `mockData.js`:
1. **mockMovies** → Replace with TMDB API data
2. **mockSeries** → Replace with TMDB API series data  
3. **mockSports** → Replace with sports API data
4. **heroContent** → Dynamic featured content selection

### Frontend Integration Changes:
1. Replace static imports from `mockData.js`
2. Add API calls using axios to backend endpoints
3. Implement loading states and error handling
4. Add pagination for carousels

## 🛠 Backend Implementation Plan

### Phase 1: Core Infrastructure
- MongoDB models for Users, Movies, Sports, Watchlists
- TMDB API integration service
- Basic CRUD operations
- Error handling middleware

### Phase 2: External API Integration
- **TMDB API**: Movie and TV show data
- **Sports API**: Live scores and match data
- Data caching strategy for performance
- Image URL transformation and CDN optimization

### Phase 3: User Features
- JWT authentication system
- User registration and login
- Personal watchlist management
- User preferences and recommendations

### Phase 4: Advanced Features
- Search functionality with filters
- Content recommendations algorithm
- User rating and review system
- Recently watched tracking

## 🔌 Frontend & Backend Integration

### API Configuration:
- Use existing `REACT_APP_BACKEND_URL` environment variable
- All API calls prefixed with `/api` for proper routing
- Implement axios interceptors for auth tokens
- Add loading spinners and error boundaries

### State Management:
- Replace mock data imports with API calls
- Implement React hooks for data fetching
- Add caching for frequently accessed data
- Handle loading and error states gracefully

## 📊 Database Schema

### Users Collection:
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hashed),
  name: String,
  watchlist: [ObjectId],
  preferences: Object,
  createdAt: Date
}
```

### Movies Collection:
```javascript
{
  _id: ObjectId,
  tmdbId: Number,
  title: String,
  description: String,
  genre: [String],
  rating: Number,
  year: Number,
  thumbnail: String,
  backdropImage: String,
  trailerUrl: String,
  categories: [String]
}
```

### Sports Collection:
```javascript
{
  _id: ObjectId,
  title: String,
  sport: String,
  status: String, // Live, Highlights, Upcoming
  teams: [String],
  venue: String,
  startTime: Date,
  image: String
}
```

## 🎯 Success Criteria

### Functional Requirements:
- ✅ Real movie/TV data from TMDB API
- ✅ Live sports content integration
- ✅ User authentication and profiles
- ✅ Working search functionality
- ✅ Personal watchlist management

### Technical Requirements:
- ✅ Seamless frontend-backend integration
- ✅ Responsive performance with real data
- ✅ Error handling and loading states
- ✅ Secure authentication system
- ✅ Scalable database design

## 📝 Notes
- All video content will link to YouTube trailers initially
- Sports "live" content will show highlights/replays
- Free platform model - no payment integration needed
- Focus on smooth user experience and fast loading times