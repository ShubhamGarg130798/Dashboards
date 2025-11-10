import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for vibrant, modern styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Remove default padding */
    .block-container {
        padding: 3rem 2rem;
        max-width: 1400px;
    }
    
    /* Header Styling */
    .header-section {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeIn 0.8s ease-in;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 400;
    }
    
    /* Brand Card Styling */
    .brand-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(255, 255, 255, 0.8);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .brand-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .brand-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 48px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
    }
    
    .brand-card:hover::before {
        opacity: 1;
    }
    
    .brand-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .brand-name {
        font-size: 2rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .brand-description {
        font-size: 1.1rem;
        color: #4a5568;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Link styling */
    a {
        text-decoration: none !important;
        color: inherit !important;
    }
    
    a:hover .brand-card {
        transform: translateY(-12px) scale(1.02);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card-animate {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* Column styling */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        margin-top: 3rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
        }
        .brand-card {
            padding: 2rem;
        }
        .brand-icon {
            font-size: 2.5rem;
        }
        .brand-name {
            font-size: 1.6rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
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
brands_list = list(brand_dashboards.items())
for i in range(0, len(brands_list), 2):
    cols = st.columns(2, gap="large")
    
    for j in range(2):
        if i + j < len(brands_list):
            brand_name, info = brands_list[i + j]
            with cols[j]:
                st.markdown(f"""
                    <a href="{info['url']}" target="_blank">
                        <div class="brand-card card-animate" style="animation-delay: {(i+j)*0.1}s;">
                            <div class="brand-icon">{info['icon']}</div>
                            <div class="brand-name">{brand_name}</div>
                            <div class="brand-description">{info['description']}</div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-text">
        <strong>Click any card to open the dashboard</strong> • Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)
