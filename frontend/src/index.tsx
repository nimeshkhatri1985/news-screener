import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './index.css';

// Import components
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Sources from './pages/Sources';
import Articles from './pages/Articles';
import Posts from './pages/Posts';
import HaryanaNews from './pages/HaryanaNews';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/sources" element={<Sources />} />
              <Route path="/articles" element={<Articles />} />
              <Route path="/posts" element={<Posts />} />
              <Route path="/haryana" element={<HaryanaNews />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);