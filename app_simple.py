import streamlit as st
import plotly.express as px
from library_manager import LibraryManager
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Library System", layout="wide")

@st.cache_resource
def init_system():
    return LibraryManager()

manager = init_system()

with st.sidebar:
    st.title("📚 AI Library")
    menu = st.radio("Navigation", 
                    ["📊 Overview", "👥 Members", "📖 Books", "🔄 Transactions"])
    stats = manager.get_dashboard_stats()
    st.metric("Active Members", stats['total_members'])
    st.metric("Total Books", stats['total_books'])

if menu == "📊 Overview":
    st.title("📊 Library Dashboard")
    stats = manager.get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Total Books", stats['total_books'])
    col2.metric("📖 Borrowed", stats['borrowed_books'])
    col3.metric("👥 Active Members", stats['total_members'])
    col4.metric("💰 Fines", f"${stats['total_fines']:.2f}")
    
    st.subheader("📊 Books by Genre")
    books_df = manager.get_all_books()
    if not books_df.empty:
        genre_counts = books_df['genre'].value_counts()
        fig = px.pie(values=genre_counts.values, names=genre_counts.index)
        st.plotly_chart(fig, use_container_width=True)

elif menu == "👥 Members":
    st.title("👥 Members")
    tab1, tab2 = st.tabs(["View", "Add"])
    
    with tab1:
        st.dataframe(manager.get_all_members(), use_container_width=True)
    
    with tab2:
        with st.form("add_member"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            if st.form_submit_button("Add") and name and email:
                try:
                    manager.add_member(name, email)
                    st.success(f"Added {name}!")
                    st.rerun()
                except:
                    st.error("Error adding member")

elif menu == "📖 Books":
    st.title("📖 Books")
    tab1, tab2 = st.tabs(["View", "Add"])
    
    with tab1:
        st.dataframe(manager.get_all_books(), use_container_width=True)
    
    with tab2:
        with st.form("add_book"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            genre = st.selectbox("Genre", ["Science Fiction", "Technology", "History", "Fiction", "Science"])
            isbn = st.text_input("ISBN")
            if st.form_submit_button("Add") and title and author and isbn:
                try:
                    manager.add_book(title, author, genre, isbn, 1)
                    st.success(f"Added {title}!")
                    st.rerun()
                except:
                    st.error("Error adding book")

elif menu == "🔄 Transactions":
    st.title("🔄 Transactions")
    tab1, tab2 = st.tabs(["Borrow", "Return"])
    
    with tab1:
        members_df = manager.get_all_members()
        books_df = manager.get_all_books()
        
        if not members_df.empty and not books_df.empty:
            with st.form("borrow"):
                member = st.selectbox("Member", members_df['id'].tolist(),
                                     format_func=lambda x: members_df[members_df['id']==x]['name'].values[0])
                available = books_df[books_df['available_copies'] > 0]
                book = st.selectbox("Book", available['id'].tolist(),
                                   format_func=lambda x: available[available['id']==x]['title'].values[0])
                
                if st.form_submit_button("Borrow"):
                    success, msg = manager.borrow_book(member, book)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    
    with tab2:
        transactions_df = manager.get_all_transactions()
        active = transactions_df[transactions_df['status'] == 'borrowed']
        
        if not active.empty:
            books_df = manager.get_all_books()
            members_df = manager.get_all_members()
            active = active.merge(books_df[['id', 'title']], left_on='book_id', right_on='id')
            active = active.merge(members_df[['id', 'name']], left_on='member_id', right_on='id')
            
            with st.form("return"):
                trans = st.selectbox("Transaction", active['id_x'].tolist(),
                                    format_func=lambda x: f"{active[active['id_x']==x]['name'].values[0]} - {active[active['id_x']==x]['title'].values[0]}")
                
                if st.form_submit_button("Return"):
                    success, msg = manager.return_book(trans)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
