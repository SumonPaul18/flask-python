import streamlit as st
from urllib.parse import urlparse, parse_qs

st.set_page_config(layout="wide")  # Full screen layout

# Custom CSS for Google Console style navbar and sidebar
st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #202124;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #e0e0e0;
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 1000;
        color: white;
    }
    .navbar-logo {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .navbar-toggle {
        cursor: pointer;
        font-size: 1.5rem;
    }
    .navbar-icons {
        display: flex;
        align-items: center;
    }
    .navbar-icons > * {
        margin-left: 1rem;
    }
    .stApp {
        margin-top: 60px;
    }
    .sidebar {
        position: fixed;
        top: 60px;
        left: 0;
        width: 250px;
        height: 100%;
        background-color: #202124;
        color: white;
        padding: 1rem;
        display: none;
    }
    .sidebar a {
        color: white;
        text-decoration: none;
        display: block;
        padding: 0.5rem 0;
    }
    .sidebar a:hover {
        background-color: #575757;
    }
    </style>
    <div class="navbar">
        <div class="navbar-logo">MyApp</div>
        <div class="navbar-toggle" onclick="toggleSidebar()">&#9776;</div>
        <div class="navbar-icons">
            <input type="text" placeholder="Search..." style="padding: 0.5rem; border-radius: 4px; border: none;">
            <div class="navbar-icon">&#128187;</div> <!-- Terminal icon -->
            <div class="navbar-icon">&#128100;</div> <!-- User profile icon -->
        </div>
    </div>
    <div class="sidebar" id="sidebar">
        <a href="#">Home</a>
        <a href="#">User Info</a>
        <a href="#">Logout</a>
    </div>
    <script>
    function toggleSidebar() {
        var sidebar = document.getElementById('sidebar');
        if (sidebar.style.display === 'none' || sidebar.style.display === '') {
            sidebar.style.display = 'block';
        } else {
            sidebar.style.display = 'none';
        }
    }
    </script>
""", unsafe_allow_html=True)

st.title('Welcome to Streamlit App')

query_params = st.query_params
if 'user' in query_params:
    st.session_state['user'] = query_params['user'][0]

if 'user' not in st.session_state:
    st.write('Please log in through the Flask app.')
else:
    page = st.sidebar.radio("Go to", ["Home", "User Info", "Logout"])

    if page == "Home":
        st.write(f'Welcome User {st.session_state["user"]}')
    elif page == "User Info":
        st.write("User Information Page")
        st.write(f'User ID: {st.session_state["user"]}')
    elif page == "Logout":
        st.session_state.clear()
        st.write("You have been logged out. Redirecting to login page...")
        st.markdown('<meta http-equiv="refresh" content="0; url=http://localhost:5000">', unsafe_allow_html=True)

# Logout button in the main area
if st.button('Logout'):
    st.session_state.clear()
    st.write("You have been logged out. Redirecting to login page...")
    st.markdown('<meta http-equiv="refresh" content="0; url=http://localhost:5000">', unsafe_allow_html=True)