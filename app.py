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

# API URL (will be replaced by ngrok URL)
api_url = os.getenv("BACKEND_URL", "http://localhost:8000/recommend")

# Function to create mock response when backend is not available
def get_mock_response(body_shape, personal_style, event_type, budget, exclude_colors):
    # Create mock outfit items
    mock_outfits = [
        {
            "id": 1,
            "name": "Elegant Silk Blouse",
            "category": "top",
            "color": "blue",
            "color_hex": "#1E88E5",
            "style": "classic",
            "reason": f"Perfect for your {body_shape} body shape. Matches your {personal_style} style and the {event_type} event.",
            "brand": "Zara",
            "price": 89,
            "description": "Elegant silk blouse perfect for any occasion",
            "material": "Silk",
            "care_instructions": "Dry clean only",
            "compatibility_score": 0.85
        },
        {
            "id": 2,
            "name": "Tailored Trousers",
            "category": "bottom",
            "color": "black",
            "color_hex": "#000000",
            "style": "classic",
            "reason": f"These trousers complement your {body_shape} body shape and match your {personal_style} style.",
            "brand": "H&M",
            "price": 59,
            "description": "Comfortable and stylish tailored trousers",
            "material": "Polyester",
            "care_instructions": "Machine wash cold",
            "compatibility_score": 0.90
        },
        {
            "id": 3,
            "name": "Leather Handbag",
            "category": "accessories",
            "color": "brown",
            "color_hex": "#6D4C41",
            "style": "classic",
            "reason": f"This accessory completes your {personal_style} look for the {event_type} event.",
            "brand": "Mango",
            "price": 75,
            "description": "Elegant leather handbag with plenty of space",
            "material": "Leather",
            "care_instructions": "Wipe with damp cloth",
            "compatibility_score": 0.80
        }
    ]
    
    # Calculate total price
    total_price = sum(item["price"] for item in mock_outfits)
    
    # Calculate overall compatibility
    overall_compatibility = sum(item["compatibility_score"] for item in mock_outfits) / len(mock_outfits)
    
    # Create message based on compatibility
    if overall_compatibility > 0.8:
        message = "Excellent match! This outfit is perfect for you and will make you look amazing."
    elif overall_compatibility > 0.6:
        message = "Great choice! This outfit suits you well and matches your preferences."
    else:
        message = "Good option! You might want to consider some accessories to complete the look."
    
    # Create mock body shape info
    body_shape_info = {
        "apple": {
            "description": "Wider torso, narrower hips",
            "tips": "Draw attention away from midsection"
        },
        "pear": {
            "description": "Narrower torso, wider hips",
            "tips": "Balance proportions with structured tops"
        },
        "hourglass": {
            "description": "Balanced bust and hips with narrow waist",
            "tips": "Highlight waist with fitted styles"
        },
        "rectangle": {
            "description": "Similar width bust, waist, and hips",
            "tips": "Create curves with strategic layering"
        },
        "inverted_triangle": {
            "description": "Wider shoulders, narrower hips",
            "tips": "Add volume to lower body"
        }
    }
    
    # Create mock style info
    style_info = {
        "casual": {
            "description": "Comfortable, relaxed, everyday wear",
            "colors": "earth tones, pastels, denim"
        },
        "formal": {
            "description": "Professional, elegant attire",
            "colors": "navy, black, gray, white"
        },
        "bohemian": {
            "description": "Free-spirited, artistic, unconventional",
            "colors": "warm tones, patterns, textured fabrics"
        },
        "sporty": {
            "description": "Athletic, functional, active wear",
            "colors": "brights, neutrals, performance fabrics"
        },
        "classic": {
            "description": "Timeless, tailored, traditional",
            "colors": "neutrals, jewel tones, clean lines"
        },
        "trendy": {
            "description": "Fashion-forward, current styles",
            "colors": "seasonal colors, bold patterns, statement pieces"
        }
    }
    
    # Create mock event info
    event_info = {
        "work": {
            "dress_code": "Business casual to formal",
            "formality": "medium"
        },
        "party": {
            "dress_code": "Cocktail to festive",
            "formality": "high"
        },
        "date": {
            "dress_code": "Smart casual to dressy",
            "formality": "medium"
        },
        "casual outing": {
            "dress_code": "Relaxed and comfortable",
            "formality": "low"
        },
        "wedding": {
            "dress_code": "Formal to black tie",
            "formality": "very high"
        },
        "interview": {
            "dress_code": "Professional and conservative",
            "formality": "high"
        }
    }
    
    # Return mock response in the same format as the API
    return {
        "outfit": mock_outfits,
        "overall_compatibility": overall_compatibility,
        "message": message,
        "body_shape_info": body_shape_info.get(body_shape, body_shape_info["hourglass"]),
        "style_info": style_info.get(personal_style, style_info["classic"]),
        "event_info": event_info.get(event_type, event_info["work"]),
        "total_price": total_price
    }

# Custom CSS for stunning UI with animations
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
        animation: fadeIn 1s ease-in-out;
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
        animation: slideDown 0.8s ease-out;
    }
    
    .header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
        z-index: 0;
        animation: shimmer 3s infinite;
    }
    
    .header h1, .header p {
        position: relative;
        z-index: 1;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Form elements */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff9a9e;
        box-shadow: 0 0 0 3px rgba(255, 154, 158, 0.2);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #ff9a9e;
        box-shadow: 0 0 0 3px rgba(255, 154, 158, 0.2);
    }
    
    .stSlider > div > div > div > div {
        background: #ff9a9e;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 154, 158, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(1px);
    }
    
    .stButton > button::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    
    .stButton > button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid #f0f0f0;
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    .recommendation-card:nth-child(1) {
        animation-delay: 0.2s;
    }
    
    .recommendation-card:nth-child(2) {
        animation-delay: 0.4s;
    }
    
    .recommendation-card:nth-child(3) {
        animation-delay: 0.6s;
    }
    
    .recommendation-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Message box */
    .message-box {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #ff9a9e;
        animation: fadeIn 1s ease-out;
    }
    
    /* Total price container */
    .price-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        animation: fadeIn 1.2s ease-out;
    }
    
    .price-container h3 {
        color: #333;
        margin-bottom: 10px;
    }
    
    .price {
        font-size: 2rem;
        font-weight: 700;
        color: #ff9a9e;
        animation: pulse 2s infinite;
    }
    
    /* Info boxes */
    .info-box {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        animation: fadeInUp 0.8s ease-out;
        animation-fill-mode: both;
    }
    
    .info-box:nth-child(1) {
        animation-delay: 0.3s;
    }
    
    .info-box:nth-child(2) {
        animation-delay: 0.5s;
    }
    
    .info-box:nth-child(3) {
        animation-delay: 0.7s;
    }
    
    .info-box h3 {
        color: #ff9a9e;
        margin-bottom: 10px;
        font-family: 'Cormorant Garamond', serif;
    }
    
    /* Compatibility score */
    .compatibility-score {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 15px;
        animation: scaleIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9rem;
        animation: fadeIn 1.5s ease-out;
    }
    
    /* Remove light blue from all elements */
    div[data-testid="stVerticalBlock"] > div[style*="background-color: rgb(173, 216, 230)"] {
        background-color: white !important;
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="background-color: rgb(135, 206, 235)"] {
        background-color: white !important;
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="background-color: rgb(176, 224, 230)"] {
        background-color: white !important;
    }
    
    /* Remove light blue borders */
    div[data-testid="stVerticalBlock"] > div[style*="border-color: rgb(173, 216, 230)"] {
        border-color: #e2e8f0 !important;
    }
    
    /* Remove light blue from Streamlit's default elements */
    .element-container .stAlert {
        background-color: white !important;
        border-left: 5px solid #ff9a9e !important;
    }
    
    /* Remove light blue from metrics */
    div[data-testid="metric-container"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    div[data-testid="metric-container"] > label {
        color: #666 !important;
    }
    
    div[data-testid="metric-container"] > div {
        color: #333 !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
    }
    
    /* Animated background elements */
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .animated-bg span {
        position: absolute;
        display: block;
        width: 20px;
        height: 20px;
        background: rgba(255, 154, 158, 0.1);
        animation: move 25s linear infinite;
        bottom: -150px;
        border-radius: 50%;
    }
    
    .animated-bg span:nth-child(1) {
        left: 25%;
        width: 80px;
        height: 80px;
        animation-delay: 0s;
    }
    
    .animated-bg span:nth-child(2) {
        left: 10%;
        width: 20px;
        height: 20px;
        animation-delay: 2s;
        animation-duration: 12s;
    }
    
    .animated-bg span:nth-child(3) {
        left: 70%;
        width: 20px;
        height: 20px;
        animation-delay: 4s;
    }
    
    .animated-bg span:nth-child(4) {
        left: 40%;
        width: 60px;
        height: 60px;
        animation-delay: 0s;
        animation-duration: 18s;
    }
    
    .animated-bg span:nth-child(5) {
        left: 65%;
        width: 20px;
        height: 20px;
        animation-delay: 0s;
    }
    
    .animated-bg span:nth-child(6) {
        left: 75%;
        width: 110px;
        height: 110px;
        animation-delay: 3s;
    }
    
    @keyframes move {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
            border-radius: 50%;
        }
        100% {
            transform: translateY(-1000px) rotate(720deg);
            opacity: 0;
            border-radius: 50%;
        }
    }
</style>

<div class="animated-bg">
    <span></span>
    <span></span>
    <span></span>
    <span></span>
    <span></span>
    <span></span>
</div>
""", unsafe_allow_html=True)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>Style AI</h1>
        <p>Your personal fashion stylist powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar">
            <h2>Your Preferences</h2>
            <p>Tell us about yourself to get personalized outfit recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form inputs
        body_shape = st.selectbox(
            "Body Shape",
            ["apple", "pear", "hourglass", "rectangle", "inverted_triangle"],
            index=2
        )
        
        personal_style = st.selectbox(
            "Personal Style",
            ["casual", "formal", "bohemian", "sporty", "classic", "trendy"],
            index=4
        )
        
        event_type = st.selectbox(
            "Event Type",
            ["work", "party", "date", "casual outing", "wedding", "interview"],
            index=0
        )
        
        budget = st.slider(
            "Budget ($)",
            min_value=50,
            max_value=500,
            value=200,
            step=10
        )
        
        exclude_colors = st.multiselect(
            "Colors to Exclude",
            ["red", "blue", "green", "yellow", "black", "white", "pink", "purple", "orange", "brown", "gray"]
        )
        
        # Get recommendations button
        get_recommendations = st.button("Get Recommendations")
    
    # Main content
    if get_recommendations:
        # Show loading spinner
        with st.spinner("Finding the perfect outfit for you..."):
            # Simulate API call delay
            time.sleep(2)
            
            # Get recommendations (mock or real)
            try:
                # Try to get real recommendations from API
                response = requests.post(
                    api_url,
                    json={
                        "body_shape": body_shape,
                        "personal_style": personal_style,
                        "event_type": event_type,
                        "budget": budget,
                        "exclude_colors": exclude_colors
                    }
                )
                
                if response.status_code == 200:
                    recommendations = response.json()
                else:
                    recommendations = get_mock_response(body_shape, personal_style, event_type, budget, exclude_colors)
            except:
                # Fallback to mock response
                recommendations = get_mock_response(body_shape, personal_style, event_type, budget, exclude_colors)
        
        # Display message
        st.markdown(f"""
        <div class="message-box">
            <h3>Recommendation</h3>
            <p>{recommendations['message']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display compatibility score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="compatibility-score">
                {int(recommendations['overall_compatibility'] * 100)}%
            </div>
            <p style="text-align:center;">Compatibility</p>
            """, unsafe_allow_html=True)
        
        # Display outfit recommendations
        st.markdown("<h2>Recommended Outfit</h2>", unsafe_allow_html=True)
        
        for item in recommendations['outfit']:
            st.markdown(f"""
            <div class="recommendation-card">
                <h3>{item['name']}</h3>
                <p><strong>Brand:</strong> {item['brand']} | <strong>Price:</strong> ${item['price']}</p>
                <p><strong>Color:</strong> <span style="display:inline-block;width:20px;height:20px;background-color:{item['color_hex']};border-radius:50%;vertical-align:middle;"></span> {item['color'].capitalize()}</p>
                <p><strong>Material:</strong> {item['material']}</p>
                <p><strong>Care:</strong> {item['care_instructions']}</p>
                <p><strong>Why it works:</strong> {item['reason']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display total price
        st.markdown(f"""
        <div class="price-container">
            <h3>Total Outfit Price</h3>
            <div class="price">${recommendations['total_price']}</div>
            <p>Within your ${budget} budget</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display additional information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h3>Body Shape: {body_shape.capitalize()}</h3>
                <p>{recommendations['body_shape_info']['description']}</p>
                <p><strong>Tip:</strong> {recommendations['body_shape_info']['tips']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <h3>Style: {personal_style.capitalize()}</h3>
                <p>{recommendations['style_info']['description']}</p>
                <p><strong>Colors:</strong> {recommendations['style_info']['colors']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="info-box">
                <h3>Event: {event_type.capitalize()}</h3>
                <p><strong>Dress Code:</strong> {recommendations['event_info']['dress_code']}</p>
                <p><strong>Formality:</strong> {recommendations['event_info']['formality'].replace('_', ' ').capitalize()}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Style AI | Your Personal Fashion Assistant</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
