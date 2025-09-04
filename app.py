
import streamlit as st
import requests
import json
import os
import plotly.graph_objects as go
import plotly.express as px
from streamlit_lottie import st_lottie

# Set page configuration
st.set_page_config(
    page_title="AI Virtual Stylist",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie animation safely with requests
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.error(f"Error loading Lottie: {e}")
    return None

# Load animations
lottie_robot = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_touohxv0.json")
lottie_fashion = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_V9t630.json")

# API URL (will be replaced by ngrok URL)
api_url = os.getenv("BACKEND_URL", "http://localhost:8000/recommend")

# Custom CSS
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Color indicator style */
    .color-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    /* Card style */
    .item-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("👗 AI Virtual Stylist")
st.write("Personalized outfit recommendations based on your body shape, style, and event.")

# Sidebar input form
st.sidebar.header("Customize Your Outfit")
body_shape = st.sidebar.selectbox("Choose Body Shape", ["apple", "pear", "hourglass", "rectangle", "inverted_triangle"])
personal_style = st.sidebar.selectbox("Choose Personal Style", ["casual", "formal", "bohemian", "sporty", "classic", "trendy"])
event_type = st.sidebar.selectbox("Choose Event Type", ["work", "party", "date", "casual outing", "wedding", "interview"])
budget = st.sidebar.slider("Budget ($)", 20, 500, 150)
exclude_colors = st.sidebar.multiselect("Exclude Colors", ["black", "white", "blue", "red", "green", "yellow", "purple", "pink", "brown", "gray"])

# Button to get recommendations
if st.sidebar.button("Get Recommendations"):
    with st.spinner("Finding your perfect outfit..."):
        payload = {
            "body_shape": body_shape,
            "personal_style": personal_style,
            "event_type": event_type,
            "budget": budget,
            "exclude_colors": exclude_colors
        }
        try:
            response = requests.post(api_url, json=payload, timeout=30)
            if response.status_code == 200:
                rec = response.json()
                st.subheader("✨ Outfit Recommendation")
                st.markdown(f"**Overall Compatibility:** {rec['overall_compatibility']:.2f}")
                st.markdown(f"**Message:** {rec['message']}")
                
                # Display outfit items in a clean card layout
                for item in rec["outfit"]:
                    st.markdown(f"""
                    <div class="item-card">
                        <h3>{item['name']}</h3>
                        <p><strong>Category:</strong> {item['category']}</p>
                        <p><strong>Color:</strong> <span class="color-indicator" style="background-color: {item['color_hex']}"></span>{item['color']}</p>
                        <p><strong>Brand:</strong> {item['brand']}</p>
                        <p><strong>Price:</strong> ${item['price']}</p>
                        <p><strong>Material:</strong> {item['material']}</p>
                        <p><strong>Care:</strong> {item['care_instructions']}</p>
                        <p><strong>Compatibility Score:</strong> {item['compatibility_score']:.2f}</p>
                        <p><strong>Why it works:</strong> {item['reason']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display total price
                st.markdown(f"**Total Price:** ${rec['total_price']}")
                
                # Display additional information
                with st.expander("Style & Event Information"):
                    st.markdown(f"**Body Shape Info:**")
                    st.markdown(f"- {rec['body_shape_info']['description']}")
                    st.markdown(f"- Tip: {rec['body_shape_info']['tips']}")
                    
                    st.markdown(f"**Style Info:**")
                    st.markdown(f"- {rec['style_info']['description']}")
                    st.markdown(f"- Colors: {rec['style_info']['colors']}")
                    
                    st.markdown(f"**Event Info:**")
                    st.markdown(f"- Dress code: {rec['event_info']['dress_code']}")
                    st.markdown(f"- Formality: {rec['event_info']['formality']}")
            else:
                st.error(f"Error fetching recommendations. Status: {response.status_code}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
