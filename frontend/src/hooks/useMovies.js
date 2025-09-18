import { useState, useEffect } from 'react';
import { moviesAPI, seriesAPI, sportsAPI } from '../services/api';

export const useMovies = () => {
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [hindiMovies, setHindiMovies] = useState([]);
  const [oldHindiMovies, setOldHindiMovies] = useState([]);
  const [trendingHindiMovies, setTrendingHindiMovies] = useState([]);
  const [punjabiMovies, setPunjabiMovies] = useState([]);
  const [oldPunjabiMovies, setOldPunjabiMovies] = useState([]);
  const [trendingPunjabiMovies, setTrendingPunjabiMovies] = useState([]);
  const [animeMovies, setAnimeMovies] = useState([]);
  const [trendingSeries, setTrendingSeries] = useState([]);
  const [webSeries, setWebSeries] = useState([]);
  const [sportsContent, setSportsContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchContent = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all content in parallel
      const requests = await Promise.allSettled([
        moviesAPI.getTrending(),
        moviesAPI.getPopular(),
        moviesAPI.getHindi(),
        moviesAPI.getOldHindi(),
        moviesAPI.getTrendingHindi(),
        moviesAPI.getPunjabi(),
        moviesAPI.getOldPunjabi(),
        moviesAPI.getTrendingPunjabi(),
        moviesAPI.getAnime(),
        seriesAPI.getTrending(),
        seriesAPI.getWeb(),
        sportsAPI.getAll()
      ]);

      // Handle results
      const results = requests.map(result => 
        result.status === 'fulfilled' ? result.value.data || [] : []
      );

      const [
        trendingRes,
        popularRes,
        hindiRes,
        oldHindiRes,
        trendingHindiRes,
        punjabiRes,
        oldPunjabiRes,
        trendingPunjabiRes,
        animeRes,
        trendingSeriesRes,
        webSeriesRes,
        sportsRes
      ] = results;

      // Set all the state
      setTrendingMovies(trendingRes);
      setPopularMovies(popularRes);
      setHindiMovies(hindiRes);
      setOldHindiMovies(oldHindiRes);
      setTrendingHindiMovies(trendingHindiRes);
      setPunjabiMovies(punjabiRes);
      setOldPunjabiMovies(oldPunjabiRes);
      setTrendingPunjabiMovies(trendingPunjabiRes);
      setAnimeMovies(animeRes);
      setTrendingSeries(trendingSeriesRes);
      setWebSeries(webSeriesRes);
      setSportsContent(sportsRes);

      // Log any failed requests
      requests.forEach((result, index) => {
        if (result.status === 'rejected') {
          const categories = [
            'trending movies', 'popular movies', 'hindi movies', 'old hindi movies',
            'trending hindi movies', 'punjabi movies', 'old punjabi movies',
            'trending punjabi movies', 'anime movies', 'trending series',
            'web series', 'sports content'
          ];
          console.error(`Failed to fetch ${categories[index]}:`, result.reason);
        }
      });

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
  };
};