import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import api, { ArticleWithScore, HaryanaFilterPreset, TweetPreview } from '../services/api';
import { 
  FunnelIcon, 
  SparklesIcon,
  ArrowTopRightOnSquareIcon,
  BuildingOfficeIcon,
  AcademicCapIcon,
  CurrencyDollarIcon,
  TruckIcon,
  TrophyIcon,
  GlobeAltIcon,
  CheckBadgeIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { 
  ChatBubbleLeftRightIcon as TwitterIcon 
} from '@heroicons/react/24/solid';
import { format } from 'date-fns';

const HaryanaNews: React.FC = () => {
  const [selectedPreset, setSelectedPreset] = useState<string>('tourism');
  const [selectedSentiment, setSelectedSentiment] = useState<string>('positive');
  const [minScore, setMinScore] = useState<number>(20);
  const [selectedArticle, setSelectedArticle] = useState<ArticleWithScore | null>(null);
  const [tweetModalArticle, setTweetModalArticle] = useState<ArticleWithScore | null>(null);
  const [tweetPreview, setTweetPreview] = useState<TweetPreview | null>(null);
  const [customMessage, setCustomMessage] = useState<string>('');
  const [includeHashtags, setIncludeHashtags] = useState<boolean>(true);
  const [tweetSuccess, setTweetSuccess] = useState<string>('');
  const [tweetError, setTweetError] = useState<string>('');
  const [usePremium, setUsePremium] = useState<boolean>(true);

  const { data: presets, isLoading: presetsLoading } = useQuery({
    queryKey: ['haryana-presets'],
    queryFn: api.getHaryanaFilterPresets
  });

  const { data: articles, isLoading: articlesLoading } = useQuery({
    queryKey: ['haryana-articles', selectedPreset, selectedSentiment, minScore],
    queryFn: () => api.getHaryanaArticles({
      filter_preset: selectedPreset,
      sentiment: selectedSentiment || undefined,
      min_score: minScore,
      limit: 100
    }),
    enabled: !!selectedPreset
  });

  const { data: twitterStatus } = useQuery({
    queryKey: ['twitter-status'],
    queryFn: api.getTwitterStatus
  });

  const previewMutation = useMutation({
    mutationFn: api.previewTweet,
    onSuccess: (data) => {
      setTweetPreview(data);
      setTweetError('');
    },
    onError: (error: any) => {
      setTweetError(error.response?.data?.detail || 'Failed to preview tweet');
    }
  });

  const postMutation = useMutation({
    mutationFn: api.postToTwitter,
    onSuccess: (data) => {
      setTweetSuccess(data.tweet_url || 'Tweet posted successfully!');
      setTweetError('');
      setTimeout(() => {
        setTweetModalArticle(null);
        setTweetSuccess('');
        setCustomMessage('');
        setTweetPreview(null);
      }, 3000);
    },
    onError: (error: any) => {
      setTweetError(error.response?.data?.detail || 'Failed to post tweet');
    }
  });

  const handleOpenTweetModal = (article: ArticleWithScore, e: React.MouseEvent) => {
    e.stopPropagation();
    setTweetModalArticle(article);
    setTweetSuccess('');
    setTweetError('');
    setCustomMessage('');
    setUsePremium(false);
    setTweetPreview(null);
    
    previewMutation.mutate({
      article_id: article.id,
      include_hashtags: includeHashtags,
      use_premium: false
    });
  };

  const handlePreviewUpdate = (premiumOverride?: boolean) => {
    if (tweetModalArticle) {
      const isPremium = premiumOverride !== undefined ? premiumOverride : usePremium;
      console.log('🔍 Preview Request:', {
        article_id: tweetModalArticle.id,
        use_premium: isPremium,
        include_hashtags: includeHashtags
      });
      previewMutation.mutate({
        article_id: tweetModalArticle.id,
        custom_message: customMessage || undefined,
        include_hashtags: includeHashtags,
        use_premium: isPremium
      });
    }
  };

  const handlePostToTwitter = () => {
    if (tweetModalArticle) {
      postMutation.mutate({
        article_id: tweetModalArticle.id,
        custom_message: customMessage || undefined,
        include_hashtags: includeHashtags,
        use_premium: usePremium
      });
    }
  };

  const getPresetIcon = (key: string) => {
    const icons: Record<string, any> = {
      tourism: GlobeAltIcon,
      infrastructure: BuildingOfficeIcon,
      economy: CurrencyDollarIcon,
      education: AcademicCapIcon,
      agriculture: TruckIcon,
      sports: TrophyIcon,
      environment: SparklesIcon,
      governance: CheckBadgeIcon
    };
    return icons[key] || FunnelIcon;
  };

  const getSentimentBadge = (sentiment?: string) => {
    if (!sentiment) return null;
    
    const colors: Record<string, string> = {
      positive: 'bg-green-100 text-green-800 border-green-200',
      negative: 'bg-red-100 text-red-800 border-red-200',
      neutral: 'bg-gray-100 text-gray-800 border-gray-200'
    };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium border ${colors[sentiment] || colors.neutral}`}>
        {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
      </span>
    );
  };

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <SparklesIcon className="h-8 w-8 text-blue-600 mr-3" />
              Haryana News Screener
            </h1>
            <p className="text-gray-600 mt-2">
              Intelligent filtering for Haryana-specific news with topic-based categorization and sentiment analysis
            </p>
          </div>
        </div>
      </div>

      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Select News Category</h2>
        {presetsLoading ? (
          <div className="text-center py-4">Loading categories...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {presets && (Object.entries(presets) as [string, HaryanaFilterPreset][]).map(([key, preset]) => {
              const Icon = getPresetIcon(key);
              const isSelected = selectedPreset === key;
              return (
                <button
                  key={key}
                  onClick={() => setSelectedPreset(key)}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    isSelected
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start">
                    <Icon className={`h-6 w-6 mr-3 ${isSelected ? 'text-blue-600' : 'text-gray-400'}`} />
                    <div className="flex-1">
                      <h3 className={`font-medium ${isSelected ? 'text-blue-900' : 'text-gray-900'}`}>
                        {preset.name}
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">{preset.description}</p>
                      <p className="text-xs text-gray-500 mt-2">{preset.keyword_count} keywords</p>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>

      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Refine Results</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sentiment Filter
            </label>
            <select
              value={selectedSentiment}
              onChange={(e) => setSelectedSentiment(e.target.value)}
              className="input-field"
            >
              <option value="">All Sentiments</option>
              <option value="positive">Positive Only</option>
              <option value="neutral">Neutral Only</option>
              <option value="negative">Negative Only</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Relevance Score
            </label>
            <input
              type="number"
              value={minScore}
              onChange={(e) => setMinScore(Number(e.target.value))}
              className="input-field"
              min="0"
              step="10"
              placeholder="0"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={() => {
                setSelectedSentiment('');
                setMinScore(0);
              }}
              className="btn-secondary w-full"
            >
              Reset Filters
            </button>
          </div>
        </div>
      </div>

      {articles && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <SparklesIcon className="h-5 w-5 text-blue-600 mr-2" />
              <span className="font-medium text-blue-900">
                {articles.length} relevant articles found
              </span>
            </div>
            <div className="text-sm text-blue-700">
              Category: {presets?.[selectedPreset]?.name || selectedPreset}
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Filtered Articles
          </h2>
          {articlesLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="text-gray-600 mt-4">Analyzing articles...</p>
            </div>
          ) : articles && articles.length > 0 ? (
            <div className="space-y-4">
              {articles.map((article: ArticleWithScore) => (
                <div
                  key={article.id}
                  className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer"
                  onClick={() => setSelectedArticle(article)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 flex-1">
                      {article.title}
                    </h3>
                    {getSentimentBadge(article.sentiment)}
                  </div>
                  
                  <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                    {article.content.substring(0, 200)}...
                  </p>

                  <div className="flex flex-wrap items-center gap-4 text-sm">
                    <div className="flex items-center text-blue-600">
                      <SparklesIcon className="h-4 w-4 mr-1" />
                      <span className="font-medium">Score: {article.relevance_score}</span>
                    </div>
                    
                    {article.matched_keywords && article.matched_keywords.length > 0 && (
                      <div className="flex items-center text-gray-600">
                        <span className="font-medium mr-2">Keywords:</span>
                        <div className="flex flex-wrap gap-1">
                          {article.matched_keywords.slice(0, 5).map((keyword: string, idx: number) => (
                            <span
                              key={idx}
                              className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs"
                            >
                              {keyword}
                            </span>
                          ))}
                          {article.matched_keywords.length > 5 && (
                            <span className="text-gray-500 text-xs">
                              +{article.matched_keywords.length - 5} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    <div className="ml-auto flex items-center space-x-4">
                      <span className="text-gray-500">
                        {format(new Date(article.published_at), 'MMM dd, yyyy')}
                      </span>
                      
                      <button
                        onClick={(e) => handleOpenTweetModal(article, e)}
                        className="flex items-center px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                        title="Post to Twitter"
                      >
                        <TwitterIcon className="h-4 w-4 mr-1" />
                        <span className="text-sm">Tweet</span>
                      </button>
                      
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="flex items-center text-blue-600 hover:text-blue-700"
                      >
                        <span className="mr-1">Read</span>
                        <ArrowTopRightOnSquareIcon className="h-4 w-4" />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <SparklesIcon className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p>No articles found matching your criteria.</p>
              <p className="text-sm mt-2">Try adjusting your filters or selecting a different category.</p>
            </div>
          )}
        </div>
      </div>

      {selectedArticle && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedArticle(null)}
        >
          <div
            className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-gray-900 flex-1">
                  {selectedArticle.title}
                </h2>
                <button
                  onClick={() => setSelectedArticle(null)}
                  className="text-gray-400 hover:text-gray-600 ml-4"
                >
                  <span className="text-2xl">&times;</span>
                </button>
              </div>

              <div className="flex items-center gap-3 mb-4">
                {getSentimentBadge(selectedArticle.sentiment)}
                <span className="text-sm text-gray-600">
                  Score: {selectedArticle.relevance_score}
                </span>
                <span className="text-sm text-gray-500">
                  {format(new Date(selectedArticle.published_at), 'MMMM dd, yyyy')}
                </span>
              </div>

              <div className="prose max-w-none mb-6">
                <p className="text-gray-700">{selectedArticle.content}</p>
              </div>

              {selectedArticle.matched_keywords && selectedArticle.matched_keywords.length > 0 && (
                <div className="mb-4">
                  <h3 className="text-sm font-semibold text-gray-900 mb-2">Matched Keywords</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedArticle.matched_keywords.map((keyword, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex gap-3 pt-4 border-t border-gray-200">
                <a
                  href={selectedArticle.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary flex items-center"
                >
                  Read Full Article
                  <ArrowTopRightOnSquareIcon className="h-4 w-4 ml-2" />
                </a>
                <button
                  onClick={() => setSelectedArticle(null)}
                  className="btn-secondary"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {tweetModalArticle && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setTweetModalArticle(null)}
        >
          <div
            className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                  <TwitterIcon className="h-6 w-6 mr-2 text-blue-500" />
                  Post to Twitter
                </h2>
                <button
                  onClick={() => setTweetModalArticle(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>

              {twitterStatus && !twitterStatus.configured && (
                <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
                  <p className="text-yellow-800 text-sm">
                    ⚠️ Twitter API not configured. See TWITTER_SETUP_GUIDE.md for setup instructions.
                  </p>
                </div>
              )}

              <div className="mb-4 p-4 bg-gray-50 rounded">
                <h3 className="font-semibold text-gray-900 mb-2">
                  {tweetModalArticle.title}
                </h3>
                <p className="text-sm text-gray-600">
                  Score: {tweetModalArticle.relevance_score} | Sentiment: {tweetModalArticle.sentiment}
                </p>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Custom Message (Optional)
                </label>
                <textarea
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  onBlur={() => handlePreviewUpdate()}
                  placeholder="Add your own message..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
              </div>

              <div className="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <label className="block text-sm font-medium text-gray-900 mb-3">
                  Twitter Account Type
                </label>
                <div className="space-y-2">
                  <div className="flex items-center">
                    <input
                      type="radio"
                      id="freeAccount"
                      name="accountType"
                      checked={!usePremium}
                      onChange={() => {
                        console.log('📻 Switching to FREE account');
                        setUsePremium(false);
                        setTimeout(() => handlePreviewUpdate(false), 100);
                      }}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <label htmlFor="freeAccount" className="ml-2 text-sm text-gray-700">
                      <span className="font-medium">Free Account</span> - Concise tweet (~150-250 chars: title + hashtags + link)
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      type="radio"
                      id="premiumAccount"
                      name="accountType"
                      checked={usePremium}
                      onChange={() => {
                        console.log('📻 Switching to PREMIUM account');
                        setUsePremium(true);
                        setTimeout(() => handlePreviewUpdate(true), 100);
                      }}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <label htmlFor="premiumAccount" className="ml-2 text-sm text-gray-700">
                      <span className="font-medium">Premium Account</span> - Detailed tweet with full summary (280-4000 chars)
                    </label>
                  </div>
                </div>
              </div>

              <div className="mb-4 flex items-center">
                <input
                  type="checkbox"
                  id="includeHashtags"
                  checked={includeHashtags}
                  onChange={(e) => {
                    setIncludeHashtags(e.target.checked);
                    setTimeout(handlePreviewUpdate, 100);
                  }}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="includeHashtags" className="ml-2 text-sm text-gray-700">
                  Include hashtags (#Haryana #HaryanaNews)
                </label>
              </div>

              {previewMutation.isPending && (
                <div className="mb-4 p-4 bg-gray-50 rounded">
                  <p className="text-gray-600">Loading preview...</p>
                </div>
              )}

              {tweetPreview && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tweet Preview ({tweetPreview.character_count}/{usePremium ? '4000' : '280'} characters)
                  </label>
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded whitespace-pre-wrap">
                    {tweetPreview.tweet_text}
                  </div>
                </div>
              )}

              {tweetSuccess && (
                <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded">
                  <p className="text-green-800">
                    ✅ Tweet posted successfully!
                    {tweetSuccess.startsWith('http') && (
                      <a
                        href={tweetSuccess}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="ml-2 text-green-600 hover:text-green-700 underline"
                      >
                        View Tweet
                      </a>
                    )}
                  </p>
                </div>
              )}

              {tweetError && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded">
                  <p className="text-red-800">❌ {tweetError}</p>
                </div>
              )}

              <div className="flex gap-3 pt-4 border-t border-gray-200">
                <button
                  onClick={handlePostToTwitter}
                  disabled={postMutation.isPending || !twitterStatus?.configured || !!tweetSuccess}
                  className="btn-primary flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <TwitterIcon className="h-4 w-4 mr-2" />
                  {postMutation.isPending ? 'Posting...' : 'Post to Twitter'}
                </button>
                <button
                  onClick={() => setTweetModalArticle(null)}
                  className="btn-secondary"
                >
                  {tweetSuccess ? 'Done' : 'Cancel'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HaryanaNews;
