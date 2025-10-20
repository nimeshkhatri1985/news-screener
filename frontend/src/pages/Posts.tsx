import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { DocumentTextIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import api from '../services/api';

const Posts: React.FC = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newPost, setNewPost] = useState({
    article_id: 0,
    content: ''
  });

  const queryClient = useQueryClient();

  const { data: posts, isLoading: postsLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: api.getPosts
  });
  const { data: articles, isLoading: articlesLoading } = useQuery({
    queryKey: ['articles'],
    queryFn: () => api.getArticles({ limit: 100 })
  });

  const createPostMutation = useMutation({
    mutationFn: api.createPost,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      setShowCreateForm(false);
      setNewPost({ article_id: 0, content: '' });
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newPost.article_id && newPost.content.trim()) {
      createPostMutation.mutate(newPost);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'posted':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <DocumentTextIcon className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'posted':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Social Media Posts</h1>
          <p className="text-gray-600">Manage your curated posts and posting history</p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary"
        >
          Create New Post
        </button>
      </div>

      {/* Create Post Form */}
      {showCreateForm && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Post</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Select Article
              </label>
              <select
                value={newPost.article_id}
                onChange={(e) => setNewPost({ ...newPost, article_id: Number(e.target.value) })}
                className="input-field"
                required
              >
                <option value={0}>Choose an article...</option>
                {articles?.map((article) => (
                  <option key={article.id} value={article.id}>
                    {article.title.substring(0, 80)}...
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Post Content
              </label>
              <textarea
                value={newPost.content}
                onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
                className="input-field"
                rows={4}
                placeholder="Write your social media post here..."
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                {newPost.content.length}/280 characters
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={createPostMutation.isLoading}
                className="btn-primary"
              >
                {createPostMutation.isLoading ? 'Creating...' : 'Create Post'}
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Posts List */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Posting History</h2>
        
        {postsLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : posts && posts.length > 0 ? (
          <div className="space-y-4">
            {posts.map((post) => {
              const article = articles?.find(a => a.id === post.article_id);
              return (
                <div key={post.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        {getStatusIcon(post.status)}
                        <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(post.status)}`}>
                          {post.status}
                        </span>
                        {post.posted_at && (
                          <span className="text-xs text-gray-500">
                            Posted: {format(new Date(post.posted_at), 'MMM d, yyyy • h:mm a')}
                          </span>
                        )}
                      </div>
                      <p className="text-gray-900 mb-2">{post.content}</p>
                      {article && (
                        <div className="text-sm text-gray-600">
                          <p className="font-medium">From: {article.title}</p>
                          <a 
                            href={article.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-primary-600 hover:text-primary-700"
                          >
                            View original article →
                          </a>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      {post.status === 'draft' && (
                        <button className="btn-primary text-sm">
                          Post Now
                        </button>
                      )}
                      {post.twitter_id && (
                        <a
                          href={`https://twitter.com/i/web/status/${post.twitter_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-600 hover:text-primary-700 text-sm"
                        >
                          View on Twitter
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">No posts created yet</p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="btn-primary"
            >
              Create Your First Post
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Posts;
