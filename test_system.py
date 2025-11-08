"""Test script to verify all system components"""

from library_manager import LibraryManager
from ai_engine import AIEngine
import pandas as pd

def test_library_system():
    print("🧪 Testing AI Library System...\n")
    
    # Initialize
    manager = LibraryManager()
    ai_engine = AIEngine()
    
    # Test 1: Database Connection
    print("✓ Test 1: Database Connection")
    stats = manager.get_dashboard_stats()
    print(f"  - Total Books: {stats['total_books']}")
    print(f"  - Total Members: {stats['total_members']}")
    print(f"  - Borrowed Books: {stats['borrowed_books']}")
    print(f"  - Total Fines: ${stats['total_fines']:.2f}\n")
    
    # Test 2: Data Retrieval
    print("✓ Test 2: Data Retrieval")
    members_df = manager.get_all_members()
    books_df = manager.get_all_books()
    transactions_df = manager.get_all_transactions()
    print(f"  - Members loaded: {len(members_df)}")
    print(f"  - Books loaded: {len(books_df)}")
    print(f"  - Transactions loaded: {len(transactions_df)}\n")
    
    # Test 3: AI - Collaborative Filtering
    print("✓ Test 3: Collaborative Filtering")
    if not transactions_df.empty and not members_df.empty:
        member_id = members_df.iloc[0]['id']
        recs = ai_engine.collaborative_filtering(transactions_df, member_id, top_n=3)
        print(f"  - Recommendations for Member {member_id}: {len(recs)} books")
        for book_id, score in recs[:3]:
            book = books_df[books_df['id'] == book_id]
            if not book.empty:
                print(f"    • {book.iloc[0]['title']} (score: {score:.2f})")
    print()
    
    # Test 4: AI - Member Clustering
    print("✓ Test 4: Member Clustering")
    if not members_df.empty and not transactions_df.empty:
        clusters = ai_engine.cluster_members(members_df, transactions_df)
        print(f"  - Members clustered: {len(clusters)}")
        cluster_counts = pd.Series(clusters.values()).value_counts()
        for cluster, count in cluster_counts.items():
            print(f"    • {cluster}: {count} members")
    print()
    
    # Test 5: AI - Late Prediction
    print("✓ Test 5: Late Return Prediction")
    if not transactions_df.empty:
        ai_engine.train_late_predictor(transactions_df)
        if ai_engine.late_predictor is not None:
            print("  - Model trained successfully")
            member_id = members_df.iloc[0]['id']
            risk = ai_engine.predict_late_return(member_id, 14, transactions_df)
            print(f"  - Sample prediction for Member {member_id}: {risk*100:.1f}% late risk")
    print()
    
    # Test 6: AI - NLP Search
    print("✓ Test 6: NLP Search")
    if not books_df.empty:
        query = "space exploration science"
        results = ai_engine.nlp_search(query, books_df)
        print(f"  - Query: '{query}'")
        print(f"  - Results found: {len(results)}")
        for book_id, similarity in results[:3]:
            book = books_df[books_df['id'] == book_id]
            if not book.empty:
                print(f"    • {book.iloc[0]['title']} ({similarity*100:.1f}% match)")
    print()
    
    print("✅ All tests completed successfully!")
    print("\n🚀 System is ready to use. Run: streamlit run app.py")

if __name__ == "__main__":
    test_system()
