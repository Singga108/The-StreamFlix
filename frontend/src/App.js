import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import ContentCarousel from "./components/ContentCarousel";
import Footer from "./components/Footer";
import ErrorBoundary from "./components/ErrorBoundary";
import { ContentLoader } from "./components/LoadingSpinner";
import { useMovies } from "./hooks/useMovies";

const Home = () => {
  const { 
    trendingMovies, 
    popularMovies, 
    hindiMovies,
    oldHindiMovies,
    trendingHindiMovies,
    punjabiMovies,
    oldPunjabiMovies,
    trendingPunjabiMovies,
    animeMovies,
    trendingSeries, 
    webSeries,
    sportsContent, 
    loading, 
    error, 
    refetch 
  } = useMovies();

  if (loading) {
    return (
      <div className="min-h-screen bg-black">
        <Navbar />
        <div className="pt-16">
          <ContentLoader message="Loading StreamFlix content..." />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black">
        <Navbar />
        <div className="pt-16">
          <ErrorBoundary onReset={refetch}>
            <div className="min-h-[400px] flex items-center justify-center">
              <div className="text-center">
                <p className="text-red-400 mb-4">{error}</p>
                <button 
                  onClick={refetch}
                  className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded"
                >
                  Try Again
                </button>
              </div>
            </div>
          </ErrorBoundary>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-black">
        <Navbar />
        
        {/* Hero Section */}
        <HeroSection />
        
        {/* Content Sections */}
        <div className="py-16 space-y-12">
          {trendingMovies.length > 0 && (
            <ContentCarousel 
              title="🔥 Trending Now" 
              items={trendingMovies} 
              type="movie"
            />
          )}
          
          {popularMovies.length > 0 && (
            <ContentCarousel 
              title="⭐ Popular Movies" 
              items={popularMovies} 
              type="movie"
            />
          )}

          {trendingHindiMovies.length > 0 && (
            <ContentCarousel 
              title="🇮🇳 Trending in Hindi" 
              items={trendingHindiMovies} 
              type="movie"
            />
          )}

          {hindiMovies.length > 0 && (
            <ContentCarousel 
              title="🎬 Hindi Movies" 
              items={hindiMovies} 
              type="movie"
            />
          )}

          {oldHindiMovies.length > 0 && (
            <ContentCarousel 
              title="📽️ Old Hindi Classics" 
              items={oldHindiMovies} 
              type="movie"
            />
          )}

          {trendingPunjabiMovies.length > 0 && (
            <ContentCarousel 
              title="🔥 Trending in Punjabi" 
              items={trendingPunjabiMovies} 
              type="movie"
            />
          )}

          {punjabiMovies.length > 0 && (
            <ContentCarousel 
              title="🎭 Punjabi Movies" 
              items={punjabiMovies} 
              type="movie"
            />
          )}

          {oldPunjabiMovies.length > 0 && (
            <ContentCarousel 
              title="🎪 Old Punjabi Classics" 
              items={oldPunjabiMovies} 
              type="movie"
            />
          )}

          {animeMovies.length > 0 && (
            <ContentCarousel 
              title="🎌 Anime Movies" 
              items={animeMovies} 
              type="movie"
            />
          )}

          {webSeries.length > 0 && (
            <ContentCarousel 
              title="📺 Web Series" 
              items={webSeries} 
              type="series"
            />
          )}
          
          {sportsContent.length > 0 && (
            <ContentCarousel 
              title="⚽ Live Sports & Highlights" 
              items={sportsContent} 
              type="sports"
            />
          )}
          
          {trendingSeries.length > 0 && (
            <ContentCarousel 
              title="📻 TV Series" 
              items={trendingSeries} 
              type="series"
            />
          )}
          
          {/* Show message if no content available */}
          {!trendingMovies.length && !popularMovies.length && !sportsContent.length && !trendingSeries.length && 
           !hindiMovies.length && !punjabiMovies.length && !animeMovies.length && !webSeries.length && (
            <div className="text-center py-20">
              <p className="text-gray-400 text-lg">No content available at the moment.</p>
              <p className="text-gray-500 mt-2">Please check back later.</p>
            </div>
          )}
        </div>
        
        <Footer />
      </div>
    </ErrorBoundary>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
