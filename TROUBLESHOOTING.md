# 🔧 Troubleshooting Guide

## Common Issues & Solutions

### Installation Issues

#### ❌ Issue: `pip install` fails
```bash
Error: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with specific Python version
python3 -m pip install -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

#### ❌ Issue: `sentence-transformers` installation fails
```bash
Error: Building wheel for sentence-transformers failed
```

**Solution:**
```bash
# Install build dependencies first
pip install wheel setuptools

# Install PyTorch first (required for sentence-transformers)
pip install torch

# Then install sentence-transformers
pip install sentence-transformers
```

---

### Database Issues

#### ❌ Issue: `OperationalError: no such table`
```bash
sqlalchemy.exc.OperationalError: no such table: members
```

**Solution:**
```bash
# Delete existing database and recreate
rm library.db

# Run seed script to recreate tables
python seed_data.py
```

---

#### ❌ Issue: `IntegrityError: UNIQUE constraint failed`
```bash
IntegrityError: UNIQUE constraint failed: members.email
```

**Solution:**
- Email already exists in database
- Use a different email address
- Or delete the database and reseed:
```bash
rm library.db
python seed_data.py
```

---

#### ❌ Issue: Database locked
```bash
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Close all connections to the database
# Stop the Streamlit app (Ctrl+C)
# Restart the app
streamlit run app.py
```

---

### Streamlit Issues

#### ❌ Issue: `streamlit: command not found`
```bash
bash: streamlit: command not found
```

**Solution:**
```bash
# Ensure streamlit is installed
pip install streamlit

# Or use python module syntax
python -m streamlit run app.py
```

---

#### ❌ Issue: Port already in use
```bash
Error: Port 8501 is already in use
```

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502

# Or kill the process using port 8501
# On Mac/Linux:
lsof -ti:8501 | xargs kill -9

# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

#### ❌ Issue: Page doesn't load / blank screen
```bash
# Browser shows blank page
```

**Solution:**
1. Check terminal for errors
2. Clear browser cache
3. Try incognito/private mode
4. Restart Streamlit:
```bash
# Stop with Ctrl+C
# Restart
streamlit run app.py
```

---

### AI/ML Issues

#### ❌ Issue: Recommendations return empty list
```bash
# No recommendations shown
```

**Solution:**
- Need more transaction data
- Ensure member has borrowed books
- Add more transactions:
```bash
python seed_data.py  # Run again to add more data
```

---

#### ❌ Issue: Late prediction model not training
```bash
# "Not enough data for AI insights"
```

**Solution:**
- Need at least 10 completed transactions
- Run seed script multiple times:
```bash
python seed_data.py
python seed_data.py
python seed_data.py
```

---

#### ❌ Issue: NLP search very slow on first run
```bash
# Takes 30+ seconds on first search
```

**Solution:**
- This is normal! Sentence Transformer downloads model on first use
- Model is cached after first download (~80MB)
- Subsequent searches will be fast
- Wait for initial download to complete

---

#### ❌ Issue: Clustering fails with "n_samples < n_clusters"
```bash
ValueError: n_samples=2 should be >= n_clusters=4
```

**Solution:**
- Need more members in database
- Add more members through UI or seed script
- Or reduce cluster count in config.py:
```python
N_CLUSTERS = 2  # Reduce from 4 to 2
```

---

### Data Issues

#### ❌ Issue: No data showing in tables
```bash
# Tables show "No data available"
```

**Solution:**
```bash
# Run seed script to populate database
python seed_data.py

# Refresh the Streamlit page
```

---

#### ❌ Issue: Can't borrow book - "Maximum 3 books allowed"
```bash
# Member already has 3 books
```

**Solution:**
- Return one of the member's books first
- Or change limit in library_manager.py:
```python
self.max_books_per_member = 5  # Increase from 3
```

---

#### ❌ Issue: Can't borrow book - "Book not available"
```bash
# All copies are borrowed
```

**Solution:**
- Return a copy of that book first
- Or add more copies through "Add Book" with same ISBN
- Or add a new book

---

### Performance Issues

#### ❌ Issue: App is slow / laggy
```bash
# UI takes long to respond
```

**Solution:**
1. Check database size:
```bash
ls -lh library.db
```

2. If database is large (>100MB), consider:
   - Archiving old transactions
   - Optimizing queries
   - Using PostgreSQL instead of SQLite

3. Clear Streamlit cache:
```bash
# In the app, press 'C' then 'Clear cache'
```

---

#### ❌ Issue: High memory usage
```bash
# System running out of memory
```

**Solution:**
- Restart the Streamlit app
- Reduce data size
- Close other applications
- Increase system RAM

---

### Export Issues

#### ❌ Issue: Export button doesn't work
```bash
# Click export but nothing happens
```

**Solution:**
1. Check browser's download settings
2. Allow pop-ups for localhost
3. Try different browser
4. Check console for errors (F12)

---

#### ❌ Issue: Exported CSV is empty
```bash
# CSV file has headers but no data
```

**Solution:**
- No data in database for that export type
- Run seed script:
```bash
python seed_data.py
```

---

## Testing & Verification

### Run System Test
```bash
python test_system.py
```

**Expected Output:**
```
🧪 Testing AI Library System...

✓ Test 1: Database Connection
  - Total Books: 15
  - Total Members: 8
  ...

✅ All tests completed successfully!
```

---

### Verify Installation
```bash
# Check Python version (need 3.8+)
python --version

# Check installed packages
pip list | grep streamlit
pip list | grep scikit-learn
pip list | grep sentence-transformers

# Check database exists
ls -l library.db
```

---

### Reset Everything
```bash
# Complete reset - start fresh
rm library.db
rm -rf __pycache__
rm -rf .streamlit
pip install -r requirements.txt
python seed_data.py
streamlit run app.py
```

---

## Debug Mode

### Enable Streamlit Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

### Check Logs
```bash
# Streamlit logs location
~/.streamlit/logs/

# View latest log
tail -f ~/.streamlit/logs/streamlit.log
```

---

## Getting Help

### Check Documentation
1. README.md - Full documentation
2. QUICKSTART.md - Quick start guide
3. FEATURES.md - Feature list
4. ARCHITECTURE.md - System design

### Verify System Requirements
- Python 3.8 or higher
- 2GB RAM minimum
- 500MB disk space
- Internet connection (for first-time model download)

### Common Commands Reference
```bash
# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_data.py

# Run app
streamlit run app.py

# Test system
python test_system.py

# Reset database
rm library.db && python seed_data.py
```

---

## Still Having Issues?

### Collect Debug Information
```bash
# System info
python --version
pip --version
pip list

# Database info
ls -lh library.db
sqlite3 library.db "SELECT COUNT(*) FROM members;"
sqlite3 library.db "SELECT COUNT(*) FROM books;"
sqlite3 library.db "SELECT COUNT(*) FROM transactions;"

# Streamlit info
streamlit --version
```

### Create Minimal Test
```python
# test_minimal.py
from library_manager import LibraryManager

manager = LibraryManager()
print("✓ LibraryManager initialized")

stats = manager.get_dashboard_stats()
print(f"✓ Stats: {stats}")

print("✅ Basic functionality working!")
```

Run with:
```bash
python test_minimal.py
```

---

## Prevention Tips

### Best Practices
1. ✅ Always use virtual environment
2. ✅ Keep dependencies updated
3. ✅ Backup database regularly
4. ✅ Test after changes
5. ✅ Read error messages carefully

### Regular Maintenance
```bash
# Weekly: Update dependencies
pip install --upgrade -r requirements.txt

# Monthly: Clean cache
rm -rf __pycache__
rm -rf .streamlit/cache

# As needed: Backup database
cp library.db library_backup_$(date +%Y%m%d).db
```

---

**Most issues can be resolved by:**
1. Checking error messages
2. Resetting the database
3. Reinstalling dependencies
4. Restarting the application

Happy troubleshooting! 🔧✨
