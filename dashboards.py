import streamlit as st
from datetime import datetime
import calendar
import requests
import time

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Metabase Configuration
METABASE_URL = "http://43.205.95.106:3000"
METABASE_USERNAME = "shubham.garg@fintechcloud.in"
METABASE_PASSWORD = "Qwerty@12345"

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
            },
            timeout=10
        )
        if response.status_code == 200:
            token = response.json()['id']
            return token
        else:
            return None
    except Exception as e:
        return None

# Function to fetch data from Metabase
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_metabase_metric_v2(card_id, token):
    """
    Fetch using /query/json endpoint
    """
    if not token:
        return "Auth Error"
    
    try:
        headers = {
            "X-Metabase-Session": token,
            "Content-Type": "application/json"
        }
        
        # Try using json/query endpoint with empty parameters
        response = requests.post(
            f"{METABASE_URL}/api/card/{card_id}/query/json",
            headers=headers,
            json={"parameters": []},
            timeout=45
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # The json endpoint returns an array of objects
            if isinstance(data, list) and len(data) > 0:
                # Get the first row
                first_row = data[0]
                # Get the first value (should be total_disbursed_amount)
                if isinstance(first_row, dict):
                    # Get the value from the dict
                    value = list(first_row.values())[0] if first_row else None
                else:
                    value = first_row
                
                if value is None:
                    return "₹0.00"
                
                # Format the value
                if isinstance(value, (int, float)):
                    if value >= 10000000:  # 1 Crore
                        return f"₹{value/10000000:.2f} Cr"
                    elif value >= 100000:  # 1 Lakh
                        return f"₹{value/100000:.2f} L"
                    else:
                        return f"₹{value:,.0f}"
                return str(value)
            
            return "₹0.00"
        
        return f"Error {response.status_code}"
            
    except Exception as e:
        return "Error"

# Function to fetch collection percentage
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_collection_percentage(card_id, token):
    """
    Fetch collection percentage from Metabase
    """
    if not token:
        return "N/A"
    
    try:
        headers = {
            "X-Metabase-Session": token,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{METABASE_URL}/api/card/{card_id}/query/json",
            headers=headers,
            json={"parameters": []},
            timeout=45
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                first_row = data[0]
                if isinstance(first_row, dict):
                    value = list(first_row.values())[0] if first_row else None
                else:
                    value = first_row
                
                if value is None:
                    return "0%"
                
                # Format as percentage
                if isinstance(value, (int, float)):
                    return f"{value:.1f}%"
                return str(value)
            
            return "0%"
        
        return "N/A"
            
    except Exception as e:
        return "N/A"

# Function to calculate total from metric values
def parse_metric_value(value_str):
    """Parse formatted metric value back to number"""
    if isinstance(value_str, str):
        if "Error" in value_str or value_str == "Coming Soon":
            return 0
        # Remove currency symbol and spaces
        value_str = value_str.replace('₹', '').replace(',', '').strip()
        # Handle Cr and L suffixes
        if 'Cr' in value_str:
            return float(value_str.replace('Cr', '').strip()) * 10000000
        elif 'L' in value_str:
            return float(value_str.replace('L', '').strip()) * 100000
        else:
            try:
                return float(value_str)
            except:
                return 0
    return 0

def format_total(value):
    """Format total value"""
    if value >= 10000000:  # 1 Crore
        return f"₹{value/10000000:.2f} Cr"
    elif value >= 100000:  # 1 Lakh
        return f"₹{value/100000:.2f} L"
    else:
        return f"₹{value:,.0f}"

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
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    /* Individual Brand Card */
    .brand-card {
        border-radius: 16px;
        padding: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        height: 220px;
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
        margin-bottom: 0.5rem;
    }
    
    .card-label {
        font-size: 1.1rem;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.95);
        text-transform: capitalize;
        letter-spacing: 0.3px;
    }
    
    .card-icon {
        font-size: 1.5rem;
        background: rgba(255, 255, 255, 0.25);
        padding: 0.4rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 40px;
        min-height: 40px;
    }
    
    /* Card Content */
    .card-brand-name {
        font-size: 1.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    
    .card-description {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    
    .card-target {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 500;
        margin-bottom: 0.2rem;
    }
    
    .card-metric {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 1);
        font-weight: 800;
        background: rgba(255, 255, 255, 0.25);
        padding: 0.4rem 0.75rem;
        border-radius: 8px;
        display: inline-block;
        margin-top: 0.3rem;
        margin-right: 0.4rem;
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
        padding: 0 0.4rem;
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
            min-height: 200px;
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
# Force fresh calculation every time - don't cache this
now = datetime.now()
current_date = now.strftime("%d %B %Y")
current_day = now.day
days_in_month = calendar.monthrange(now.year, now.month)[1]
days_left = days_in_month - current_day

# Header
st.markdown(f"""
    <div class="header-section">
        <div class="header-left">
            <div class="main-title">Performance Console</div>
            <div class="title-underline"></div>
        </div>
        <div class="header-right">
            <div class="current-date">📅 {current_date}</div>
            <div class="days-left">⏰ {days_left} days left in month</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Get Metabase token
metabase_token = get_metabase_token()

# Define brand dashboards with colors and Metabase card IDs
# Sorted by target in decreasing order
brand_dashboards = [
    {
        "name": "FundoBaBa",
        "url": "https://tinyurl.com/5n9abwcx",
        "icon": "💼",
        "description": "Mumbai Team",
        "target": "₹25 Cr",
        "target_value": 25,
        "metabase_card_id": 441,
        "pmtd_card_id": 456,
        "collection_card_id": 453,
        "metric_label": "MTD Disb",
        "color": "blue"
    },
    {
        "name": "FastPaise",
        "url": "https://tinyurl.com/59dtjd88",
        "icon": "⚡",
        "description": "Ashutosh",
        "target": "₹18 Cr",
        "target_value": 18,
        "metabase_card_id": 432,
        "pmtd_card_id": 460,
        "collection_card_id": 445,
        "metric_label": "MTD Disb",
        "color": "green"
    },
    {
        "name": "SnapPaisa",
        "url": "https://tinyurl.com/2p9mdevt",
        "icon": "📸",
        "description": "Mumbai Team",
        "target": "₹18 Cr",
        "target_value": 18,
        "metabase_card_id": 437,
        "pmtd_card_id": 464,
        "collection_card_id": 449,
        "metric_label": "MTD Disb",
        "color": "purple"
    },
    {
        "name": "Duniya",
        "url": "https://tinyurl.com/nhzvpuy6",
        "icon": "🌍",
        "description": "Harsh",
        "target": "₹15 Cr",
        "target_value": 15,
        "metabase_card_id": 433,
        "pmtd_card_id": 459,
        "collection_card_id": 444,
        "metric_label": "MTD Disb",
        "color": "blue"
    },
    {
        "name": "Tejas",
        "url": "https://tinyurl.com/29sb8js4",
        "icon": "✨",
        "description": "Nitin",
        "target": "₹15 Cr",
        "target_value": 15,
        "metabase_card_id": 439,
        "pmtd_card_id": 466,
        "collection_card_id": 451,
        "metric_label": "MTD Disb",
        "color": "red"
    },
    {
        "name": "Salary 4 Sure",
        "url": "https://tinyurl.com/bdfdufas",
        "icon": "💸",
        "description": "Vivek & Pranit",
        "target": "₹15 Cr",
        "target_value": 15,
        "metabase_card_id": 436,
        "pmtd_card_id": 463,
        "collection_card_id": 448,
        "metric_label": "MTD Disb",
        "color": "orange"
    },
    {
        "name": "Salary Setu",
        "url": "https://tinyurl.com/2we6eyvf",
        "icon": "💵",
        "description": "Prajwal",
        "target": "₹11 Cr",
        "target_value": 11,
        "metabase_card_id": 443,
        "pmtd_card_id": 458,
        "collection_card_id": 455,
        "metric_label": "MTD Disb",
        "color": "green"
    },
    {
        "name": "Salary Adda",
        "url": "https://tinyurl.com/4cd79c5b",
        "icon": "💳",
        "description": "Asim",
        "target": "₹10 Cr",
        "target_value": 10,
        "metabase_card_id": 442,
        "pmtd_card_id": 457,
        "collection_card_id": 454,
        "metric_label": "MTD Disb",
        "color": "teal"
    },
    {
        "name": "Zepto Finance",
        "url": "https://tinyurl.com/44cj83rw",
        "icon": "⚡",
        "description": "Arvind Jaiswal",
        "target": "₹9 Cr",
        "target_value": 9,
        "metabase_card_id": 440,
        "pmtd_card_id": 467,
        "collection_card_id": 452,
        "metric_label": "MTD Disb",
        "color": "pink"
    },
    {
        "name": "Paisa on Salary",
        "url": "https://tinyurl.com/fpxzjfsk",
        "icon": "💰",
        "description": "Ajay",
        "target": "₹5 Cr",
        "target_value": 5,
        "metabase_card_id": 435,
        "pmtd_card_id": 462,
        "collection_card_id": 447,
        "metric_label": "MTD Disb",
        "color": "teal"
    },
    {
        "name": "Squid Loan",
        "url": "https://tinyurl.com/mphk5xpc",
        "icon": "🦑",
        "description": "Shashikant",
        "target": "₹5 Cr",
        "target_value": 5,
        "metabase_card_id": 438,
        "pmtd_card_id": 465,
        "collection_card_id": 450,
        "metric_label": "MTD Disb",
        "color": "indigo"
    },
    {
        "name": "Jhatpat",
        "url": "https://tinyurl.com/294bc6ns",
        "icon": "🚀",
        "description": "Vivek",
        "target": "₹3 Cr",
        "target_value": 3,
        "metabase_card_id": 434,
        "pmtd_card_id": 461,
        "collection_card_id": 446,
        "metric_label": "MTD Disb",
        "color": "orange"
    }
]

# Fetch all metrics and calculate totals
total_disbursement = 0
total_pmtd_disbursement = 0
brand_metrics = {}
brand_pmtd_metrics = {}
brand_collections = {}

for brand in brand_dashboards:
    # Fetch MTD Disbursement
    if brand['metabase_card_id']:
        metric_value = fetch_metabase_metric_v2(brand['metabase_card_id'], metabase_token)
        brand_metrics[brand['name']] = metric_value
        total_disbursement += parse_metric_value(metric_value)
    else:
        brand_metrics[brand['name']] = "Coming Soon"
    
    # Fetch PMTD Disbursement
    if brand['pmtd_card_id']:
        pmtd_value = fetch_metabase_metric_v2(brand['pmtd_card_id'], metabase_token)
        brand_pmtd_metrics[brand['name']] = pmtd_value
        total_pmtd_disbursement += parse_metric_value(pmtd_value)
    else:
        brand_pmtd_metrics[brand['name']] = "Coming Soon"
    
    # Fetch Collection %
    if brand['collection_card_id']:
        collection_value = fetch_collection_percentage(brand['collection_card_id'], metabase_token)
        brand_collections[brand['name']] = collection_value
    else:
        brand_collections[brand['name']] = "N/A"

# Calculate total target
total_target = sum([brand['target_value'] for brand in brand_dashboards])

# Calculate MoM Growth
mom_growth = total_disbursement - total_pmtd_disbursement
mom_growth_percentage = (mom_growth / total_pmtd_disbursement * 100) if total_pmtd_disbursement > 0 else 0

# Calculate Total MTD Target based on current day
def calculate_mtd_target(current_day, total_target_cr):
    """Calculate MTD Target based on the day of month"""
    total_target_amount = total_target_cr * 10000000  # Convert to rupees
    
    if 1 <= current_day <= 5:
        # 21.83% distributed over 5 days
        mtd_percentage = 21.83 * (current_day / 5) / 100
    elif 6 <= current_day <= 10:
        # 21.83% from days 1-5 + 12.21% distributed from day 6-10
        days_in_bracket = current_day - 5
        mtd_percentage = (21.83 + 12.21 * (days_in_bracket / 5)) / 100
    elif 11 <= current_day <= 15:
        # Previous brackets + 8.73% distributed from day 11-15
        days_in_bracket = current_day - 10
        mtd_percentage = (21.83 + 12.21 + 8.73 * (days_in_bracket / 5)) / 100
    elif 16 <= current_day <= 20:
        # Previous brackets + 8.35% distributed from day 16-20
        days_in_bracket = current_day - 15
        mtd_percentage = (21.83 + 12.21 + 8.73 + 8.35 * (days_in_bracket / 5)) / 100
    elif 21 <= current_day <= 25:
        # Previous brackets + 13.56% distributed from day 21-25
        days_in_bracket = current_day - 20
        mtd_percentage = (21.83 + 12.21 + 8.73 + 8.35 + 13.56 * (days_in_bracket / 5)) / 100
    else:  # 26-30/31
        # Previous brackets + 35.31% distributed from day 26 onwards
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        days_in_bracket = current_day - 25
        total_days_in_bracket = days_in_month - 25
        mtd_percentage = (21.83 + 12.21 + 8.73 + 8.35 + 13.56 + 35.31 * (days_in_bracket / total_days_in_bracket)) / 100
    
    return total_target_amount * mtd_percentage

mtd_target_amount = calculate_mtd_target(current_day, total_target)
mtd_shortfall = mtd_target_amount - total_disbursement

# Calculate percentages
shortfall_percentage = (abs(mtd_shortfall) / mtd_target_amount * 100) if mtd_target_amount > 0 else 0

# Display summary cards in vertical layout (3 columns)
cols = st.columns(3, gap="medium")

# Monthly Goal Status Card
with cols[0]:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    height: 380px;
                    display: flex;
                    flex-direction: column;">
            <div style="font-size: 1.5rem; color: #ffffff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                🌍 Monthly Goal Status
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total Target</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #3b82f6;">₹{total_target} Cr</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">{format_total(total_disbursement)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Achievement</div>
                    <div style="font-size: 2rem; font-weight: 900; color: {'#10b981' if total_disbursement >= total_target * 10000000 else '#f59e0b'};">
                        {(total_disbursement / (total_target * 10000000) * 100):.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Monthly Shortfall Card
with cols[1]:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    height: 380px;
                    display: flex;
                    flex-direction: column;">
            <div style="font-size: 1.5rem; color: #ffffff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                📈 Monthly Shortfall
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Target</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #3b82f6;">{format_total(mtd_target_amount)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">{format_total(total_disbursement)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Shortfall (Amount and %)</div>
                    <div style="font-size: 2rem; font-weight: 900; color: {'#ef4444' if mtd_shortfall > 0 else '#10b981'};">
                        {format_total(abs(mtd_shortfall))}
                    </div>
                    <div style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.8); font-weight: 700; margin-top: 0.3rem;">
                        {'↓' if mtd_shortfall > 0 else '↑'} {shortfall_percentage:.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# MoM Growth Card
with cols[2]:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    height: 380px;
                    display: flex;
                    flex-direction: column;">
            <div style="font-size: 1.5rem; color: #ffffff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                🏆 MoM Growth
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total PMTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #8b5cf6;">{format_total(total_pmtd_disbursement)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">{format_total(total_disbursement)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">MOM Growth (Amount and %)</div>
                    <div style="font-size: 2rem; font-weight: 900; color: {'#10b981' if mom_growth >= 0 else '#ef4444'};">
                        {format_total(abs(mom_growth))}
                    </div>
                    <div style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.8); font-weight: 700; margin-top: 0.3rem;">
                        {'↑' if mom_growth >= 0 else '↓'} {abs(mom_growth_percentage):.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Create brand cards in rows of 4
for i in range(0, len(brand_dashboards), 4):
    cols = st.columns(4, gap="large")
    
    for j in range(4):
        if i + j < len(brand_dashboards):
            brand = brand_dashboards[i + j]
            
            # Use pre-fetched metric values
            metric_value = brand_metrics.get(brand['name'], "Coming Soon")
            collection_value = brand_collections.get(brand['name'], "N/A")
            
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
                                <div class="card-metric">💰 Collection: {collection_value}</div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
    
    # Add spacing between rows
    if i + 4 < len(brand_dashboards):
        st.markdown("<br>", unsafe_allow_html=True)
