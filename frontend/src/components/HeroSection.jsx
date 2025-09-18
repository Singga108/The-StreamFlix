import React from 'react';
import { Play, Plus, Info } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { heroContent } from '../mockData';

const HeroSection = () => {
  const { title, description, backgroundImage, rating, year, genre } = heroContent;

  return (
    <section className="relative h-screen flex items-center justify-start overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url(${backgroundImage})`,
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-black via-black/70 to-transparent"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-black/30"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16">
        <div className="max-w-2xl">
          {/* Meta Information */}
          <div className="flex items-center space-x-4 mb-6">
            <Badge variant="secondary" className="bg-red-600 hover:bg-red-700 text-white">
              Featured
            </Badge>
            <span className="text-gray-300 text-sm">{year}</span>
            <span className="text-gray-300 text-sm">•</span>
            <div className="flex items-center space-x-1">
              <span className="text-yellow-400">★</span>
              <span className="text-gray-300 text-sm">{rating}</span>
            </div>
            <span className="text-gray-300 text-sm">•</span>
            <span className="text-gray-300 text-sm">{genre}</span>
          </div>

          {/* Title */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
            {title}
          </h1>

          {/* Description */}
          <p className="text-lg sm:text-xl text-gray-300 mb-8 leading-relaxed max-w-xl">
            {description}
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Button 
              size="lg" 
              className="bg-white hover:bg-gray-200 text-black font-semibold px-8 py-3 rounded-md transition-all duration-200 hover:scale-105"
            >
              <Play className="w-5 h-5 mr-2 fill-current" />
              Play Now
            </Button>
            
            <Button 
              variant="outline" 
              size="lg"
              className="border-gray-400 bg-gray-900/70 hover:bg-gray-800/70 text-white px-8 py-3 rounded-md transition-all duration-200 hover:scale-105 backdrop-blur-sm"
            >
              <Plus className="w-5 h-5 mr-2" />
              My List
            </Button>
            
            <Button 
              variant="ghost" 
              size="lg"
              className="text-gray-300 hover:text-white hover:bg-gray-800/50 px-8 py-3 rounded-md transition-all duration-200"
            >
              <Info className="w-5 h-5 mr-2" />
              More Info
            </Button>
          </div>
        </div>
      </div>

      {/* Bottom Fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black to-transparent"></div>
    </section>
  );
};

export default HeroSection;