import { useState, useCallback } from 'react';
import { searchAPI } from '../services/api';

export const useSearch = () => {
  const [searchResults, setSearchResults] = useState({ movies: [], series: [], total: 0 });
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState(null);

  const search = useCallback(async (query, page = 1) => {
    if (!query.trim()) {
      setSearchResults({ movies: [], series: [], total: 0 });
      return;
    }

    try {
      setIsSearching(true);
      setSearchError(null);

      const response = await searchAPI.searchContent(query, page);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Search error:', error);
      setSearchError('Failed to search content. Please try again.');
      setSearchResults({ movies: [], series: [], total: 0 });
    } finally {
      setIsSearching(false);
    }
  }, []);

  const clearSearch = useCallback(() => {
    setSearchResults({ movies: [], series: [], total: 0 });
    setSearchError(null);
  }, []);

  return {
    searchResults,
    isSearching,
    searchError,
    search,
    clearSearch
  };
};