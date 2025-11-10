import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for modern, beautiful styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Header Styling */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #f0f0f0 !important;
        font-weight: 400;
    }
    
    /* Brand Cards Container */
    .brands-container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Individual Brand Card */
    .brand-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        border: 3px solid transparent;
    }
    
    .brand-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
        border-color: #667eea;
    }
    
    .brand-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .brand-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
        text-decoration: none;
    }
    
    .brand-description {
        font-size: 1rem;
        color: #718096;
        margin-top: 0.5rem;
    }
    
    /* Link styling */
    a {
        text-decoration: none !important;
        color: inherit !important;
    }
    
    a:hover .brand-name {
        color: #667eea;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Column styling */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        .brand-card {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <div class="main-title">📊 Brand Dashboards Portal</div>
        <div class="subtitle">Access all your brand analytics in one place</div>
    </div>
    """, unsafe_allow_html=True)

# Define your brand dashboards here
brand_dashboards = {
    "Duniya": {
        "url": "https://tinyurl.com/nhzvpuy6",
        "icon": "🌍",
        "description": "Global lending platform analytics"
    },
    "FastPaise": {
        "url": "https://tinyurl.com/59dtjd88",
        "icon": "⚡",
        "description": "Quick loan performance metrics"
    },
    "Jhatpat": {
        "url": "https://tinyurl.com/294bc6ns",
        "icon": "🚀",
        "description": "Instant credit dashboard"
    },
    "Paisa on Salary": {
        "url": "https://tinyurl.com/fpxzjfsk",
        "icon": "💰",
        "description": "Salary-linked lending insights"
    },
    "SnapPaisa": {
        "url": "https://tinyurl.com/2p9mdevt",
        "icon": "📸",
        "description": "Instant approval analytics"
    },
    "Squid Loan": {
        "url": "https://tinyurl.com/mphk5xpc",
        "icon": "🦑",
        "description": "Flexible loan solutions dashboard"
    },
    "Tejas": {
        "url": "https://tinyurl.com/29sb8js4",
        "icon": "✨",
        "description": "Premium lending platform"
    },
    "Zepto": {
        "url": "https://tinyurl.com/44cj83rw",
        "icon": "⚡",
        "description": "Lightning-fast credit analytics"
    },
}

# Create brand cards in 2-column layout
st.markdown('<div class="brands-container">', unsafe_allow_html=True)

brands_list = list(brand_dashboards.items())
for i in range(0, len(brands_list), 2):
    cols = st.columns(2, gap="large")
    
    for j in range(2):
        if i + j < len(brands_list):
            brand_name, info = brands_list[i + j]
            with cols[j]:
                st.markdown(f"""
                    <a href="{info['url']}" target="_blank">
                        <div class="brand-card">
                            <div class="brand-icon">{info['icon']}</div>
                            <div class="brand-name">{brand_name}</div>
                            <div class="brand-description">{info['description']}</div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: rgba(255,255,255,0.8);">
        <p style="font-size: 0.9rem;">Built with Streamlit 🎈 | Click any card to open dashboard</p>
    </div>
    """, unsafe_allow_html=True)
