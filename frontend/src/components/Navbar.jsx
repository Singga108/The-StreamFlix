import React, { useState, useEffect } from 'react';
import { Search, Menu, X, User, Bell } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useSearch } from '../hooks/useSearch';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearchResults, setShowSearchResults] = useState(false);
  const { searchResults, isSearching, search, clearSearch } = useSearch();

  const navItems = ['Home', 'Movies', 'TV Shows', 'Sports', 'My List'];

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery.trim()) {
        search(searchQuery);
        setShowSearchResults(true);
      } else {
        clearSearch();
        setShowSearchResults(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery, search, clearSearch]);

  const handleSearchInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchItemClick = (item) => {
    console.log(`Selected: ${item.title}`);
    setShowSearchResults(false);
    setSearchQuery('');
    // Here you would navigate to the item details page
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/90 backdrop-blur-sm border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold text-red-500">StreamFlix</h1>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              {navItems.map((item) => (
                <a
                  key={item}
                  href={`#${item.toLowerCase().replace(' ', '-')}`}
                  className="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium transition-colors duration-200 hover:bg-gray-800 rounded-md"
                >
                  {item}
                </a>
              ))}
            </div>
          </div>

          {/* Search and User Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Search movies, shows..."
                value={searchQuery}
                onChange={handleSearchInputChange}
                className="pl-10 w-64 bg-gray-900/50 border-gray-700 text-white placeholder-gray-400 focus:border-red-500"
              />
              
              {/* Search Results Dropdown */}
              {showSearchResults && (searchResults.movies.length > 0 || searchResults.series.length > 0 || isSearching) && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-gray-900 border border-gray-700 rounded-md shadow-xl max-h-96 overflow-y-auto z-50">
                  {isSearching ? (
                    <div className="p-4 text-center text-gray-400">Searching...</div>
                  ) : (
                    <>
                      {searchResults.movies.length > 0 && (
                        <div>
                          <div className="px-4 py-2 text-sm font-semibold text-gray-300 bg-gray-800">Movies</div>
                          {searchResults.movies.slice(0, 3).map((movie) => (
                            <button
                              key={movie.id}
                              onClick={() => handleSearchItemClick(movie)}
                              className="w-full px-4 py-2 text-left hover:bg-gray-800 flex items-center space-x-3"
                            >
                              <img
                                src={movie.thumbnail}
                                alt={movie.title}
                                className="w-10 h-14 object-cover rounded"
                              />
                              <div>
                                <p className="text-white text-sm">{movie.title}</p>
                                <p className="text-gray-400 text-xs">{movie.year}</p>
                              </div>
                            </button>
                          ))}
                        </div>
                      )}
                      
                      {searchResults.series.length > 0 && (
                        <div>
                          <div className="px-4 py-2 text-sm font-semibold text-gray-300 bg-gray-800">TV Series</div>
                          {searchResults.series.slice(0, 3).map((series) => (
                            <button
                              key={series.id}
                              onClick={() => handleSearchItemClick(series)}
                              className="w-full px-4 py-2 text-left hover:bg-gray-800 flex items-center space-x-3"
                            >
                              <img
                                src={series.thumbnail}
                                alt={series.title}
                                className="w-10 h-14 object-cover rounded"
                              />
                              <div>
                                <p className="text-white text-sm">{series.title}</p>
                                <p className="text-gray-400 text-xs">{series.year}</p>
                              </div>
                            </button>
                          ))}
                        </div>
                      )}
                      
                      {searchResults.movies.length === 0 && searchResults.series.length === 0 && searchQuery && (
                        <div className="p-4 text-center text-gray-400">No results found</div>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
            <Button variant="ghost" size="sm" className="text-gray-300 hover:text-white">
              <Bell className="w-5 h-5" />
            </Button>
            <Button variant="ghost" size="sm" className="text-gray-300 hover:text-white">
              <User className="w-5 h-5" />
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-300 hover:text-white"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-900/95 rounded-lg mt-2">
              {navItems.map((item) => (
                <a
                  key={item}
                  href={`#${item.toLowerCase().replace(' ', '-')}`}
                  className="text-gray-300 hover:text-white block px-3 py-2 text-base font-medium transition-colors duration-200 hover:bg-gray-800 rounded-md"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item}
                </a>
              ))}
              <div className="mt-4 pt-4 border-t border-gray-700">
                <div className="relative mb-3">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={handleSearchInputChange}
                    className="pl-10 w-full bg-gray-800 border-gray-600 text-white placeholder-gray-400"
                  />
                </div>
                <div className="flex space-x-2">
                  <Button variant="ghost" size="sm" className="text-gray-300 hover:text-white flex-1">
                    <Bell className="w-4 h-4 mr-2" />
                    Notifications
                  </Button>
                  <Button variant="ghost" size="sm" className="text-gray-300 hover:text-white flex-1">
                    <User className="w-4 h-4 mr-2" />
                    Profile
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;