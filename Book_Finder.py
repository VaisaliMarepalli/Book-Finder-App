#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests

# --- PAGE SETUP ---
st.set_page_config(page_title="Book Finder", layout="centered")

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
        /* Center title and subtitle */
        .title {
            text-align: center;
            font-size: 50px;
            font-weight: 1000;
            margin-bottom: 8px;
        }
        .subtitle {
            text-align: center;
            font-size: 28px;
            font-style: italic;
            color: #555;
            font-weight: 500;
            margin-bottom: 25px;
        }
        /* Search bar section */
        .search-area {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            margin-bottom: 30px;
        }
        /* Book result cards */
        .book-card {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #f8f9fa;
            padding: 14px 20px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 1px 1px 6px rgba(0,0,0,0.1);
        }
        .book-details {
            flex: 1;
        }
        .book-title {
            font-size: 20px;
            font-weight: 700;
            color: #222;
        }
        .book-sub {
            font-size: 16px;
            color: #444;
            margin-top: 2px;
        }
        .book-year {
            font-size: 15px;
            color: #666;
        }
        .read-more {
            text-decoration: none;
            color: #0077cc;
            font-weight: 600;
            transition: 0.2s;
        }
        .read-more:hover {
            color: #004c99;
        }
    </style>
""", unsafe_allow_html=True)

# --- PAGE HEADER ---
st.markdown("<div class='title'>📚 Book Finder</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Welcome to the Book Finder — your digital library adventure!</div>", unsafe_allow_html=True)

# --- SEARCH INPUTS ---
col1, col2 = st.columns([1, 2])

with col1:
    search_type = st.selectbox("Search by", ["Title", "Author"], label_visibility="collapsed")
with col2:
    query = st.text_input("Enter keyword", placeholder=f"Enter {search_type.lower()} name", label_visibility="collapsed")

# Centered search button below inputs
st.markdown("<div style='text-align:center; margin-top:10px;'>", unsafe_allow_html=True)
search = st.button("🔍 Search")
st.markdown("</div>", unsafe_allow_html=True)


# --- FETCH & DISPLAY RESULTS ---
if search and query.strip() != "":
    st.subheader("Search Results:")
    
    # Determine API endpoint based on search type
    if search_type == "Title":
        url = f"https://openlibrary.org/search.json?title={query}"
    else:
        url = f"https://openlibrary.org/search.json?author={query}"

    # Make request
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        books = data.get("docs", [])

        if not books:
            st.warning("No books found. Try another keyword.")
        else:
            for book in books[:10]:
                title = book.get("title", "Unknown Title")
                author = ", ".join(book.get("author_name", ["Unknown Author"]))
                year = book.get("first_publish_year", "N/A")
                key = book.get("key", "#")

                st.markdown(
                    f"""
                    <div class='book-card'>
                        <div class='book-details'>
                            <div class='book-title'>📖 {title}</div>
                            <div class='book-sub'>👤 {author}</div>
                            <div class='book-year'>📅 {year}</div>
                        </div>
                        <a href='https://openlibrary.org{key}' target='_blank' class='read-more'>Read More</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.error("Failed to fetch data from API. Please try again later.")
elif search:
    st.warning("Please enter a keyword before searching.")

