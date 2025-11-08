# 🏗️ System Architecture

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT UI (app.py)                   │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │ Overview │ Members  │  Books   │  Trans.  │ AI Insights│ │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│  ┌──────────┬──────────┬──────────────────────────────┐    │
│  │  Recs    │   NLP    │        Settings              │    │
│  └──────────┴──────────┴──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              BUSINESS LOGIC LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         LibraryManager (library_manager.py)          │  │
│  │  • add_member()      • borrow_book()                 │  │
│  │  • add_book()        • return_book()                 │  │
│  │  • get_all_*()       • get_dashboard_stats()         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│   AI ENGINE      │ │   DATABASE   │ │  EXPORT UTILS    │
│  (ai_engine.py)  │ │  (models.py) │ │(export_utils.py) │
├──────────────────┤ ├──────────────┤ ├──────────────────┤
│• Collaborative   │ │• Member      │ │• CSV Export      │
│  Filtering       │ │• Book        │ │• Reports         │
│• Content-Based   │ │• Transaction │ │• Overdue List    │
│  Filtering       │ │              │ │                  │
│• K-Means         │ │  SQLAlchemy  │ │                  │
│  Clustering      │ │     ORM      │ │                  │
│• Random Forest   │ │              │ │                  │
│  Prediction      │ │   SQLite     │ │                  │
│• NLP Search      │ │   Database   │ │                  │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

---

## 🔄 Data Flow

### 1. User Borrows a Book
```
User (UI) 
  → app.py (Streamlit)
    → library_manager.borrow_book()
      → Validate member & book
      → Check borrowing limits
      → Create Transaction
      → Update book availability
      → Commit to Database
    ← Return success/error
  ← Display notification
```

### 2. AI Recommendation Generation
```
User selects member (UI)
  → app.py
    → ai_engine.collaborative_filtering()
      → Load transaction history
      → Build user-book matrix
      → Calculate cosine similarity
      → Find similar users
      → Aggregate recommendations
    ← Return top-N books
    
    → ai_engine.content_based_filtering()
      → Analyze user's genre preferences
      → Analyze user's author preferences
      → Score available books
      → Rank by relevance
    ← Return top-N books
    
  ← Display both recommendation lists
```

### 3. Late Return Prediction
```
System loads active transactions
  → app.py
    → ai_engine.train_late_predictor()
      → Load historical transactions
      → Engineer features
      → Train Random Forest model
    ← Model ready
    
    → For each active transaction:
      → ai_engine.predict_late_return()
        → Extract member features
        → Calculate late rate
        → Predict probability
      ← Return risk score
    
  ← Display risk table
```

---

## 🗄️ Database Schema

```sql
┌─────────────────────────────────────────┐
│              MEMBERS                    │
├─────────────────────────────────────────┤
│ id (PK)          INTEGER                │
│ name             VARCHAR                │
│ email            VARCHAR (UNIQUE)       │
│ join_date        DATETIME               │
│ total_fines      FLOAT                  │
│ is_active        BOOLEAN                │
└─────────────────────────────────────────┘
                    │
                    │ 1:N
                    ▼
┌─────────────────────────────────────────┐
│           TRANSACTIONS                  │
├─────────────────────────────────────────┤
│ id (PK)          INTEGER                │
│ member_id (FK)   INTEGER ───────────────┤
│ book_id (FK)     INTEGER                │
│ borrow_date      DATETIME               │
│ due_date         DATETIME               │
│ return_date      DATETIME (NULL)        │
│ fine             FLOAT                  │
│ status           VARCHAR                │
└─────────────────────────────────────────┘
                    │
                    │ N:1
                    ▼
┌─────────────────────────────────────────┐
│               BOOKS                     │
├─────────────────────────────────────────┤
│ id (PK)          INTEGER                │
│ title            VARCHAR                │
│ author           VARCHAR                │
│ genre            VARCHAR                │
│ isbn             VARCHAR (UNIQUE)       │
│ available        BOOLEAN                │
│ total_copies     INTEGER                │
│ available_copies INTEGER                │
└─────────────────────────────────────────┘
```

---

## 🤖 AI/ML Pipeline

### Recommendation System
```
┌─────────────────────────────────────────────────────┐
│         RECOMMENDATION PIPELINE                     │
└─────────────────────────────────────────────────────┘

Input: member_id
  │
  ├─► Collaborative Filtering
  │     │
  │     ├─► Build user-book matrix (pivot table)
  │     ├─► Calculate cosine similarity
  │     ├─► Find top-5 similar users
  │     ├─► Aggregate their book preferences
  │     └─► Return weighted recommendations
  │
  └─► Content-Based Filtering
        │
        ├─► Analyze member's borrowing history
        ├─► Extract genre preferences
        ├─► Extract author preferences
        ├─► Score available books
        └─► Return top-N matches

Output: Two lists of recommended books
```

### Clustering Pipeline
```
┌─────────────────────────────────────────────────────┐
│           CLUSTERING PIPELINE                       │
└─────────────────────────────────────────────────────┘

Input: All members + transactions
  │
  ├─► Feature Engineering
  │     │
  │     ├─► Total books borrowed
  │     ├─► Total fines accumulated
  │     ├─► Number of returns
  │     └─► Late return count
  │
  ├─► Standardization (StandardScaler)
  │
  ├─► K-Means Clustering (k=4)
  │
  └─► Label Assignment
        │
        ├─► Cluster 0: Casual Readers
        ├─► Cluster 1: Regular Readers
        ├─► Cluster 2: Heavy Readers
        └─► Cluster 3: Late Returners

Output: member_id → cluster_label mapping
```

### Prediction Pipeline
```
┌─────────────────────────────────────────────────────┐
│        LATE RETURN PREDICTION PIPELINE              │
└─────────────────────────────────────────────────────┘

Training Phase:
  Input: Historical transactions
    │
    ├─► Feature Engineering
    │     ├─► Borrow duration
    │     ├─► Member's late rate
    │     └─► Total fines
    │
    ├─► Label: is_late (binary)
    │
    └─► Train Random Forest Classifier

Prediction Phase:
  Input: member_id, borrow_duration
    │
    ├─► Extract member features
    ├─► Create feature vector
    ├─► Model.predict_proba()
    └─► Return probability

Output: Late return probability (0-1)
```

### NLP Search Pipeline
```
┌─────────────────────────────────────────────────────┐
│            NLP SEARCH PIPELINE                      │
└─────────────────────────────────────────────────────┘

Input: Natural language query
  │
  ├─► Encode query using Sentence Transformer
  │     (all-MiniLM-L6-v2)
  │
  ├─► Encode all books (title + author + genre)
  │
  ├─► Calculate cosine similarity
  │     between query and each book
  │
  ├─► Rank by similarity score
  │
  └─► Return top-5 matches

Output: [(book_id, similarity_score), ...]
```

---

## 📦 Module Dependencies

```
app.py
  ├─► library_manager.py
  │     ├─► models.py
  │     │     └─► sqlalchemy
  │     └─► pandas
  │
  ├─► ai_engine.py
  │     ├─► sklearn
  │     ├─► sentence_transformers
  │     ├─► numpy
  │     └─► pandas
  │
  └─► plotly (visualization)

seed_data.py
  └─► library_manager.py

test_system.py
  ├─► library_manager.py
  └─► ai_engine.py

export_utils.py
  └─► library_manager.py
```

---

## 🔐 Security & Validation

### Input Validation
```
User Input
  │
  ├─► Email validation (format check)
  ├─► Required field checks
  ├─► Unique constraint checks (email, ISBN)
  ├─► Borrowing limit validation
  ├─► Availability checks
  └─► Active member validation
```

### Business Rules Enforcement
```
Borrow Request
  │
  ├─► Check: Member is active?
  ├─► Check: Member has < 3 books?
  ├─► Check: Book is available?
  ├─► Check: Valid member & book IDs?
  │
  └─► If all pass → Create transaction
      Else → Return error message
```

---

## 🎨 UI Component Hierarchy

```
Streamlit App
│
├─► Sidebar
│   ├─► Logo/Image
│   ├─► Navigation Menu (Radio buttons)
│   ├─► Quick Stats
│   └─► Version Info
│
└─► Main Content Area
    │
    ├─► Page: Overview
    │   ├─► Metrics Row (4 cards)
    │   ├─► Charts Row (2 columns)
    │   └─► Transactions Table
    │
    ├─► Page: Members
    │   ├─► Tab: View Members
    │   └─► Tab: Add Member
    │
    ├─► Page: Books
    │   ├─► Tab: View Books
    │   └─► Tab: Add Book
    │
    ├─► Page: Transactions
    │   ├─► Tab: Borrow Book
    │   └─► Tab: Return Book
    │
    ├─► Page: AI Insights
    │   ├─► Member Clusters Section
    │   └─► Late Return Predictions Section
    │
    ├─► Page: Recommendations
    │   ├─► Member Selector
    │   ├─► Collaborative Filtering Results
    │   └─► Content-Based Filtering Results
    │
    ├─► Page: NLP Search
    │   ├─► Search Input
    │   └─► Results Table
    │
    └─► Page: Settings
        ├─► Tab: Export Reports
        └─► Tab: System Info
```

---

## 🚀 Performance Considerations

### Caching Strategy
```python
@st.cache_resource
def init_system():
    # Cached: System initialization
    # Reused across sessions
    return LibraryManager(), AIEngine()
```

### Database Optimization
- Indexed columns: id, email, isbn
- Relationship lazy loading
- Efficient queries with filters
- Batch operations where possible

### AI Model Optimization
- Train models only when needed
- Cache embeddings for NLP search
- Vectorized operations with NumPy
- Efficient similarity calculations

---

## 📊 Scalability Path

### Current: Single-User SQLite
```
[User] → [Streamlit] → [SQLite]
```

### Future: Multi-User PostgreSQL
```
[Users] → [Load Balancer] → [Streamlit Instances]
                                    ↓
                            [PostgreSQL Cluster]
```

### Future: Microservices
```
[Frontend] → [API Gateway]
                  ↓
        ┌─────────┼─────────┐
        ↓         ↓         ↓
    [Library] [AI/ML]  [Reports]
    Service   Service  Service
        ↓         ↓         ↓
    [Database] [Model Store] [S3]
```

---

This architecture provides a solid foundation for a production-ready library management system with AI capabilities! 🎯
