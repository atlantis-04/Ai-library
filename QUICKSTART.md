# 🚀 Quick Start Guide

## Installation (3 steps)

### Option 1: Automated Setup
```bash
./setup.sh
streamlit run app.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed database
python seed_data.py

# 3. Run application
streamlit run app.py
```

## First Time Usage

The application will open in your browser at `http://localhost:8501`

### Pre-loaded Sample Data
- **8 Members**: Alice, Bob, Carol, David, Emma, Frank, Grace, Henry
- **15 Books**: Mix of Science Fiction, Technology, History, etc.
- **~30 Transactions**: Sample borrowing history

### Try These Features

1. **📊 Overview Dashboard**
   - View library statistics
   - See borrowing trends chart
   - Check genre distribution

2. **🤖 AI Insights**
   - View member clusters (Casual/Regular/Heavy Readers)
   - Check late return risk predictions

3. **💡 Recommendations**
   - Select any member
   - Get personalized book suggestions
   - See both collaborative and content-based recommendations

4. **🔍 NLP Search**
   - Try: "books about space exploration"
   - Try: "technology and programming"
   - Try: "self improvement"

5. **🔄 Borrow/Return**
   - Borrow a book for any member
   - Return books and see automatic fine calculation

## Key Features to Explore

✅ **Real-time Dashboard** - Live stats and charts
✅ **Smart Recommendations** - AI-powered suggestions
✅ **Member Clustering** - Automatic reader categorization
✅ **Late Prediction** - ML model predicts late returns
✅ **NLP Search** - Natural language book search
✅ **Auto Fines** - $2/day for late returns

## Troubleshooting

**Issue**: Module not found
```bash
pip install -r requirements.txt
```

**Issue**: Database error
```bash
rm library.db
python seed_data.py
```

**Issue**: Port already in use
```bash
streamlit run app.py --server.port 8502
```

## Next Steps

- Add your own books and members
- Customize fine rates in `library_manager.py`
- Explore AI insights with more data
- Export reports (coming soon)

Enjoy your AI-powered library! 📚🤖
