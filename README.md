# 📚 AI-Powered Library Book Allocation System

> A complete, production-ready library management system with AI-powered features including book recommendations, member clustering, late return prediction, and natural language search.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Quick Start

```bash
./setup.sh
streamlit run app.py
```

**📖 New here? Start with [QUICKSTART.md](QUICKSTART.md)**

---

## 🎯 Features

### Core Library Management
- ✅ Member registration and management
- ✅ Book inventory management
- ✅ Borrow and return tracking
- ✅ Automatic fine calculation for late returns
- ✅ Transaction history logging

### 🤖 AI-Powered Features
1. **Book Recommendation System**
   - Collaborative Filtering (based on similar users)
   - Content-Based Filtering (based on genres/authors)

2. **Member Clustering**
   - Groups members by reading habits using K-Means
   - Categories: Casual Readers, Regular Readers, Heavy Readers, Late Returners

3. **Late Return Prediction**
   - Random Forest classifier predicts late return probability
   - Risk levels: High, Medium, Low

4. **Natural Language Search**
   - Semantic search using sentence transformers
   - Query examples: "books about space exploration", "technology and programming"

### 📊 Analytics Dashboard
- Real-time statistics (total books, borrowed books, active members, fines)
- Borrowing trends visualization
- Genre distribution charts
- Recent transactions table
- AI insights and predictions

## 🚀 Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Initialize database with sample data:**
```bash
python seed_data.py
```

3. **Run the application:**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
PythonProject1/
├── app.py                 # Main Streamlit dashboard
├── models.py              # SQLAlchemy database models
├── library_manager.py     # Core business logic
├── ai_engine.py          # AI/ML models and algorithms
├── seed_data.py          # Database seeding script
├── requirements.txt      # Python dependencies
├── library.db           # SQLite database (auto-created)
└── README.md            # This file
```

## 🎨 UI Navigation

- **📊 Overview**: Dashboard with stats and charts
- **👥 Members**: View and add library members
- **📖 Books**: Manage book inventory
- **🔄 Transactions**: Borrow and return books
- **🤖 AI Insights**: Member clusters and late return predictions
- **💡 Recommendations**: Personalized book suggestions
- **🔍 NLP Search**: Natural language book search

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Streamlit
- **AI/ML**: Scikit-learn, Sentence Transformers
- **Visualization**: Plotly, Pandas

## 📝 Usage Examples

### Add a Member
1. Navigate to "👥 Members"
2. Click "Add Member" tab
3. Enter name and email
4. Click "Add Member"

### Borrow a Book
1. Navigate to "🔄 Transactions"
2. Select member and book
3. Click "Borrow Book"
4. Book is automatically due in 14 days

### Get Recommendations
1. Navigate to "💡 Recommendations"
2. Select a member
3. Click "Generate Recommendations"
4. View collaborative and content-based suggestions

### Search with NLP
1. Navigate to "🔍 NLP Search"
2. Enter natural language query
3. View semantically matched books

## ⚙️ Configuration

Edit `library_manager.py` to customize:
- `fine_per_day`: Fine amount per day (default: $2.00)
- `max_borrow_days`: Loan period (default: 14 days)
- `max_books_per_member`: Borrowing limit (default: 3 books)

## 🔮 Future Enhancements

- [ ] PDF/Excel report export
- [ ] Email notifications for due dates
- [ ] REST API for mobile app
- [ ] Chatbot assistant
- [ ] Sentiment analysis on reviews
- [ ] Multi-library support

## 📄 License

MIT License - Feel free to use and modify!

## 👨‍💻 Author

Built with ❤️ using Python, Streamlit, and AI/ML
