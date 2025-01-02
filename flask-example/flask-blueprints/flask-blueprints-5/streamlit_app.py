import streamlit as st
from itsdangerous import URLSafeTimedSerializer

st.set_page_config(
    page_title="My App",
    page_icon="pc.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Welcome to My App")
st.sidebar.title("Sidebar")

# ফ্লাস্ক অ্যাপ্লিকেশনের সিক্রেট কী
secret_key = "supersekrit"

def verify_token(token):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        user_id = serializer.loads(token, salt=secret_key)
        return user_id
    except:
        return None

# URL থেকে টোকেন পড়ুন
query_params = st.experimental_get_query_params()
token = query_params.get("token", [None])[0]

if token:
    user_id = verify_token(token)
    if user_id:
        st.success("Login successful!")
        st.write(f"Welcome, user ID: {user_id}")
    else:
        st.error("Invalid or expired token.")
else:
    st.error("No token provided.")