import streamlit as st
import base64

# Embedded logo data
DUNIYA_LOGO = "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

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for KPI card style
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Override Streamlit's default backgrounds */
    .stApp {
        background: #ffffff;
    }
    
    .main {
        background: transparent;
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1600px;
        background: transparent;
    }
    
    /* Ensure all parent elements have white background */
    section[data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Header Styling */
    .header-section {
        margin-bottom: 3rem;
        padding-bottom: 1.5rem;
        text-align: center;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #2563eb;
        margin-bottom: 1rem;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    
    .title-underline {
        width: 240px;
        height: 6px;
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        border-radius: 3px;
        margin: 0 auto;
    }
    
    /* Brand Card Container */
    .brand-card-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Individual Brand Card */
    .brand-card {
        border-radius: 24px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .brand-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Card Colors */
    .card-blue {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }
    
    .card-green {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .card-orange {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .card-teal {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
    }
    
    .card-purple {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }
    
    .card-indigo {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    }
    
    .card-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .card-pink {
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
    }
    
    /* Card Header */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .card-label {
        font-size: 1.4rem;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.95);
        text-transform: capitalize;
        letter-spacing: 0.3px;
    }
    
    .card-icon {
        font-size: 2rem;
        background: rgba(255, 255, 255, 0.25);
        padding: 0.5rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 50px;
        min-height: 50px;
    }
    
    .card-logo {
        background: white;
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        max-width: 180px;
        max-height: 60px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .card-logo img {
        width: 100%;
        height: auto;
        object-fit: contain;
    }
    
    /* Card Content */
    .card-brand-name {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .card-description {
        font-size: 1.35rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        font-style: italic;
    }
    
    /* Link styling */
    a {
        text-decoration: none !important;
        color: inherit !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* Column styling */
    [data-testid="column"] {
        padding: 0 0.75rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .brand-card {
            padding: 1.5rem;
            min-height: 120px;
        }
        .card-brand-name {
            font-size: 1.5rem;
        }
        .main-title {
            font-size: 2.5rem;
        }
        .title-underline {
            width: 150px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <div class="main-title">Brand Dashboards Portal</div>
        <div class="title-underline"></div>
    </div>
    """, unsafe_allow_html=True)

# Define brand dashboards with colors
brand_dashboards = [
    {
        "name": "Duniya",
        "url": "https://tinyurl.com/nhzvpuy6",
        "logo": "Duniya_Finance.png",
        "description": "Harsh",
        "color": "blue"
    },
    {
        "name": "FastPaise",
        "url": "https://tinyurl.com/59dtjd88",
        "icon": "⚡",
        "description": "Ashutosh",
        "color": "green"
    },
    {
        "name": "Jhatpat",
        "url": "https://tinyurl.com/294bc6ns",
        "icon": "🚀",
        "description": "Vivek",
        "color": "orange"
    },
    {
        "name": "Paisa on Salary",
        "url": "https://tinyurl.com/fpxzjfsk",
        "icon": "💰",
        "description": "Ajay",
        "color": "teal"
    },
    {
        "name": "SnapPaisa",
        "url": "https://tinyurl.com/2p9mdevt",
        "icon": "📸",
        "description": "Mumbai Team",
        "color": "purple"
    },
    {
        "name": "Squid Loan",
        "url": "https://tinyurl.com/mphk5xpc",
        "icon": "🦑",
        "description": "Shashikant",
        "color": "indigo"
    },
    {
        "name": "Tejas",
        "url": "https://tinyurl.com/29sb8js4",
        "icon": "✨",
        "description": "Nitin",
        "color": "red"
    },
    {
        "name": "Zepto Finance",
        "url": "https://tinyurl.com/44cj83rw",
        "icon": "⚡",
        "description": "Arvind Jaiswal",
        "color": "pink"
    },
    {
        "name": "FundoBaBa",
        "url": "https://tinyurl.com/5n9abwcx",
        "icon": "💼",
        "description": "Mumbai Team",
        "color": "blue"
    }
]

# Create brand cards in rows of 4
for i in range(0, len(brand_dashboards), 4):
    cols = st.columns(4, gap="large")
    
    for j in range(4):
        if i + j < len(brand_dashboards):
            brand = brand_dashboards[i + j]
            with cols[j]:
                # Check if brand has logo or icon
                if 'logo' in brand:
                    if brand['logo'] == 'Duniya_Finance.png':
                        icon_html = f'<div class="card-logo"><img src="data:image/png;base64,{DUNIYA_LOGO}" alt="{brand["name"]} logo"></div>'
                    else:
                        icon_html = f'<div class="card-icon">{brand.get("icon", "📊")}</div>'
                else:
                    icon_html = f'<div class="card-icon">{brand["icon"]}</div>'
                
                st.markdown(f"""
                    <a href="{brand['url']}" target="_blank">
                        <div class="brand-card card-{brand['color']}">
                            <div class="card-header">
                                <div class="card-label">{brand['name']}</div>
                                {icon_html}
                            </div>
                            <div>
                                <div class="card-description">{brand['description']}</div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
    
    # Add spacing between rows
    if i + 4 < len(brand_dashboards):
        st.markdown("<br>", unsafe_allow_html=True)
