"""Configuration settings for the library system"""

# Library Settings
FINE_PER_DAY = 2.0
MAX_BORROW_DAYS = 14
MAX_BOOKS_PER_MEMBER = 3

# AI Model Settings
N_CLUSTERS = 4
RECOMMENDATION_COUNT = 5
LATE_PREDICTION_THRESHOLD = 0.7

# Database
DATABASE_URL = 'sqlite:///library.db'

# UI Settings
PAGE_TITLE = "AI Library System"
SIDEBAR_WIDTH = 250

# Cluster Labels
CLUSTER_LABELS = [
    'Casual Readers',
    'Regular Readers', 
    'Heavy Readers',
    'Late Returners'
]

# Book Genres
GENRES = [
    "Science Fiction",
    "Technology",
    "History",
    "Fiction",
    "Science",
    "Biography",
    "Self-Help",
    "Design",
    "Psychology",
    "Business",
    "Fantasy",
    "Mystery",
    "Romance",
    "Thriller"
]
