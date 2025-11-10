import streamlit as st

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
    
    .main {
        background: linear-gradient(to bottom, #f0f4ff 0%, #e8eeff 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1600px;
    }
    
    /* Header Styling */
    .header-section {
        margin-bottom: 3rem;
        padding-bottom: 1.5rem;
    }
    
    .main-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #1e3a8a;
        margin-bottom: 1rem;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    
    .title-underline {
        width: 240px;
        height: 6px;
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        border-radius: 3px;
        margin-bottom: 0;
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
        font-size: 0.9rem;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.95);
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
    
    /* Card Content */
    .card-brand-name {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .card-description {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
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
        "icon": "🌍",
        "description": "Global lending platform analytics",
        "color": "blue"
    },
    {
        "name": "FastPaise",
        "url": "https://tinyurl.com/59dtjd88",
        "icon": "⚡",
        "description": "Quick loan performance metrics",
        "color": "green"
    },
    {
        "name": "Jhatpat",
        "url": "https://tinyurl.com/294bc6ns",
        "icon": "🚀",
        "description": "Instant credit dashboard",
        "color": "orange"
    },
    {
        "name": "Paisa on Salary",
        "url": "https://tinyurl.com/fpxzjfsk",
        "icon": "💰",
        "description": "Salary-linked lending insights",
        "color": "teal"
    },
    {
        "name": "SnapPaisa",
        "url": "https://tinyurl.com/2p9mdevt",
        "icon": "📸",
        "description": "Instant approval analytics",
        "color": "purple"
    },
    {
        "name": "Squid Loan",
        "url": "https://tinyurl.com/mphk5xpc",
        "icon": "🦑",
        "description": "Flexible loan solutions dashboard",
        "color": "indigo"
    },
    {
        "name": "Tejas",
        "url": "https://tinyurl.com/29sb8js4",
        "icon": "✨",
        "description": "Premium lending platform",
        "color": "red"
    },
    {
        "name": "Zepto",
        "url": "https://tinyurl.com/44cj83rw",
        "icon": "⚡",
        "description": "Lightning-fast credit analytics",
        "color": "pink"
    }
]

# Create brand cards in rows of 4
for i in range(0, len(brand_dashboards), 4):
    cols = st.columns(4, gap="large")
    
    for j in range(4):
        if i + j < len(brand_dashboards):
            brand = brand_dashboards[i + j]
            with cols[j]:
                st.markdown(f"""
                    <a href="{brand['url']}" target="_blank">
                        <div class="brand-card card-{brand['color']}">
                            <div class="card-header">
                                <div class="card-label">{brand['name']}</div>
                                <div class="card-icon">{brand['icon']}</div>
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
