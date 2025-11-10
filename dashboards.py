import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for modern, professional styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    h1 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    h3 {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 400 !important;
        margin-bottom: 2rem !important;
    }
    
    /* Card Container */
    .dashboard-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        height: 120px;
        font-size: 20px;
        font-weight: 600;
        border-radius: 15px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(-2px);
    }
    
    /* Section Styling */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.5rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 10px;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Links Styling */
    a {
        text-decoration: none;
        color: #667eea;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #764ba2;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Success message styling */
    .stSuccess {
        background: #48bb78;
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# App header
st.markdown('<h1>📊 Brand Dashboards Portal</h1>', unsafe_allow_html=True)
st.markdown('<h3>Access all your brand analytics in one place</h3>', unsafe_allow_html=True)

# Define your brand dashboards here
# Format: {"Brand Name": {"url": "Dashboard URL", "icon": "emoji", "description": "text"}}
brand_dashboards = {
    "Duniya": {
        "url": "https://tinyurl.com/nhzvpuy6",
        "icon": "🌍",
        "description": "Duniya Dashboard"
    },
    "FastPaise": {
        "url": "https://tinyurl.com/59dtjd88",
        "icon": "⚡",
        "description": "FastPaise Dashboard"
    },
    "Jhatpat": {
        "url": "https://tinyurl.com/294bc6ns",
        "icon": "🚀",
        "description": "Jhatpat Dashboard"
    },
    "Paisa on Salary": {
        "url": "https://tinyurl.com/fpxzjfsk",
        "icon": "💰",
        "description": "Paisa on Salary Dashboard"
    },
    "SnapPaisa": {
        "url": "https://tinyurl.com/2p9mdevt",
        "icon": "📸",
        "description": "SnapPaisa Dashboard"
    },
    "Squid Loan": {
        "url": "https://tinyurl.com/mphk5xpc",
        "icon": "🦑",
        "description": "Squid Loan Dashboard"
    },
    "Tejas": {
        "url": "https://tinyurl.com/29sb8js4",
        "icon": "✨",
        "description": "Tejas Dashboard"
    },
    "Zepto": {
        "url": "https://tinyurl.com/44cj83rw",
        "icon": "⚡",
        "description": "Zepto Dashboard"
    },
}

# Brand dashboards section with direct links
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Select a brand to view its dashboard</div>', unsafe_allow_html=True)

# Display all brands in a clean grid
cols = st.columns(2, gap="large")
for idx, (name, info) in enumerate(brand_dashboards.items()):
    with cols[idx % 2]:
        st.markdown(f"### {info['icon']} [{name}]({info['url']})")
        st.markdown(f"<p style='color: #718096; margin-top: -1rem;'>{info['description']}</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Brand Dashboards Portal | Built with Streamlit 🎈</div>', unsafe_allow_html=True)
