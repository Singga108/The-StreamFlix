import React, { useState, useRef } from 'react';
import { ChevronLeft, ChevronRight, Play, Plus, Star } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';

const ContentCarousel = ({ title, items, type = 'movie' }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [hoveredItem, setHoveredItem] = useState(null);
  const scrollContainerRef = useRef(null);

  const itemsPerView = 5;
  const maxIndex = Math.max(0, items.length - itemsPerView);

  const scrollLeft = () => {
    setCurrentIndex(Math.max(0, currentIndex - 1));
  };

  const scrollRight = () => {
    setCurrentIndex(Math.min(maxIndex, currentIndex + 1));
  };

  const handleItemClick = (item) => {
    console.log(`Playing: ${item.title}`);
    // Here you would implement the actual play functionality
  };

  return (
    <section className="mb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Title */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl sm:text-3xl font-bold text-white">{title}</h2>
          <div className="flex space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={scrollLeft}
              disabled={currentIndex === 0}
              className="border-gray-600 bg-gray-800/50 hover:bg-gray-700 text-white disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={scrollRight}
              disabled={currentIndex >= maxIndex}
              className="border-gray-600 bg-gray-800/50 hover:bg-gray-700 text-white disabled:opacity-50"
            >
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Carousel Container */}
        <div className="relative overflow-hidden">
          <div 
            ref={scrollContainerRef}
            className="flex transition-transform duration-300 ease-out"
            style={{
              transform: `translateX(-${currentIndex * (100 / itemsPerView)}%)`
            }}
          >
            {items.map((item, index) => (
              <div
                key={item.id}
                className="flex-none w-1/5 px-2"
                onMouseEnter={() => setHoveredItem(item.id)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                <Card className={`bg-gray-900 border-gray-700 overflow-hidden transition-all duration-300 cursor-pointer ${
                  hoveredItem === item.id ? 'transform scale-105 shadow-2xl shadow-red-500/20' : ''
                }`}>
                  <div className="relative">
                    <img
                      src={item.thumbnail}
                      alt={item.title}
                      className="w-full h-48 object-cover"
                      loading="lazy"
                    />
                    
                    {/* Overlay on Hover */}
                    {hoveredItem === item.id && (
                      <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
                        <div className="flex space-x-2">
                          <Button 
                            size="sm" 
                            onClick={() => handleItemClick(item)}
                            className="bg-white hover:bg-gray-200 text-black"
                          >
                            <Play className="w-4 h-4 mr-1 fill-current" />
                            Play
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            className="border-gray-400 bg-gray-800/50 hover:bg-gray-700 text-white"
                          >
                            <Plus className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    )}

                    {/* Status Badge for Sports */}
                    {type === 'sports' && item.status && (
                      <Badge 
                        className={`absolute top-2 left-2 ${
                          item.status === 'Live' 
                            ? 'bg-red-600 hover:bg-red-700' 
                            : item.status === 'Upcoming'
                            ? 'bg-blue-600 hover:bg-blue-700'
                            : 'bg-gray-600 hover:bg-gray-700'
                        } text-white`}
                      >
                        {item.status}
                      </Badge>
                    )}
                  </div>

                  <CardContent className="p-4">
                    <h3 className="font-semibold text-white mb-2 truncate">{item.title}</h3>
                    
                    {type === 'sports' ? (
                      <div className="space-y-1">
                        <p className="text-sm text-gray-400">{item.sport}</p>
                        <p className="text-xs text-gray-500">{item.time}</p>
                        <p className="text-xs text-gray-500">{item.venue}</p>
                      </div>
                    ) : (
                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-400">{item.year}</span>
                          <div className="flex items-center space-x-1">
                            <Star className="w-3 h-3 text-yellow-400 fill-current" />
                            <span className="text-sm text-gray-400">{item.rating}</span>
                          </div>
                        </div>
                        <p className="text-sm text-gray-400">{item.genre}</p>
                        <p className="text-xs text-gray-500">{item.duration}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContentCarousel;