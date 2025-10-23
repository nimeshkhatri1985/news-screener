import React, { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { ArrowTopRightOnSquareIcon, DocumentTextIcon, MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import api from '../services/api';

const Articles: React.FC = () => {
  const [selectedSource, setSelectedSource] = useState<number | undefined>();
  const [searchTerm, setSearchTerm] = useState('');
  const [keywords, setKeywords] = useState('');
  const [category, setCategory] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  const { data: sources } = useQuery({
    queryKey: ['sources'],
    queryFn: api.getSources
  });
  
  // Use search API if search term is provided, otherwise use articles API with filters
  const { data: articles, isLoading } = useQuery({
    queryKey: ['articles', selectedSource, keywords, category, dateFrom, dateTo, searchTerm],
    queryFn: () => {
      if (searchTerm.trim()) {
        return api.searchArticles({ 
          q: searchTerm,
          source_id: selectedSource,
          limit: 50 
        });
      } else {
        return api.getArticles({ 
          source_id: selectedSource,
          keywords: keywords || undefined,
          category: category || undefined,
          date_from: dateFrom || undefined,
          date_to: dateTo || undefined,
          limit: 50 
        });
      }
    }
  });

  const filteredArticles = articles || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Articles</h1>
        <p className="text-gray-600">Browse and filter articles from your sources</p>
      </div>

      {/* Filters */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Filters & Search</h2>
          <button
            onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700"
          >
            <FunnelIcon className="h-5 w-5" />
            <span>{showAdvancedFilters ? 'Hide' : 'Show'} Advanced Filters</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Filter by Source
            </label>
            <select
              value={selectedSource || ''}
              onChange={(e) => setSelectedSource(e.target.value ? Number(e.target.value) : undefined)}
              className="input-field"
            >
              <option value="">All Sources</option>
              {sources?.map((source: any) => (
                <option key={source.id} value={source.id}>
                  {source.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search Articles
            </label>
            <div className="relative">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
                placeholder="Search by title or content..."
              />
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
            </div>
          </div>
        </div>

        {/* Advanced Filters */}
        {showAdvancedFilters && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="text-md font-medium text-gray-900 mb-4">Advanced Filters</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Keywords (comma-separated)
                </label>
                <input
                  type="text"
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                  className="input-field"
                  placeholder="ai, machine learning, tech"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <input
                  type="text"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="input-field"
                  placeholder="technology, business, science"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date Range
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="date"
                    value={dateFrom}
                    onChange={(e) => setDateFrom(e.target.value)}
                    className="input-field text-sm"
                    placeholder="From"
                  />
                  <input
                    type="date"
                    value={dateTo}
                    onChange={(e) => setDateTo(e.target.value)}
                    className="input-field text-sm"
                    placeholder="To"
                  />
                </div>
              </div>
            </div>
            <div className="mt-4 flex space-x-3">
              <button
                onClick={() => {
                  setKeywords('');
                  setCategory('');
                  setDateFrom('');
                  setDateTo('');
                }}
                className="btn-secondary text-sm"
              >
                Clear Filters
              </button>
              <div className="text-sm text-gray-500 flex items-center">
                {filteredArticles.length} articles found
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Articles List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="card p-6 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        ) : filteredArticles.length > 0 ? (
          filteredArticles.map((article: any) => (
            <div key={article.id} className="card p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {article.title}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {article.content?.substring(0, 300)}...
                  </p>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>
                      {format(new Date(article.published_at), 'MMM d, yyyy • h:mm a')}
                    </span>
                    <span>
                      Source: {sources?.find((s: any) => s.id === article.source_id)?.name}
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                    title="Read original article"
                  >
                    <ArrowTopRightOnSquareIcon className="h-5 w-5" />
                  </a>
                  <button
                    className="p-2 text-blue-600 hover:text-blue-700 transition-colors"
                    title="Create post from this article"
                  >
                    <DocumentTextIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card p-8 text-center">
            <p className="text-gray-500 mb-4">No articles found</p>
            <p className="text-sm text-gray-400">
              {selectedSource || searchTerm 
                ? 'Try adjusting your filters' 
                : 'Add some news sources to get started'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Articles;
