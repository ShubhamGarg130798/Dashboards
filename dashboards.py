import streamlit as st
from datetime import datetime
import calendar
import requests

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Metabase Configuration
METABASE_URL = "http://43.205.95.106:3000/"  # Replace with your Metabase URL
METABASE_USERNAME = "shubham.garg@fintechcloud.in"  # Replace with your username
METABASE_PASSWORD = "Qwerty@12345"  # Replace with your password

# Function to get Metabase session token
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_metabase_token():
    """Get authentication token from Metabase"""
    try:
        response = requests.post(
            f"{METABASE_URL}/api/session",
            json={
                "username": METABASE_USERNAME,
                "password": METABASE_PASSWORD
            }
        )
        if response.status_code == 200:
            return response.json()['id']
        return None
    except Exception as e:
        st.error(f"Error connecting to Metabase: {e}")
        return None

# Function to fetch data from Metabase question/card
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_metabase_metric(card_id, token):
    """
    Fetch data from a Metabase question/card
    card_id: The ID of the Metabase question
    """
    try:
        headers = {
            "X-Metabase-Session": token
        }
        response = requests.post(
            f"{METABASE_URL}/api/card/{card_id}/query",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            # Extract the first row, first column value (adjust based on your query structure)
            if 'data' in data and 'rows' in data['data'] and len(data['data']['rows']) > 0:
                return data['data']['rows'][0][0]  # Adjust index based on your needs
        return "N/A"
    except Exception as e:
        return "N/A"

# Alternative: Fetch from Metabase public link/embed
@st.cache_data(ttl=300)
def fetch_metabase_public_metric(public_uuid):
    """
    Fetch data from a public Metabase question
    public_uuid: The public UUID from the shared link
    """
    try:
        response = requests.get(
            f"{METABASE_URL}/api/public/card/{public_uuid}/query"
        )
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'rows' in data['data'] and len(data['data']['rows']) > 0:
                return data['data']['rows'][0][0]
        return "N/A"
    except Exception as e:
        return "N/A"

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
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-left {
        flex: 1;
        text-align: center;
    }
    
    .header-right {
        position: absolute;
        right: 3rem;
        top: 2rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .current-date {
        font-size: 1.1rem;
        font-weight: 600;
        color: #64748b;
        background: #f1f5f9;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
    }
    
    .days-left {
        font-size: 0.95rem;
        font-weight: 600;
        color: #f59e0b;
        background: #fef3c7;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: 2px solid #fbbf24;
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
        height: 240px;
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
    
    /* Card Content */
    .card-brand-name {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .card-description {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    .card-target {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    
    .card-metric {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 1);
        font-weight: 800;
        background: rgba(255, 255, 255, 0.25);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
        margin-top: 0.4rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
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
        .header-section {
            flex-direction: column;
            gap: 1rem;
        }
        
        .header-right {
            position: relative;
            right: auto;
            top: auto;
        }
        
        .brand-card {
            padding: 1.5rem;
            min-height: 180px;
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

# Get current date and calculate days left in month
now = datetime.now()
current_date = now.strftime("%d %B %Y")
current_day = now.day
days_in_month = calendar.monthrange(now.year, now.month)[1]
days_left = days_in_month - current_day

# Header
st.markdown(f"""
    <div class="header-section">
        <div class="header-left">
            <div class="main-title">Brand Dashboards Portal</div>
            <div class="title-underline"></div>
        </div>
        <div class="header-right">
            <div class="current-date">📅 {current_date}</div>
            <div class="days-left">⏰ {days_left} days left in month</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Get Metabase token (only if using authenticated API)
# metabase_token = get_metabase_token()

# Define brand dashboards with colors and Metabase card IDs
brand_dashboards = [
    {
        "name": "Duniya",
        "url": "https://tinyurl.com/nhzvpuy6",
        "icon": "🌍",
        "description": "Harsh",
        "target": "₹15 Cr",
        "metabase_card_id": 123,  # Replace with actual Metabase question ID
        "metric_label": "MTD Disb.",
        "color": "blue"
    },
    {
        "name": "FastPaise",
        "url": "https://tinyurl.com/59dtjd88",
        "icon": "⚡",
        "description": "Ashutosh",
        "target": "₹18 Cr",
        "metabase_card_id": 124,
        "metric_label": "MTD Disb.",
        "color": "green"
    },
    {
        "name": "Jhatpat",
        "url": "https://tinyurl.com/294bc6ns",
        "icon": "🚀",
        "description": "Vivek",
        "target": "₹3 Cr",
        "metabase_card_id": 125,
        "metric_label": "MTD Disb.",
        "color": "orange"
    },
    {
        "name": "Paisa on Salary",
        "url": "https://tinyurl.com/fpxzjfsk",
        "icon": "💰",
        "description": "Ajay",
        "target": "₹5 Cr",
        "metabase_card_id": 126,
        "metric_label": "MTD Disb.",
        "color": "teal"
    },
    {
        "name": "SnapPaisa",
        "url": "https://tinyurl.com/2p9mdevt",
        "icon": "📸",
        "description": "Mumbai Team",
        "target": "₹18 Cr",
        "metabase_card_id": 127,
        "metric_label": "MTD Disb.",
        "color": "purple"
    },
    {
        "name": "Squid Loan",
        "url": "https://tinyurl.com/mphk5xpc",
        "icon": "🦑",
        "description": "Shashikant",
        "target": "₹5 Cr",
        "metabase_card_id": 128,
        "metric_label": "MTD Disb.",
        "color": "indigo"
    },
    {
        "name": "Tejas",
        "url": "https://tinyurl.com/29sb8js4",
        "icon": "✨",
        "description": "Nitin",
        "target": "₹15 Cr",
        "metabase_card_id": 129,
        "metric_label": "MTD Disb.",
        "color": "red"
    },
    {
        "name": "Zepto Finance",
        "url": "https://tinyurl.com/44cj83rw",
        "icon": "⚡",
        "description": "Arvind Jaiswal",
        "target": "₹9 Cr",
        "metabase_card_id": 130,
        "metric_label": "MTD Disb.",
        "color": "pink"
    },
    {
        "name": "FundoBaBa",
        "url": "https://tinyurl.com/5n9abwcx",
        "icon": "💼",
        "description": "Mumbai Team",
        "target": "₹25 Cr",
        "metabase_card_id": 193,
        "metric_label": "MTD Disb.",
        "color": "blue"
    },
    {
        "name": "Salary Setu",
        "url": "https://tinyurl.com/2we6eyvf",
        "icon": "💵",
        "description": "Prajwal",
        "target": "₹11 Cr",
        "metabase_card_id": 132,
        "metric_label": "MTD Disb.",
        "color": "green"
    },
    {
        "name": "Salary 4 Sure",
        "url": "https://tinyurl.com/bdfdufas",
        "icon": "💸",
        "description": "Vivek & Pranit",
        "target": "₹15 Cr",
        "metabase_card_id": 133,
        "metric_label": "MTD Disb.",
        "color": "orange"
    },
    {
        "name": "Salary Adda",
        "url": "https://tinyurl.com/4cd79c5b",
        "icon": "💳",
        "description": "Asim",
        "target": "₹10 Cr",
        "metabase_card_id": 134,
        "metric_label": "MTD Disb.",
        "color": "teal"
    }
]

# Create brand cards in rows of 4
for i in range(0, len(brand_dashboards), 4):
    cols = st.columns(4, gap="large")
    
    for j in range(4):
        if i + j < len(brand_dashboards):
            brand = brand_dashboards[i + j]
            
            # Fetch metric from Metabase
            # metric_value = fetch_metabase_metric(brand['metabase_card_id'], metabase_token)
            # For demo purposes, using placeholder
            metric_value = "₹8.5 Cr"  # Replace with actual API call
            
            with cols[j]:
                st.markdown(f"""
                    <a href="{brand['url']}" target="_blank">
                        <div class="brand-card card-{brand['color']}">
                            <div class="card-header">
                                <div class="card-label">{brand['name']}</div>
                                <div class="card-icon">{brand['icon']}</div>
                            </div>
                            <div>
                                <div class="card-description">👤 {brand['description']}</div>
                                <div class="card-target">🎯 Target: {brand['target']}</div>
                                <div class="card-metric">📊 {brand['metric_label']}: {metric_value}</div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
    
    # Add spacing between rows
    if i + 4 < len(brand_dashboards):
        st.markdown("<br>", unsafe_allow_html=True)
