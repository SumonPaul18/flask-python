import streamlit as st

# ফুল স্ক্রিন লেআউট সেট করুন
st.set_page_config(page_title="My Streamlit App", layout="wide")

# লোগো হেডার
st.markdown("""
    <style>
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }
        .header img {
            height: 50px;
        }
        .header .search-bar {
            flex-grow: 1;
            margin: 0 20px;
        }
        .header .profile {
            display: flex;
            align-items: center;
        }
        .header .profile img {
            height: 40px;
            border-radius: 50%;
            margin-left: 10px;
        }
    </style>
    <div class="header">
        <img src="https://via.placeholder.com/50" alt="Logo">
        <input type="text" class="search-bar" placeholder="Search...">
        <div class="profile">
            <span>Username</span>
            <img src="https://via.placeholder.com/40" alt="Profile">
        </div>
    </div>
""", unsafe_allow_html=True)

# সাইডবার সহ সাবমেনু
with st.sidebar:
    st.image("https://via.placeholder.com/150", use_column_width=True)
    st.title("Navigation")
    menu = st.selectbox("Menu", ["Home", "Features", "Pricing", "About"])
    if menu == "Home":
        st.write("Welcome to the Home page!")
    elif menu == "Features":
        st.write("Here are our features.")
    elif menu == "Pricing":
        st.write("Check out our pricing plans.")
    elif menu == "About":
        st.write("Learn more about us.")

# মূল কন্টেন্ট
st.write("This is the main content area.")