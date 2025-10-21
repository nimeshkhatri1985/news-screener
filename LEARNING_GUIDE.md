# 🎓 Understanding News Screener Implementation

## 📚 **Learning Path: From Beginner to Expert**

### **Start Here: The Big Picture**

**News Screener** is a full-stack web application that helps you:
1. Monitor news from multiple RSS feeds
2. Filter articles by keywords, dates, and sources
3. Create social media posts from curated articles

**Architecture**: Monolithic application with separate frontend and backend

---

## 🗺️ **Recommended Learning Order**

### **Phase 1: Understanding the Basics (Start Here!)**

#### **1. Read the Main README** 
📄 **File**: `/README.md`
- **What to Learn**: Project overview, features, tech stack
- **Time**: 10 minutes
- **Why Start Here**: Gives you the 30,000-foot view

#### **2. Understand the Tech Stack**
📄 **File**: `/TECHNICAL_DOCUMENTATION.md` (Section 2)
- **What to Learn**: Why we chose FastAPI, React, TypeScript, etc.
- **Key Concepts**: 
  - FastAPI for Python backends
  - React for interactive UIs
  - TypeScript for type safety
- **Time**: 15 minutes

---

### **Phase 2: Backend Understanding**

#### **3. Start with the Database Models**
📄 **File**: `/backend/main.py` (Lines 17-85)
- **What to Learn**: Data structure and relationships
- **Key Models**:
  ```python
  Source      # News sources (RSS feeds)
  Article     # Individual news articles
  Filter      # User-defined filters
  Post        # Social media posts
  ```
- **Time**: 20 minutes
- **Hands-on**: Look at each model and understand what data it stores

#### **4. Explore API Endpoints**
📄 **File**: `/backend/main.py` (Lines 120-250)
- **What to Learn**: How frontend communicates with backend
- **Key Endpoints**:
  ```
  GET  /sources     → List all news sources
  POST /sources     → Add new source
  GET  /articles    → List articles (with filtering)
  GET  /filters     → List saved filters
  GET  /posts       → List social media posts
  ```
- **Time**: 30 minutes
- **Hands-on**: Open http://localhost:8000/docs and try the endpoints

#### **5. Understanding the Scraper**
📄 **File**: `/backend/scraper.py`
- **What to Learn**: How we fetch articles from RSS feeds
- **Key Concept**: RSS feed parsing with feedparser
- **Time**: 15 minutes

---

### **Phase 3: Frontend Understanding**

#### **6. Start with the Entry Point**
📄 **File**: `/frontend/src/index.tsx`
- **What to Learn**: How the React app initializes
- **Key Concepts**:
  - React Router for navigation
  - TanStack Query for data fetching
- **Time**: 10 minutes

#### **7. Understand the Component Structure**
📄 **Files**: 
- `/frontend/src/components/Header.tsx` - Navigation header
- `/frontend/src/pages/Dashboard.tsx` - Home page
- `/frontend/src/pages/Sources.tsx` - Manage sources
- `/frontend/src/pages/Articles.tsx` - Browse articles
- `/frontend/src/pages/Posts.tsx` - Manage posts

**Order to Read**:
1. **Header.tsx** (5 min) - Simple navigation component
2. **Dashboard.tsx** (15 min) - Shows overview with cards
3. **Sources.tsx** (20 min) - Form submission example
4. **Articles.tsx** (30 min) - Complex filtering logic
5. **Posts.tsx** (15 min) - Similar to Sources

#### **8. Understanding API Communication**
📄 **File**: `/frontend/src/services/api.ts`
- **What to Learn**: How frontend talks to backend
- **Key Concepts**:
  - Axios for HTTP requests
  - TypeScript interfaces for type safety
- **Time**: 15 minutes

---

### **Phase 4: Deep Dive into Key Features**

#### **9. The Filtering System**
**Files to Study**:
- Backend: `/backend/main.py` (Lines 143-187)
- Frontend: `/frontend/src/pages/Articles.tsx` (Lines 16-42)

**What Happens**:
```
User types keyword → Frontend sends GET request → 
Backend filters database → Returns matching articles → 
Frontend displays results
```
**Time**: 30 minutes

#### **10. Form Submissions**
**Example**: Adding a new source
- Frontend: `/frontend/src/pages/Sources.tsx` (Lines 22-34)
- Backend: `/backend/main.py` (Lines 135-142)

**Flow**:
```
User fills form → Click submit → POST request → 
Backend validates data → Save to database → 
Return success → Frontend updates UI
```
**Time**: 20 minutes

---

## 🎯 **Quick Reference Guide**

### **Key Files and Their Purpose**

| File | Purpose | Complexity |
|------|---------|-----------|
| `/backend/main.py` | Core API logic | ⭐⭐⭐ |
| `/frontend/src/pages/Articles.tsx` | Article filtering UI | ⭐⭐⭐ |
| `/frontend/src/services/api.ts` | API communication | ⭐⭐ |
| `/backend/scraper.py` | RSS feed parsing | ⭐⭐ |
| `/frontend/src/pages/Dashboard.tsx` | Dashboard UI | ⭐⭐ |
| `/frontend/src/components/Header.tsx` | Navigation | ⭐ |

---

## 🔍 **Understanding by Example**

### **Example 1: How Article Filtering Works**

**Step 1 - User Action** (Frontend):
```typescript
// User types "AI" in search box
setSearchTerm("AI")
```

**Step 2 - API Call** (Frontend):
```typescript
// React Query fetches filtered articles
api.getArticles({ keywords: "AI" })
```

**Step 3 - Backend Processing**:
```python
# Backend receives: GET /articles?keywords=AI
# Searches database for articles containing "AI"
query.filter(Article.title.ilike('%AI%'))
```

**Step 4 - Response**:
```typescript
// Frontend receives array of matching articles
// Displays them in the UI
```

### **Example 2: Adding a News Source**

**Step 1 - User Fills Form**:
```
Name: "BBC News"
URL: "https://bbc.com"
RSS Feed: "https://bbc.com/rss"
```

**Step 2 - Submit**:
```typescript
createSourceMutation.mutate({
  name: "BBC News",
  url: "https://bbc.com",
  rss_feed: "https://bbc.com/rss",
  is_active: true
})
```

**Step 3 - Backend Saves**:
```python
db_source = Source(**source_data)
db.add(db_source)
db.commit()
```

**Step 4 - UI Updates**:
```typescript
// React Query refetches sources list
// New source appears in the list
```

---

## 📖 **Code Reading Tips**

### **For Backend (Python/FastAPI)**
1. **Start with models** (classes) - understand data structure
2. **Read endpoint decorators** (`@app.get`, `@app.post`)
3. **Follow the request flow**: Input → Processing → Output
4. **Pay attention to type hints**: `async def get_articles() -> List[Article]`

### **For Frontend (React/TypeScript)**
1. **Look for `useState`** - this manages component state
2. **Find `useQuery`** - this fetches data from API
3. **Understand JSX** - HTML-like syntax in JavaScript
4. **Follow props** - data passed between components

---

## 🎓 **Concepts to Understand**

### **Backend Concepts**
- **REST API**: Endpoints that respond to HTTP requests
- **ORM (SQLAlchemy)**: Maps Python classes to database tables
- **Async/Await**: Non-blocking code execution
- **Pydantic Models**: Data validation and serialization

### **Frontend Concepts**
- **React Hooks**: `useState`, `useQuery`, `useMutation`
- **React Router**: Client-side navigation
- **TanStack Query**: Server state management
- **TypeScript**: JavaScript with types

### **Full Stack Concepts**
- **API Communication**: How frontend and backend talk
- **State Management**: Keeping UI in sync with data
- **Form Handling**: User input → validation → submission
- **Real-time Updates**: Automatic UI refresh after data changes

---

## 🎯 **Next Steps After Understanding**

1. **Experiment**: Change some code and see what happens
2. **Add Features**: Try adding a new field to a model
3. **Debug**: Use browser DevTools and Python debugger
4. **Extend**: Add Twitter integration (next phase)

---

## 📚 **Additional Resources**

### **Official Documentation**
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **TanStack Query**: https://tanstack.com/query/latest
- **Tailwind CSS**: https://tailwindcss.com/

### **Our Documentation**
- `/TECHNICAL_DOCUMENTATION.md` - Detailed technical decisions
- `/CODE_OVERVIEW.md` - File-by-file breakdown
- `/README.md` - Setup and usage guide

---

## 💡 **Pro Tips**

1. **Don't try to understand everything at once** - Focus on one feature
2. **Use the browser DevTools** - Watch network requests
3. **Use print statements** - See what data flows through
4. **Read error messages carefully** - They're usually helpful
5. **Ask questions** - Better to ask than to guess

---

## 🎯 **Your Learning Checklist**

- [ ] Read main README
- [ ] Understand tech stack choices
- [ ] Study database models
- [ ] Try API endpoints in Swagger UI (http://localhost:8000/docs)
- [ ] Read Header component (simplest)
- [ ] Read Dashboard component
- [ ] Understand API service
- [ ] Study filtering system
- [ ] Trace a full request/response cycle
- [ ] Try modifying something small
- [ ] Celebrate understanding! 🎉

---

**Start with the README, then come back to this guide for deeper understanding!**
