import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pickle
import os

class AIEngine:
    def __init__(self):
        self.nlp_model = None
        self.late_predictor = RandomForestClassifier(n_estimators=10, random_state=42)
        self.late_predictor.fit([[14, 0.0, 0.0], [7, 0.5, 10.0]], [0, 1])
        self.scaler = StandardScaler()
        
    def collaborative_filtering(self, transactions_df, member_id, top_n=5):
        """Recommend books based on similar users' borrowing patterns"""
        if transactions_df.empty:
            return []
        
        user_book_matrix = transactions_df.pivot_table(
            index='member_id', columns='book_id', aggfunc='size', fill_value=0
        )
        
        if member_id not in user_book_matrix.index:
            return []
        
        user_similarity = cosine_similarity(user_book_matrix)
        user_idx = list(user_book_matrix.index).index(member_id)
        similar_users = user_similarity[user_idx].argsort()[-6:-1][::-1]
        
        borrowed_books = set(user_book_matrix.loc[member_id][user_book_matrix.loc[member_id] > 0].index)
        recommendations = defaultdict(float)
        
        for sim_user_idx in similar_users:
            sim_user_id = user_book_matrix.index[sim_user_idx]
            sim_score = user_similarity[user_idx][sim_user_idx]
            user_books = user_book_matrix.loc[sim_user_id]
            
            for book_id, count in user_books.items():
                if count > 0 and book_id not in borrowed_books:
                    recommendations[book_id] += sim_score * count
        
        return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def content_based_filtering(self, books_df, member_transactions, top_n=5):
        """Recommend books based on user's genre/author preferences"""
        if member_transactions.empty or books_df.empty:
            return []
        
        user_genres = member_transactions['genre'].value_counts().to_dict()
        user_authors = member_transactions['author'].value_counts().to_dict()
        
        borrowed_books = set(member_transactions['book_id'].unique())
        available_books = books_df[~books_df['id'].isin(borrowed_books)]
        
        scores = []
        for _, book in available_books.iterrows():
            score = user_genres.get(book['genre'], 0) * 2 + user_authors.get(book['author'], 0)
            scores.append((book['id'], score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]
    
    def cluster_members(self, members_df, transactions_df, n_clusters=4):
        """Cluster members by reading habits"""
        if members_df.empty or transactions_df.empty:
            return {}
        
        member_features = []
        member_ids = []
        
        for member_id in members_df['id']:
            member_trans = transactions_df[transactions_df['member_id'] == member_id]
            
            features = [
                len(member_trans),
                member_trans['fine'].sum(),
                len(member_trans[member_trans['status'] == 'returned']),
                len(member_trans[member_trans['return_date'].notna() & 
                    (member_trans['return_date'] > member_trans['due_date'])])
            ]
            member_features.append(features)
            member_ids.append(member_id)
        
        if len(member_features) < n_clusters:
            n_clusters = max(1, len(member_features))
        
        X = self.scaler.fit_transform(member_features)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X)
        
        cluster_labels = ['Casual Readers', 'Regular Readers', 'Heavy Readers', 'Late Returners']
        return {member_ids[i]: cluster_labels[clusters[i] % len(cluster_labels)] for i in range(len(member_ids))}
    
    def train_late_predictor(self, transactions_df):
        """Train model to predict late returns"""
        if transactions_df.empty:
            # Create a dummy model with minimal data
            X = np.array([[14, 0.0, 0.0], [7, 0.5, 10.0]])
            y = np.array([0, 1])
            self.late_predictor = RandomForestClassifier(n_estimators=10, random_state=42)
            self.late_predictor.fit(X, y)
            return
        
        completed = transactions_df[transactions_df['return_date'].notna()].copy()
        if completed.empty or len(completed) < 2:
            # Create a dummy model with minimal data
            X = np.array([[14, 0.0, 0.0], [7, 0.5, 10.0]])
            y = np.array([0, 1])
            self.late_predictor = RandomForestClassifier(n_estimators=10, random_state=42)
            self.late_predictor.fit(X, y)
            return
        
        completed['is_late'] = (completed['return_date'] > completed['due_date']).astype(int)
        completed['borrow_duration'] = (completed['due_date'] - completed['borrow_date']).dt.days
        
        member_stats = completed.groupby('member_id').agg({
            'is_late': 'mean',
            'fine': 'sum'
        }).reset_index()
        member_stats.columns = ['member_id', 'late_rate', 'total_fines']
        
        completed = completed.merge(member_stats, on='member_id', how='left')
        
        features = ['borrow_duration', 'late_rate', 'total_fines']
        X = completed[features].fillna(0)
        y = completed['is_late']
        
        # Ensure we have at least 2 samples and both classes
        if len(X) < 2 or len(np.unique(y)) < 2:
            # Add dummy samples to ensure model can be trained
            X = np.vstack([X.values, [[14, 0.0, 0.0], [7, 0.5, 10.0]]])
            y = np.concatenate([y.values, [0, 1]])
        
        self.late_predictor = RandomForestClassifier(n_estimators=50, random_state=42)
        self.late_predictor.fit(X, y)
    
    def predict_late_return(self, member_id, borrow_duration, transactions_df):
        """Predict if a member will return late"""
        try:
            if not hasattr(self, 'late_predictor') or self.late_predictor is None:
                return 0.5
            
            member_trans = transactions_df[
                (transactions_df['member_id'] == member_id) & 
                (transactions_df['return_date'].notna())
            ]
            
            if member_trans.empty:
                late_rate = 0.0
                total_fines = 0.0
            else:
                late_rate = ((member_trans['return_date'] > member_trans['due_date']).sum() / len(member_trans))
                total_fines = member_trans['fine'].sum()
            
            features = np.array([[borrow_duration, late_rate, total_fines]])
            proba = self.late_predictor.predict_proba(features)
            
            if len(proba) > 0 and len(proba[0]) > 1:
                return float(proba[0][1])
            return 0.5
        except Exception:
            return 0.5
    
    def nlp_search(self, query, books_df):
        """Search books using TF-IDF (lightweight NLP)"""
        if books_df.empty:
            return []
        
        book_texts = (books_df['title'] + ' ' + books_df['author'] + ' ' + books_df['genre']).tolist()
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(book_texts + [query])
        
        query_vec = tfidf_matrix[-1]
        book_vecs = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(query_vec, book_vecs)[0]
        top_indices = similarities.argsort()[-5:][::-1]
        
        return [(books_df.iloc[i]['id'], similarities[i]) for i in top_indices]
