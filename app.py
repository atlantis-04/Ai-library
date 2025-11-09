import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from library_manager import LibraryManager
from ai_engine import AIEngine
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="AI Library System", layout="wide", initial_sidebar_state="expanded")

# Midnight Glass Theme - macOS Style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * {font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;}
    .stApp {background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);}
    .main .block-container {background-color: transparent; padding: 2rem;}
    .stButton>button {
        background: rgba(255, 255, 255, 0.08);
        color: #ffffff;
        border-radius: 12px;
        padding: 0.65rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.12);
        font-weight: 600;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    h1, h2, h3 {color: #ffffff; text-shadow: 0 2px 10px rgba(0,0,0,0.5);}
    h1 {font-weight: 700; padding-bottom: 1rem; letter-spacing: -0.5px;}
    h2 {font-weight: 600; padding-top: 0.5rem; letter-spacing: -0.3px;}
    h3 {font-weight: 500; letter-spacing: -0.2px;}
    [data-testid="stMetricValue"] {font-size: 2rem; font-weight: 700; color: #ffffff;}
    [data-testid="stMetricLabel"] {color: rgba(255, 255, 255, 0.7); font-weight: 600;}
    .stMarkdown {color: rgba(255, 255, 255, 0.9);}
    label {color: rgba(255, 255, 255, 0.9) !important; font-weight: 600 !important;}
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    }
    div[data-baseweb="select"] > div {color: #ffffff !important;}
    input, textarea {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    }
    .stRadio > label {display: none !important;}
    .stRadio > div {gap: 6px;}
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        margin: 4px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    }
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        transform: translateX(6px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    }
    .stRadio > div > label > div[data-checked="true"] {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 8px 32px rgba(255,255,255,0.1), inset 0 2px 4px rgba(255,255,255,0.1) !important;
        font-weight: 700 !important;
    }
    .stRadio > div > label > div {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        letter-spacing: 0.2px !important;
    }
    .stDataFrame, .stTable {
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    }
    .stDataFrame > div, .stTable > div {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    .stDataFrame table, .stTable table {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    .stDataFrame thead tr th {
        background: rgba(255, 255, 255, 0.08) !important;
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 16px 12px !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }
    .stDataFrame tbody tr {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    .stDataFrame tbody tr:hover {
        background-color: rgba(255, 255, 255, 0.06) !important;
        transform: scale(1.005) !important;
        box-shadow: 0 4px 16px rgba(255,255,255,0.05) !important;
    }
    .stDataFrame tbody tr td {
        color: rgba(255, 255, 255, 0.9) !important;
        padding: 14px 12px !important;
        font-weight: 500 !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 6px;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
    }
    .stTabs [data-baseweb="tab"] {color: rgba(255, 255, 255, 0.6) !important; background-color: transparent;}
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 8px;
    }
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
    }
    .stAlert {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
@st.cache_resource
def init_system():
    return LibraryManager(), AIEngine()

manager, ai_engine = init_system()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 20px 10px 20px;'>
        <div style='font-size: 70px; margin-bottom: 10px;'>📚</div>
        <h2 style='color: white; margin: 0; font-size: 24px; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);'>AI Library</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("Navigation", 
                    ["📊 Overview", "👥 Members", "📖 Books", "🔄 Transactions", 
                     "🤖 AI Insights", "💡 Recommendations", "🔍 NLP Search", "⚙️ Settings"],
                    label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    stats = manager.get_dashboard_stats()
    st.metric("Active Members", stats['total_members'])
    st.metric("Total Books", stats['total_books'])
    st.markdown("---")
    st.markdown("**Version:** 1.0.0")

# Main Content
if menu == "📊 Overview":
    st.title("📊 Library Dashboard")
    
    stats = manager.get_dashboard_stats()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Books", stats['total_books'], delta=None)
    with col2:
        st.metric("📖 Borrowed", stats['borrowed_books'], delta=None)
    with col3:
        st.metric("👥 Active Members", stats['total_members'], delta=None)
    with col4:
        st.metric("💰 Fines Collected", f"${stats['total_fines']:.2f}", delta=None)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Borrowing Trends")
        transactions_df = manager.get_all_transactions()
        if not transactions_df.empty:
            transactions_df['borrow_date'] = pd.to_datetime(transactions_df['borrow_date'])
            daily_borrows = transactions_df.groupby(transactions_df['borrow_date'].dt.date).size().reset_index()
            daily_borrows.columns = ['Date', 'Count']
            fig = px.line(daily_borrows, x='Date', y='Count', markers=True)
            fig.update_layout(height=300, plot_bgcolor='rgba(255,255,255,0.02)', paper_bgcolor='rgba(255,255,255,0.02)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No transaction data available")
    
    with col2:
        st.subheader("📊 Books by Genre")
        books_df = manager.get_all_books()
        if not books_df.empty:
            genre_counts = books_df['genre'].value_counts()
            fig = px.pie(values=genre_counts.values, names=genre_counts.index, hole=0.4)
            fig.update_layout(height=300, plot_bgcolor='rgba(255,255,255,0.02)', paper_bgcolor='rgba(255,255,255,0.02)', font=dict(color='white'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No books available")
    
    st.markdown("---")
    
    # Recent Transactions
    st.subheader("🔄 Recent Transactions")
    if not transactions_df.empty:
        recent = transactions_df.sort_values('borrow_date', ascending=False).head(10)
        books_df = manager.get_all_books()
        members_df = manager.get_all_members()
        
        recent = recent.merge(books_df[['id', 'title']], left_on='book_id', right_on='id', how='left')
        recent = recent.merge(members_df[['id', 'name']], left_on='member_id', right_on='id', how='left')
        
        display_cols = ['name', 'title', 'borrow_date', 'due_date', 'status', 'fine']
        st.dataframe(recent[display_cols].rename(columns={
            'name': 'Member', 'title': 'Book', 'borrow_date': 'Borrowed', 
            'due_date': 'Due Date', 'status': 'Status', 'fine': 'Fine ($)'
        }), use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet")

elif menu == "👥 Members":
    st.title("👥 Member Management")
    
    tab1, tab2 = st.tabs(["View Members", "Add Member"])
    
    with tab1:
        members_df = manager.get_all_members()
        if not members_df.empty:
            st.dataframe(members_df, use_container_width=True, hide_index=True)
        else:
            st.info("No members registered")
    
    with tab2:
        with st.form("add_member"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            submit = st.form_submit_button("Add Member")
            
            if submit and name and email:
                try:
                    manager.add_member(name, email)
                    st.success(f"Member {name} added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif menu == "📖 Books":
    st.title("📖 Book Management")
    
    tab1, tab2 = st.tabs(["View Books", "Add Book"])
    
    with tab1:
        books_df = manager.get_all_books()
        if not books_df.empty:
            st.dataframe(books_df, use_container_width=True, hide_index=True)
        else:
            st.info("No books in library")
    
    with tab2:
        with st.form("add_book"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            genre = st.selectbox("Genre", ["Science Fiction", "Technology", "History", 
                                          "Fiction", "Science", "Biography", "Self-Help", 
                                          "Design", "Psychology", "Business"])
            isbn = st.text_input("ISBN")
            copies = st.number_input("Number of Copies", min_value=1, value=1)
            submit = st.form_submit_button("Add Book")
            
            if submit and title and author and isbn:
                try:
                    manager.add_book(title, author, genre, isbn, copies)
                    st.success(f"Book '{title}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif menu == "🔄 Transactions":
    st.title("🔄 Transaction Management")
    
    tab1, tab2 = st.tabs(["Borrow Book", "Return Book"])
    
    with tab1:
        members_df = manager.get_all_members()
        books_df = manager.get_all_books()
        
        if not members_df.empty and not books_df.empty:
            with st.form("borrow_book"):
                member = st.selectbox("Select Member", 
                                     options=members_df['id'].tolist(),
                                     format_func=lambda x: members_df[members_df['id']==x]['name'].values[0])
                
                available_books = books_df[books_df['available_copies'] > 0]
                book = st.selectbox("Select Book",
                                   options=available_books['id'].tolist(),
                                   format_func=lambda x: available_books[available_books['id']==x]['title'].values[0])
                
                submit = st.form_submit_button("Borrow Book")
                
                if submit:
                    success, msg = manager.borrow_book(member, book)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.warning("Add members and books first")
    
    with tab2:
        transactions_df = manager.get_all_transactions()
        active_trans = transactions_df[transactions_df['status'] == 'borrowed']
        
        if not active_trans.empty:
            books_df = manager.get_all_books()
            members_df = manager.get_all_members()
            
            active_trans = active_trans.merge(books_df[['id', 'title']], 
                                             left_on='book_id', right_on='id', how='left')
            active_trans = active_trans.merge(members_df[['id', 'name']], 
                                             left_on='member_id', right_on='id', how='left')
            
            with st.form("return_book"):
                trans = st.selectbox("Select Transaction",
                                    options=active_trans['id_x'].tolist(),
                                    format_func=lambda x: f"{active_trans[active_trans['id_x']==x]['name'].values[0]} - {active_trans[active_trans['id_x']==x]['title'].values[0]}")
                
                submit = st.form_submit_button("Return Book")
                
                if submit:
                    success, msg = manager.return_book(trans)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("No active borrowings")

elif menu == "🤖 AI Insights":
    st.title("🤖 AI-Powered Insights")
    
    members_df = manager.get_all_members()
    transactions_df = manager.get_all_transactions()
    
    if not transactions_df.empty:
        # Train late predictor
        ai_engine.train_late_predictor(transactions_df)
        
        # Member Clustering
        st.subheader("👥 Member Clusters")
        clusters = ai_engine.cluster_members(members_df, transactions_df)
        
        if clusters:
            cluster_df = pd.DataFrame(list(clusters.items()), columns=['Member ID', 'Cluster'])
            cluster_df = cluster_df.merge(members_df[['id', 'name']], 
                                         left_on='Member ID', right_on='id', how='left')
            
            col1, col2 = st.columns(2)
            with col1:
                cluster_counts = cluster_df['Cluster'].value_counts()
                fig = px.bar(x=cluster_counts.index, y=cluster_counts.values,
                           labels={'x': 'Cluster', 'y': 'Count'})
                fig.update_layout(plot_bgcolor='rgba(255,255,255,0.02)', paper_bgcolor='rgba(255,255,255,0.02)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(cluster_df[['name', 'Cluster']], 
                           use_container_width=True, hide_index=True)
        
        # Late Return Predictions
        st.subheader("⚠️ Late Return Risk Analysis")
        active_trans = transactions_df[transactions_df['status'] == 'borrowed']
        
        if not active_trans.empty:
            predictions = []
            for _, trans in active_trans.iterrows():
                duration = (pd.to_datetime(trans['due_date']) - pd.to_datetime(trans['borrow_date'])).days
                risk = ai_engine.predict_late_return(trans['member_id'], duration, transactions_df)
                predictions.append({
                    'Transaction ID': trans['id'],
                    'Member ID': trans['member_id'],
                    'Late Risk': f"{risk*100:.1f}%",
                    'Risk Level': 'High' if risk > 0.7 else 'Medium' if risk > 0.4 else 'Low'
                })
            
            if predictions:
                pred_df = pd.DataFrame(predictions)
                pred_df = pred_df.merge(members_df[['id', 'name']], 
                                       left_on='Member ID', right_on='id', how='left')
                
                st.dataframe(pred_df[['name', 'Late Risk', 'Risk Level']], 
                            use_container_width=True, hide_index=True)
            else:
                st.info("No active transactions to analyze.")
    else:
        st.info("Not enough data for AI insights. Add more transactions.")

elif menu == "💡 Recommendations":
    st.title("💡 Book Recommendations")
    
    members_df = manager.get_all_members()
    books_df = manager.get_all_books()
    transactions_df = manager.get_all_transactions()
    
    if not members_df.empty and not books_df.empty:
        member_id = st.selectbox("Select Member",
                                options=members_df['id'].tolist(),
                                format_func=lambda x: members_df[members_df['id']==x]['name'].values[0])
        
        if st.button("Generate Recommendations"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🤝 Collaborative Filtering")
                collab_recs = ai_engine.collaborative_filtering(transactions_df, member_id)
                
                if collab_recs:
                    rec_books = []
                    for book_id, score in collab_recs:
                        book = books_df[books_df['id'] == book_id]
                        if not book.empty:
                            rec_books.append({
                                'Title': book.iloc[0]['title'],
                                'Author': book.iloc[0]['author'],
                                'Score': f"{score:.2f}"
                            })
                    st.dataframe(pd.DataFrame(rec_books), use_container_width=True, hide_index=True)
                else:
                    st.info("No recommendations available")
            
            with col2:
                st.subheader("📚 Content-Based Filtering")
                member_trans = transactions_df[transactions_df['member_id'] == member_id]
                member_trans = member_trans.merge(books_df, left_on='book_id', right_on='id', how='left')
                
                content_recs = ai_engine.content_based_filtering(books_df, member_trans)
                
                if content_recs:
                    rec_books = []
                    for book_id, score in content_recs:
                        book = books_df[books_df['id'] == book_id]
                        if not book.empty:
                            rec_books.append({
                                'Title': book.iloc[0]['title'],
                                'Author': book.iloc[0]['author'],
                                'Genre': book.iloc[0]['genre']
                            })
                    st.dataframe(pd.DataFrame(rec_books), use_container_width=True, hide_index=True)
                else:
                    st.info("No recommendations available")
    else:
        st.warning("Add members and books first")

elif menu == "🔍 NLP Search":
    st.title("🔍 Natural Language Search")
    
    st.markdown("Search for books using natural language queries like:")
    st.markdown("- *'books about space exploration'*")
    st.markdown("- *'technology and programming'*")
    st.markdown("- *'self improvement and habits'*")
    
    query = st.text_input("Enter your search query:")
    
    if query:
        books_df = manager.get_all_books()
        
        if not books_df.empty:
            results = ai_engine.nlp_search(query, books_df)
            
            if results:
                result_books = []
                for book_id, similarity in results:
                    if similarity > 0.0:
                        book = books_df[books_df['id'] == book_id]
                        if not book.empty:
                            result_books.append({
                                'Title': book.iloc[0]['title'],
                                'Author': book.iloc[0]['author'],
                                'Genre': book.iloc[0]['genre'],
                                'Relevance': f"{similarity*100:.1f}%",
                                'Available': '✅' if book.iloc[0]['available'] else '❌'
                            })
                
                if result_books:
                    st.dataframe(pd.DataFrame(result_books), use_container_width=True, hide_index=True)
                else:
                    st.info("No matching books found")
            else:
                st.info("No matching books found")
        else:
            st.warning("No books in library")

elif menu == "⚙️ Settings":
    st.title("⚙️ Settings & Reports")
    
    tab1, tab2 = st.tabs(["Export Reports", "System Info"])
    
    with tab1:
        st.subheader("📊 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Members"):
                members_df = manager.get_all_members()
                csv = members_df.to_csv(index=False)
                st.download_button(
                    label="Download Members CSV",
                    data=csv,
                    file_name=f"members_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📥 Export Books"):
                books_df = manager.get_all_books()
                csv = books_df.to_csv(index=False)
                st.download_button(
                    label="Download Books CSV",
                    data=csv,
                    file_name=f"books_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📥 Export Transactions"):
                transactions_df = manager.get_all_transactions()
                csv = transactions_df.to_csv(index=False)
                st.download_button(
                    label="Download Transactions CSV",
                    data=csv,
                    file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📥 Export Overdue Books"):
                transactions_df = manager.get_all_transactions()
                overdue = transactions_df[
                    (transactions_df['status'] == 'borrowed') & 
                    (pd.to_datetime(transactions_df['due_date']) < datetime.now())
                ]
                if not overdue.empty:
                    csv = overdue.to_csv(index=False)
                    st.download_button(
                        label="Download Overdue CSV",
                        data=csv,
                        file_name=f"overdue_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No overdue books")
    
    with tab2:
        st.subheader("ℹ️ System Information")
        
        stats = manager.get_dashboard_stats()
        
        st.markdown(f"""
        **Library Statistics:**
        - Total Books: {stats['total_books']}
        - Total Members: {stats['total_members']}
        - Currently Borrowed: {stats['borrowed_books']}
        - Total Fines Collected: ${stats['total_fines']:.2f}
        
        **System Configuration:**
        - Fine per Day: ${manager.fine_per_day}
        - Max Borrow Days: {manager.max_borrow_days}
        - Max Books per Member: {manager.max_books_per_member}
        
        **AI Features:**
        - ✅ Collaborative Filtering
        - ✅ Content-Based Filtering
        - ✅ Member Clustering (K-Means)
        - ✅ Late Return Prediction (Random Forest)
        - ✅ NLP Search (Sentence Transformers)
        
        **Version:** 1.0.0
        """)
