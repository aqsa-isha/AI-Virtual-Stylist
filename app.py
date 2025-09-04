import streamlit as st
import requests
import json
import os
import time

# Set page configuration
st.set_page_config(
    page_title="Style AI",
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
        else:
            return None
    except Exception as e:
        st.error(f"Error loading Lottie: {e}")
        return None

# Try to load animations, with fallbacks
try:
    lottie_fashion = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_V9t630.json")
    if lottie_fashion is None:
        lottie_fashion = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
except:
    lottie_fashion = None

try:
    lottie_loading = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_DMgKk2.json")
    if lottie_loading is None:
        lottie_loading = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_x62chj.json")
except:
    lottie_loading = None

try:
    lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_l5z0rj.json")
    if lottie_success is None:
        lottie_success = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_gciiixj2.json")
except:
    lottie_success = None

try:
    lottie_stylist = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_touohxv0.json")
    if lottie_stylist is None:
        lottie_stylist = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_1pxqjqps.json")
except:
    lottie_stylist = None

# API URL (will be replaced by ngrok URL)
api_url = os.getenv("BACKEND_URL", "http://localhost:8000/recommend")

# Custom CSS for stunning UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700&family=Parisienne&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #333;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .header h1 {
        font-family: 'Parisienne', cursive;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    /* Main container */
    .main-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        min-height: 100vh;
        padding: 20px;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
        transform: rotate(30deg);
    }
    
    .header h1 {
        font-size: 4.5rem;
        margin: 0;
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .header p {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.3rem;
        margin: 10px 0 0;
        color: rgba(255,255,255,0.9);
        position: relative;
        z-index: 1;
        font-weight: 300;
    }
    
    /* Sidebar */
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .sidebar-header {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        margin-bottom: 25px;
        text-align: center;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Form elements */
    .stSelectbox > div > div > select, .stSlider > div > div > div > div > div {
        font-family: 'Montserrat', sans-serif;
        background-color: rgba(255,255,255,0.9) !important;
        color: #333 !important;
        border-radius: 10px !important;
    }
    
    .stMultiiselect > div > div > div > div > div {
        font-family: 'Montserrat', sans-serif;
        background-color: rgba(255,255,255,0.9) !important;
        color: #333 !important;
        border-radius: 10px !important;
    }
    
    /* Button */
    div[data-testid="stSidebar"] > div > div > button {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 20px;
        font-weight: 600;
        width: 100%;
        margin-top: 20px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(245,87,108,0.4);
    }
    
    div[data-testid="stSidebar"] > div > div > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(245,87,108,0.6);
    }
    
    /* Loading animation container */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 30px 0;
    }
    
    .loading-text {
        font-family: 'Cormorant Garamond', serif;
        margin-top: 20px;
        font-size: 2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    
    /* Success animation container */
    .success-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 30px 0;
    }
    
    .success-text {
        font-family: 'Cormorant Garamond', serif;
        margin-top: 20px;
        font-size: 2rem;
        font-weight: 600;
        color: #4CAF50;
        letter-spacing: 0.5px;
    }
    
    /* Recommendation header */
    .recommendation-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 30px 0 20px;
        padding: 0 10px;
    }
    
    .recommendation-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3rem;
        margin: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    
    .compatibility-badge {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 5px 15px rgba(245,87,108,0.4);
    }
    
    /* Message box */
    .message-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        border-left: 5px solid #f5576c;
    }
    
    .message-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.2rem;
        margin: 0;
        color: #555;
        font-weight: 300;
        font-style: italic;
    }
    
    /* Outfit grid */
    .outfit-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 25px;
        margin-bottom: 30px;
    }
    
    /* Outfit card */
    .outfit-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .outfit-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .outfit-card-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 20px;
        color: white;
    }
    
    .outfit-card-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        margin: 0;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .outfit-card-body {
        padding: 20px;
    }
    
    .outfit-detail {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .outfit-detail-label {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        min-width: 100px;
        color: #555;
    }
    
    .outfit-detail-value {
        font-family: 'Montserrat', sans-serif;
        flex-grow: 1;
    }
    
    .color-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
        border: 1px solid #eee;
    }
    
    .outfit-reason {
        font-family: 'Montserrat', sans-serif;
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        border-left: 4px solid #f5576c;
        font-style: italic;
        font-weight: 300;
    }
    
    .outfit-score {
        font-family: 'Cormorant Garamond', serif;
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 5px 15px rgba(245,87,108,0.4);
    }
    
    /* Total price */
    .total-price-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    }
    
    .total-price-label {
        font-family: 'Montserrat', sans-serif;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0 0 10px;
        font-weight: 300;
    }
    
    .total-price-value {
        font-family: 'Cormorant Garamond', serif;
        color: white;
        font-size: 2.8rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 0.5px;
    }
    
    /* Info section */
    .info-section {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .info-section-header {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.2rem;
        margin-top: 0;
        margin-bottom: 20px;
        color: #667eea;
        text-align: center;
        letter-spacing: 0.5px;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
    }
    
    .info-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        border-top: 4px solid #667eea;
    }
    
    .info-card-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        margin-top: 0;
        margin-bottom: 15px;
        color: #764ba2;
        letter-spacing: 0.5px;
    }
    
    .info-card-list {
        font-family: 'Montserrat', sans-serif;
        padding-left: 20px;
        margin: 0;
    }
    
    .info-card-list li {
        margin-bottom: 8px;
        font-weight: 300;
    }
    
    /* Footer */
    .footer {
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #777;
        font-size: 0.9rem;
        font-weight: 300;
    }
</style>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div class="header">
    <h1>Style AI</h1>
    <p>Your Personal Fashion Assistant</p>
</div>
""", unsafe_allow_html=True)

# Display fashion animation with fallback
if lottie_fashion:
    try:
        st_lottie(lottie_fashion, height=250, key="fashion")
    except:
        st.markdown("""
        <div style="text-align: center; padding: 20px; font-size: 1.2rem; color: #667eea;">
            <p>✨ Your Personal Fashion Assistant ✨</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 20px; font-size: 1.2rem; color: #667eea;">
        <p>✨ Your Personal Fashion Assistant ✨</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-header">Customize Your Outfit</div>
    </div>
    """, unsafe_allow_html=True)
    
    body_shape = st.selectbox("Choose Body Shape", ["apple", "pear", "hourglass", "rectangle", "inverted_triangle"])
    personal_style = st.selectbox("Choose Personal Style", ["casual", "formal", "bohemian", "sporty", "classic", "trendy"])
    event_type = st.selectbox("Choose Event Type", ["work", "party", "date", "casual outing", "wedding", "interview"])
    budget = st.slider("Budget ($)", 20, 500, 150)
    exclude_colors = st.multiselect("Exclude Colors", ["black", "white", "blue", "red", "green", "yellow", "purple", "pink", "brown", "gray"])
    
    # Display stylist animation with fallback
    if lottie_stylist:
        try:
            st_lottie(lottie_stylist, height=200, key="stylist")
        except:
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <p>👗 Your Personal Stylist 👗</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p>👗 Your Personal Stylist 👗</p>
        </div>
        """, unsafe_allow_html=True)

# Button to get recommendations
if st.sidebar.button("Get Recommendations"):
    # Show loading animation
    loading_container = st.empty()
    with loading_container.container():
        if lottie_loading:
            try:
                st.markdown("""
                <div class="loading-container">
                    <div style="width: 250px; height: 250px;">
                """, unsafe_allow_html=True)
                st_lottie(lottie_loading, height=250, key="loading")
                st.markdown("""
                    </div>
                    <p class="loading-text">Finding your perfect outfit...</p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown("""
                <div class="loading-container">
                    <p class="loading-text">Finding your perfect outfit...</p>
                    <div style="margin-top: 20px;">
                        <div style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: #667eea; animation: pulse 1.5s infinite;"></div>
                        <div style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: #764ba2; animation: pulse 1.5s infinite; animation-delay: 0.2s; margin-left: 5px;"></div>
                        <div style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: #f093fb; animation: pulse 1.5s infinite; animation-delay: 0.4s; margin-left: 5px;"></div>
                    </div>
                    <style>
                        @keyframes pulse {
                            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
                            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
                            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
                        }
                    </style>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="loading-container">
                <p class="loading-text">Finding your perfect outfit...</p>
                <div style="margin-top: 20px;">
                    <div style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: #667eea; animation: pulse 1.5s infinite;"></div>
                    <div style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: #764ba2; animation: pulse 1.5s infinite; animation-delay: 0.2s; margin-left: 5px;"></div>
                    <div style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: #f093fb; animation: pulse 1.5s infinite; animation-delay: 0.4s; margin-left: 5px;"></div>
                </div>
                <style>
                    @keyframes pulse {
                        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
                        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
                        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
                    }
                </style>
            </div>
            """, unsafe_allow_html=True)
    
    # Make API request
    payload = {
        "body_shape": body_shape,
        "personal_style": personal_style,
        "event_type": event_type,
        "budget": budget,
        "exclude_colors": exclude_colors
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        
        # Clear loading animation
        loading_container.empty()
        
        if response.status_code == 200:
            rec = response.json()
            
            # Show success animation
            success_container = st.empty()
            if lottie_success:
                try:
                    with success_container.container():
                        st.markdown("""
                        <div class="success-container">
                            <div style="width: 200px; height: 200px;">
                        """, unsafe_allow_html=True)
                        st_lottie(lottie_success, height=200, key="success")
                        st.markdown("""
                            </div>
                            <p class="success-text">Perfect match found!</p>
                        </div>
                        """, unsafe_allow_html=True)
                except:
                    with success_container.container():
                        st.markdown("""
                        <div class="success-container">
                            <p class="success-text">✨ Perfect match found! ✨</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                with success_container.container():
                    st.markdown("""
                    <div class="success-container">
                        <p class="success-text">✨ Perfect match found! ✨</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Wait a moment to show the success animation
            time.sleep(2)
            success_container.empty()
            
            # Display recommendation header
            st.markdown("""
            <div class="recommendation-header">
                <h2 class="recommendation-title">✨ Outfit Recommendation</h2>
                <div class="compatibility-badge">Compatibility: {:.2f}</div>
            </div>
            """.format(rec['overall_compatibility']), unsafe_allow_html=True)
            
            # Display message
            st.markdown("""
            <div class="message-box">
                <p class="message-text">{}</p>
            </div>
            """.format(rec['message']), unsafe_allow_html=True)
            
            # Display outfit items in a grid
            st.markdown('<div class="outfit-grid">', unsafe_allow_html=True)
            for item in rec["outfit"]:
                st.markdown("""
                <div class="outfit-card">
                    <div class="outfit-card-header">
                        <h3 class="outfit-card-title">{}</h3>
                    </div>
                    <div class="outfit-card-body">
                        <div class="outfit-detail">
                            <span class="outfit-detail-label">Category:</span>
                            <span class="outfit-detail-value">{}</span>
                        </div>
                        <div class="outfit-detail">
                            <span class="outfit-detail-label">Color:</span>
                            <span class="outfit-detail-value"><span class="color-indicator" style="background-color: {}"></span>{}</span>
                        </div>
                        <div class="outfit-detail">
                            <span class="outfit-detail-label">Brand:</span>
                            <span class="outfit-detail-value">{}</span>
                        </div>
                        <div class="outfit-detail">
                            <span class="outfit-detail-label">Price:</span>
                            <span class="outfit-detail-value">${}</span>
                        </div>
                        <div class="outfit-detail">
                            <span class="outfit-detail-label">Material:</span>
                            <span class="outfit-detail-value">{}</span>
                        </div>
                        <div class="outfit-detail">
                            <span class="outfit-detail-label">Care:</span>
                            <span class="outfit-detail-value">{}</span>
                        </div>
                        <div class="outfit-reason">
                            <strong>Why it works:</strong> {}
                        </div>
                    </div>
                    <div class="outfit-score">{:.2f}</div>
                </div>
                """.format(
                    item['name'], 
                    item['category'],
                    item['color_hex'], 
                    item['color'],
                    item['brand'],
                    item['price'],
                    item['material'],
                    item['care_instructions'],
                    item['reason'],
                    item['compatibility_score']
                ), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display total price
            st.markdown("""
            <div class="total-price-container">
                <p class="total-price-label">Total Price</p>
                <p class="total-price-value">${}</p>
            </div>
            """.format(rec['total_price']), unsafe_allow_html=True)
            
            # Display additional information
            with st.expander("Style & Event Information", expanded=False):
                st.markdown("""
                <div class="info-section">
                    <h3 class="info-section-header">Style & Event Information</h3>
                    <div class="info-grid">
                        <div class="info-card">
                            <h4 class="info-card-title">Body Shape Info</h4>
                            <ul class="info-card-list">
                                <li>{}</li>
                                <li><strong>Tip:</strong> {}</li>
                            </ul>
                        </div>
                        <div class="info-card">
                            <h4 class="info-card-title">Style Info</h4>
                            <ul class="info-card-list">
                                <li>{}</li>
                                <li><strong>Colors:</strong> {}</li>
                            </ul>
                        </div>
                        <div class="info-card">
                            <h4 class="info-card-title">Event Info</h4>
                            <ul class="info-card-list">
                                <li><strong>Dress code:</strong> {}</li>
                                <li><strong>Formality:</strong> {}</li>
                            </ul>
                        </div>
                    </div>
                </div>
                """.format(
                    rec['body_shape_info']['description'],
                    rec['body_shape_info']['tips'],
                    rec['style_info']['description'],
                    rec['style_info']['colors'],
                    rec['event_info']['dress_code'],
                    rec['event_info']['formality']
                ), unsafe_allow_html=True)
            
            # Footer
            st.markdown("""
            <div class="footer">
                <p>Style AI © 2023 | Powered by Advanced Fashion AI</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error(f"Error fetching recommendations. Status: {response.status_code}. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        # Clear loading animation
        loading_container.empty()
        st.error(f"API request failed: {e}")

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
