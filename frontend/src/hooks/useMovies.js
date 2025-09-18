import { useState, useEffect } from 'react';
import { moviesAPI, seriesAPI, sportsAPI } from '../services/api';

export const useMovies = () => {
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [trendingSeries, setTrendingSeries] = useState([]);
  const [sportsContent, setSportsContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchContent = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all content in parallel
      const [
        trendingMoviesRes,
        popularMoviesRes, 
        trendingSeriesRes,
        sportsRes
      ] = await Promise.allSettled([
        moviesAPI.getTrending(),
        moviesAPI.getPopular(),
        seriesAPI.getTrending(),
        sportsAPI.getAll()
      ]);

      // Handle trending movies
      if (trendingMoviesRes.status === 'fulfilled') {
        setTrendingMovies(trendingMoviesRes.value.data || []);
      } else {
        console.error('Failed to fetch trending movies:', trendingMoviesRes.reason);
      }

      // Handle popular movies
      if (popularMoviesRes.status === 'fulfilled') {
        setPopularMovies(popularMoviesRes.value.data || []);
      } else {
        console.error('Failed to fetch popular movies:', popularMoviesRes.reason);
      }

      // Handle trending series
      if (trendingSeriesRes.status === 'fulfilled') {
        setTrendingSeries(trendingSeriesRes.value.data || []);
      } else {
        console.error('Failed to fetch trending series:', trendingSeriesRes.reason);
      }

      // Handle sports content
      if (sportsRes.status === 'fulfilled') {
        setSportsContent(sportsRes.value.data || []);
      } else {
        console.error('Failed to fetch sports content:', sportsRes.reason);
      }

    } catch (err) {
      console.error('Error fetching content:', err);
      setError('Failed to load content. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContent();
  }, []);

  const refetch = () => {
    fetchContent();
  };

  return {
    trendingMovies,
    popularMovies,
    trendingSeries,
    sportsContent,
    loading,
    error,
    refetch
  };
};