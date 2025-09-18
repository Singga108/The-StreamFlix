import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import ContentCarousel from "./components/ContentCarousel";
import Footer from "./components/Footer";
import { mockMovies, mockSeries, mockSports, categories } from "./mockData";

const Home = () => {
  // Filter content by categories
  const trendingMovies = mockMovies.filter(movie => movie.category === 'trending');
  const popularMovies = mockMovies.filter(movie => movie.category === 'popular');
  const dramaContent = mockMovies.filter(movie => movie.category === 'drama');
  const allSeries = mockSeries;
  const sportsContent = mockSports;

  return (
    <div className="min-h-screen bg-black">
      <Navbar />
      
      {/* Hero Section */}
      <HeroSection />
      
      {/* Content Sections */}
      <div className="py-16 space-y-12">
        <ContentCarousel 
          title="Trending Now" 
          items={trendingMovies} 
          type="movie"
        />
        
        <ContentCarousel 
          title="Popular Movies" 
          items={popularMovies} 
          type="movie"
        />
        
        <ContentCarousel 
          title="Live Sports & Highlights" 
          items={sportsContent} 
          type="sports"
        />
        
        <ContentCarousel 
          title="TV Series" 
          items={allSeries} 
          type="series"
        />
        
        <ContentCarousel 
          title="Drama Collection" 
          items={dramaContent} 
          type="movie"
        />
      </div>
      
      <Footer />
    </div>
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
