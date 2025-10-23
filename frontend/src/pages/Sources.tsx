import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import api from '../services/api';

const Sources: React.FC = () => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [newSource, setNewSource] = useState({
    name: '',
    url: '',
    rss_feed: '',
    is_active: true
  });

  const queryClient = useQueryClient();

  const { data: sources, isLoading } = useQuery({
    queryKey: ['sources'],
    queryFn: api.getSources
  });

  const createSourceMutation = useMutation({
    mutationFn: api.createSource,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] });
      setShowAddForm(false);
      setNewSource({ name: '', url: '', rss_feed: '', is_active: true });
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createSourceMutation.mutate(newSource);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">News Sources</h1>
          <p className="text-gray-600">Manage your news sources and RSS feeds</p>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <PlusIcon className="h-5 w-5" />
          <span>Add Source</span>
        </button>
      </div>

      {/* Add Source Form */}
      {showAddForm && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Add New Source</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Source Name
              </label>
              <input
                type="text"
                value={newSource.name}
                onChange={(e) => setNewSource({ ...newSource, name: e.target.value })}
                className="input-field"
                placeholder="e.g., TechCrunch"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Website URL
              </label>
              <input
                type="url"
                value={newSource.url}
                onChange={(e) => setNewSource({ ...newSource, url: e.target.value })}
                className="input-field"
                placeholder="https://techcrunch.com"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                RSS Feed URL
              </label>
              <input
                type="url"
                value={newSource.rss_feed}
                onChange={(e) => setNewSource({ ...newSource, rss_feed: e.target.value })}
                className="input-field"
                placeholder="https://techcrunch.com/feed/"
                required
              />
            </div>
            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={createSourceMutation.isLoading}
                className="btn-primary"
              >
                {createSourceMutation.isLoading ? 'Adding...' : 'Add Source'}
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Sources List */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Active Sources</h2>
        
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : sources && sources.length > 0 ? (
          <div className="space-y-4">
            {sources.map((source: any) => (
              <div key={source.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">{source.name}</h3>
                    <p className="text-sm text-gray-600">
                      <a 
                        href={source.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700"
                      >
                        {source.url}
                      </a>
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      RSS: {source.rss_feed}
                    </p>
                    <p className="text-xs text-gray-500">
                      Added: {format(new Date(source.created_at), 'MMM d, yyyy')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      source.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {source.is_active ? 'Active' : 'Inactive'}
                    </span>
                    <button className="text-red-600 hover:text-red-700">
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">No sources added yet</p>
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-primary"
            >
              Add Your First Source
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sources;
