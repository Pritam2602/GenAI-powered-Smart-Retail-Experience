import streamlit as st
import requests
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="GenAI Fashion Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Styling ---
# Dark theme styling to match the modern interface
st.markdown("""
<style>
    /* Dark theme for the entire app */
    .stApp {
        background-color: #0E1117; /* Dark background */
        color: #FAFAFA; /* Light text */
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    /* Container styling for sections */
    .stContainer {
        background-color: #262730;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid #3A3A3A;
    }
    
    /* Main button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #FF4B4B; /* Red accent color */
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #FAFAFA;
        font-weight: 700;
    }
    
    /* Metric cards styling */
    .metric-card {
        background-color: #262730;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #3A3A3A;
        margin: 10px 0;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #1F4E3D;
        border: 1px solid #4CAF50;
        border-radius: 8px;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #1E3A5F;
        border: 1px solid #2196F3;
        border-radius: 8px;
    }
    
    /* Warning message styling */
    .stWarning {
        background-color: #4A3C1A;
        border: 1px solid #FF9800;
        border-radius: 8px;
    }
    
    /* Error message styling */
    .stError {
        background-color: #4A1A1A;
        border: 1px solid #F44336;
        border-radius: 8px;
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        background-color: #262730;
        border: 1px solid #3A3A3A;
        color: #FAFAFA;
        border-radius: 8px;
    }
    
    /* Selectbox styling */
    .stSelectbox>div>div>select {
        background-color: #262730;
        border: 1px solid #3A3A3A;
        color: #FAFAFA;
        border-radius: 8px;
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background-color: #FF4B4B;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #262730;
        border: 1px solid #3A3A3A;
        border-radius: 8px;
        color: #FAFAFA;
    }
    
    /* Ensure all text is readable */
    body, p, li, div {
        color: #FAFAFA !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3A3A3A;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4A4A4A;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://placehold.co/400x150/0068c9/FFFFFF?text=GenAI+Fashion+Hub", use_container_width=True) # FIX: use_container_width
    st.header("API Configuration")
    api_base = st.text_input("API Base URL", value="http://127.0.0.1:8001")
    
    st.info("This app demonstrates a GenAI-powered fashion retail system. Use the sections below to interact with the AI models.")
    st.markdown("---")
    st.header("API Health Check")
    if st.button("Check API Status"):
        with st.spinner("Pinging API..."):
            try:
                r = requests.get(f"{api_base}/healthz")
                if r.ok:
                    st.success("API is running!")
                    st.json(r.json())
                else:
                    st.error(f"API returned status {r.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Connection failed. Is the FastAPI server running?")

# --- Main Content ---
st.title("🛍️ GenAI Fashion Hub")
st.markdown("**An AI-powered interface for fashion recommendations and price predictions.**")

# --- About the Fast Multi-Model System ---
with st.expander("🚀 About the Fast Multi-Model System", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Specialized Models:**
        - **💍 Jewelry Model**: Gold, silver, diamonds, precious stones
        - **⌚ Watch Model**: Timepieces, movements, luxury brands  
        - **👑 Luxury Apparel**: Designer, premium, high-end fashion
        - **👕 Standard Apparel**: Regular clothing and accessories
        """)
    
    with col2:
        st.markdown("""
        **⚡ Key Improvements:**
        - ✅ Better accuracy on jewelry & watches
        - ✅ Automatic product classification
        - ✅ Enhanced feature engineering
        - ✅ Realistic price constraints
        - ✅ Fast training (10 min vs. all day)
        - ✅ GPU acceleration (RTX 3050)
        """)

# --- Recommender Section ---
st.header("✨ Find Your Style: AI Recommender")
st.markdown("Discover similar fashion items using our AI-powered recommendation system.")

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Describe the fashion item you're looking for:", value="blue denim jacket for men")
with col2:
    k = st.slider("Number of recommendations:", 5, 20, 10)

if st.button("🔍 Get Recommendations"):
    with st.spinner("Searching for similar items..."):
        try:
            payload = {"query": query, "k": k}
            r = requests.post(f"{api_base}/recommend_products", json=payload)
            if r.ok:
                results = r.json().get('results', [])
                if not results:
                    st.warning("No similar items found. Try a different query.")
                else:
                    st.success(f"🎉 Found {len(results)} recommendations!")
                    st.markdown("---")
                    
                    # Display results in a modern grid
                    for i, item in enumerate(results):
                        meta = item.get('metadata', {})
                        
                        # Create a card-like layout for each recommendation
                        with st.container():
                            col1, col2, col3 = st.columns([1, 3, 1])
                            
                            with col1:
                                img_url = meta.get('img', 'https://placehold.co/200x250/262730/FAFAFA?text=No+Image')
                                # Ensure it's a valid URL
                                if img_url and (img_url.startswith('http://') or img_url.startswith('https://')):
                                    try:
                                        st.image(img_url, use_container_width=True, width=150)
                                    except Exception as e:
                                        st.image('https://placehold.co/200x250/262730/FAFAFA?text=No+Image', 
                                                use_container_width=True, width=150)
                                else:
                                    st.image('https://placehold.co/200x250/262730/FAFAFA?text=No+Image', 
                                            use_container_width=True, width=150)
                            
                            with col2:
                                st.markdown(f"**{meta.get('brand', 'N/A').title()}**")
                                st.caption(item.get('document', 'No description'))
                                st.markdown(f"**₹{meta.get('discounted_price', 0):,.0f}** | ⭐ {meta.get('avg_rating', 'N/A')}")
                            
                            with col3:
                                st.markdown(f"**Rating:** {meta.get('avg_rating', 'N/A')}")
                                st.markdown(f"**Reviews:** {meta.get('rating_count', 0)}")
                            
                            st.markdown("---")
            else:
                st.error(f"Error from API: {r.json().get('detail', r.text)}")
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Please ensure the FastAPI server is running.")

st.markdown("---")

# --- Price Predictor Section ---
st.header("💰 AI Price Predictor")
st.markdown("Fill in the product details to get an estimated price from the AI model.")

with st.form("price_form"):
    # Use columns for a cleaner layout
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", "Men Solid Casual Shirt")
        brand = st.text_input("Brand", "roadster")
        gender = st.selectbox("Gender", ["men", "women", "unisex", "boys", "girls"], index=0)
        category = st.text_input("Category", "shirt")
    with col2:
        fabric = st.text_input("Fabric", "cotton")
        pattern = st.text_input("Pattern", "solid")
        color = st.text_input("Color", "blue")
        rating_count = st.number_input("Number of Ratings", 0, 100000, 500)
    
    discount_percent = st.slider("Discount %", 0.0, 95.0, 40.0, 5.0)

    # The submit button for the form
    submit = st.form_submit_button("🚀 Predict Price")

    if submit:
        with st.spinner("Asking the AI for a price prediction..."):
            try:
                # Payload now matches the required fields for your advanced model
                payload = {
                    "product_name": product_name,
                    "brand": brand,
                    "gender": gender,
                    "category": category,
                    "fabric": fabric or None,
                    "pattern": pattern or None,
                    "color": color or None,
                    "rating_count": int(rating_count),
                    "discount_percent": float(discount_percent)
                }
                
                r = requests.post(f"{api_base}/predict_price", json=payload)
                
                if r.ok:
                    result = r.json()
                    
                    # Main prediction result with large display
                    st.markdown("---")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### 🎯 Predicted Price: **₹{result.get('predicted_price', 'N/A'):,.2f}**")
                    with col2:
                        st.markdown("### 🎯 Confidence: **High**")
                    
                    # Model information in a modern card layout
                    st.markdown("### 📊 Model Information")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Product Type", result.get('product_type', 'N/A').title())
                    with col2:
                        st.metric("Model Type", result.get('model_type', 'N/A').replace('_', ' ').title())
                    with col3:
                        confidence = "High" if result.get('product_type') in ['jewelry', 'watches'] else "Medium"
                        st.metric("Confidence", confidence)
                    
                    # Show which specialized model was used
                    product_type = result.get('product_type', 'N/A')
                    if product_type == 'jewelry':
                        st.info("💍 **Jewelry Model**: Optimized for gold, silver, diamonds, and precious stones")
                    elif product_type == 'watches':
                        st.info("⌚ **Watch Model**: Specialized for timepieces, movements, and luxury brands")
                    elif product_type == 'luxury_apparel':
                        st.info("👑 **Luxury Apparel Model**: For designer, premium, and high-end fashion items")
                    else:
                        st.info("👕 **Standard Apparel Model**: For regular clothing and accessories")
                else:
                    st.error(f"Error from API: {r.json().get('detail', r.text)}")
            except requests.exceptions.ConnectionError:
                st.error("Connection failed. Please ensure the FastAPI server is running.")

