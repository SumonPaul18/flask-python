import streamlit as st
from urllib.parse import urlparse, parse_qs

st.set_page_config(layout="wide")  # Full screen layout

# Custom CSS for navbar and collapsible sidebar
st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f8f9fa;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #e0e0e0;
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 1000;
    }
    .navbar-logo {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .navbar-toggle {
        cursor: pointer;
        font-size: 1.5rem;
    }
    </style>
    <div class="navbar">
        <div class="navbar-logo">MyApp</div>
        <div class="navbar-toggle" onclick="toggleSidebar()">☰</div>
    </div>
    <script>
    function toggleSidebar() {
        var sidebar = document.querySelector('.css-1d391kg');
        if (sidebar.style.display === 'none') {
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
    st.sidebar.title("Navigation")
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