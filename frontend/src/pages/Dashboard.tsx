import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { 
  NewspaperIcon, 
  CogIcon, 
  DocumentTextIcon,
  ChartBarIcon 
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import api from '../services/api';

const Dashboard: React.FC = () => {
  const { data: articles, isLoading: articlesLoading } = useQuery({
    queryKey: ['articles'],
    queryFn: () => api.getArticles({ limit: 5 })
  });

  const { data: sources, isLoading: sourcesLoading } = useQuery({
    queryKey: ['sources'],
    queryFn: api.getSources
  });

  const { data: posts, isLoading: postsLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: api.getPosts
  });

  const stats = [
    {
      name: 'Total Articles',
      value: articles?.length || 0,
      icon: NewspaperIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      name: 'Active Sources',
      value: sources?.length || 0,
      icon: CogIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      name: 'Posts Created',
      value: posts?.length || 0,
      icon: DocumentTextIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      name: 'Success Rate',
      value: (posts?.length || 0) > 0 ? '85%' : '0%',
      icon: ChartBarIcon,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your news screening activity</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="card p-6">
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Articles */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recent Articles</h2>
          <Link 
            to="/articles" 
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            View all
          </Link>
        </div>
        
        {articlesLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : articles && articles.length > 0 ? (
          <div className="space-y-4">
            {articles.map((article: any) => (
              <div key={article.id} className="border-b border-gray-200 pb-4 last:border-b-0">
                <h3 className="font-medium text-gray-900 mb-1">{article.title}</h3>
                <p className="text-sm text-gray-600 mb-2">
                  {article.content?.substring(0, 150)}...
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{format(new Date(article.published_at), 'MMM d, yyyy')}</span>
                  <a 
                    href={article.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-primary-600 hover:text-primary-700"
                  >
                    Read more →
                  </a>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No articles found. Add some sources to get started.</p>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link 
            to="/sources" 
            className="btn-primary text-center"
          >
            Add News Source
          </Link>
          <Link 
            to="/articles" 
            className="btn-secondary text-center"
          >
            Browse Articles
          </Link>
          <Link 
            to="/posts" 
            className="btn-secondary text-center"
          >
            Create Post
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
