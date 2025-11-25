import streamlit as st
from datetime import datetime
import calendar
import requests
import time
from zoneinfo import ZoneInfo

# PASSWORD PROTECTION
PASSWORD = "nbfcsecure123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password to access dashboard:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.success("Access granted. Welcome!")
        st.rerun()
    elif password:
        st.error("Incorrect password")
    st.stop()

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
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    .kpi-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .brand-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .brand-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
        padding: 8px;
        background: #f8f9fa;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Get current date and calculate days left in month
# Force fresh calculation every time - don't cache this
# Use IST timezone explicitly
ist_timezone = ZoneInfo("Asia/Kolkata")
now = datetime.now(ist_timezone)
current_date = now.strftime("%d %B %Y")
current_day = now.day
days_in_month = calendar.monthrange(now.year, now.month)[1]
days_left = days_in_month - current_day

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
        "secondary_mtd_card_id": 476,
        "pmtd_card_id": 467,
        "secondary_pmtd_card_id": 477,
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
    },
    {
        "name": "Minutes Loan",
        "url": "https://tinyurl.com/yj3mss22",
        "icon": "⏱️",
        "description": "Pranit",
        "target": "₹3 Cr",
        "target_value": 3,
        "metabase_card_id": 470,
        "pmtd_card_id": None,
        "collection_card_id": None,
        "metric_label": "MTD Disb",
        "color": "indigo"
    },
    {
        "name": "Paisa Pop",
        "url": "https://tinyurl.com/4jd65fut",
        "icon": "🎈",
        "description": "Priyanka",
        "target": "₹3 Cr",
        "target_value": 3,
        "metabase_card_id": 473,
        "pmtd_card_id": 474,
        "collection_card_id": None,
        "metric_label": "MTD Disb",
        "color": "pink"
    },
    {
        "name": "Qua Loans",
        "url": "https://tinyurl.com/bdhj328e",
        "icon": "🔷",
        "description": "Harsha & Nitin",
        "target": "₹3 Cr",
        "target_value": 3,
        "metabase_card_id": 479,
        "pmtd_card_id": 480,
        "collection_card_id": None,
        "metric_label": "MTD Disb",
        "color": "blue"
    },
    {
        "name": "Salary 4 You",
        "url": "https://tinyurl.com/p43ptyp4",
        "icon": "💵",
        "description": "Nadeem",
        "target": "₹3 Cr",
        "target_value": 3,
        "metabase_card_id": 486,
        "pmtd_card_id": 488,
        "collection_card_id": 491,
        "metric_label": "MTD Disb",
        "color": "green"
    },
    {
        "name": "Udhaar Portal",
        "url": "https://tinyurl.com/wb6n38dx",
        "icon": "🏦",
        "description": "Manas",
        "target": "₹1 Cr",
        "target_value": 1,
        "metabase_card_id": 498,
        "pmtd_card_id": 500,
        "collection_card_id": 499,
        "metric_label": "MTD Disb",
        "color": "teal"
    },
    {
        "name": "Rupee Hype",
        "url": "https://tinyurl.com/39ztaew8",
        "icon": "🚀",
        "description": "Nadeem",
        "target": "₹1 Cr",
        "target_value": 1,
        "metabase_card_id": 485,
        "pmtd_card_id": 487,
        "collection_card_id": 492,
        "metric_label": "MTD Disb",
        "color": "purple"
    }
]

# Fetch all metrics and calculate totals
total_disbursement = 0
total_pmtd_disbursement = 0
brand_metrics = {}
brand_pmtd_metrics = {}
brand_collections = {}
brand_yet_to_achieve = {}

for brand in brand_dashboards:
    # Fetch MTD Disbursement
    if brand['metabase_card_id']:
        metric_value = fetch_metabase_metric_v2(brand['metabase_card_id'], metabase_token)
        mtd_disb_value = parse_metric_value(metric_value)
        
        # Add secondary MTD card if exists (for Zepto Finance)
        if brand.get('secondary_mtd_card_id'):
            secondary_metric_value = fetch_metabase_metric_v2(brand['secondary_mtd_card_id'], metabase_token)
            mtd_disb_value += parse_metric_value(secondary_metric_value)
        
        # Store the combined formatted value for display
        brand_metrics[brand['name']] = format_total(mtd_disb_value)
        total_disbursement += mtd_disb_value
        
        # Calculate Yet to Achieve
        target_value = brand['target_value'] * 10000000  # Convert Cr to rupees
        yet_to_achieve = target_value - mtd_disb_value
        yet_to_achieve_pct = (yet_to_achieve / target_value * 100) if target_value > 0 else 0
        
        if yet_to_achieve > 0:
            brand_yet_to_achieve[brand['name']] = f"{format_total(yet_to_achieve)} ({yet_to_achieve_pct:.0f}%)"
        else:
            brand_yet_to_achieve[brand['name']] = "Target Achieved! 🎉"
    else:
        brand_metrics[brand['name']] = "Coming Soon"
        brand_yet_to_achieve[brand['name']] = "N/A"
    
    # Fetch PMTD Disbursement
    if brand['pmtd_card_id']:
        pmtd_value = fetch_metabase_metric_v2(brand['pmtd_card_id'], metabase_token)
        pmtd_disb_value = parse_metric_value(pmtd_value)
        
        # Add secondary PMTD card if exists (for Zepto Finance)
        if brand.get('secondary_pmtd_card_id'):
            secondary_pmtd_value = fetch_metabase_metric_v2(brand['secondary_pmtd_card_id'], metabase_token)
            pmtd_disb_value += parse_metric_value(secondary_pmtd_value)
        
        # Store the combined formatted value for display
        brand_pmtd_metrics[brand['name']] = format_total(pmtd_disb_value)
        total_pmtd_disbursement += pmtd_disb_value
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
        # 21.2366% distributed over 5 days
        mtd_percentage = 21.2366 * (current_day / 5) / 100
    elif 6 <= current_day <= 10:
        # 21.2366% from days 1-5 + 11.62% distributed from day 6-10
        days_in_bracket = current_day - 5
        mtd_percentage = (21.2366 + 11.62 * (days_in_bracket / 5)) / 100
    elif 11 <= current_day <= 15:
        # Previous brackets + 8.13% distributed from day 11-15
        days_in_bracket = current_day - 10
        mtd_percentage = (21.2366 + 11.62 + 8.13 * (days_in_bracket / 5)) / 100
    elif 16 <= current_day <= 20:
        # Previous brackets + 7.75% distributed from day 16-20
        days_in_bracket = current_day - 15
        mtd_percentage = (21.2366 + 11.62 + 8.13 + 7.75 * (days_in_bracket / 5)) / 100
    elif 21 <= current_day <= 25:
        # Previous brackets + 12.96% distributed from day 21-25
        days_in_bracket = current_day - 20
        mtd_percentage = (21.2366 + 11.62 + 8.13 + 7.75 + 12.96 * (days_in_bracket / 5)) / 100
    else:  # 26-30/31
        # Previous brackets + 38.3134% distributed from day 26 onwards
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        days_in_bracket = current_day - 25
        total_days_in_bracket = days_in_month - 25
        mtd_percentage = (21.2366 + 11.62 + 8.13 + 7.75 + 12.96 + 38.3134 * (days_in_bracket / total_days_in_bracket)) / 100
    
    return total_target_amount * mtd_percentage

mtd_target_amount = calculate_mtd_target(current_day, total_target)
mtd_shortfall = mtd_target_amount - total_disbursement

# Calculate percentages
shortfall_percentage = (abs(mtd_shortfall) / mtd_target_amount * 100) if mtd_target_amount > 0 else 0

# ========== PREDICTION MODELS ==========

# Calculate predicted month-end disbursement based on current performance

# Method 1: Simple Linear Extrapolation
# Assumes constant daily run rate
daily_avg = total_disbursement / current_day if current_day > 0 else 0
linear_projection = (total_disbursement / current_day * days_in_month) if current_day > 0 else 0

# Method 2: Pattern-Based Prediction (Most Accurate)
# Uses the same bracket distribution pattern with current achievement rate
mtd_target_percentage = 61.6966 if current_day == 25 else (calculate_mtd_target(current_day, 100) / 10000000)
remaining_target_percentage = 100 - mtd_target_percentage
achievement_rate = (total_disbursement / mtd_target_amount) if mtd_target_amount > 0 else 0

# Calculate expected disbursement for remaining days based on pattern
remaining_days_target = (total_target * 10000000) * (remaining_target_percentage / 100)
projected_remaining = remaining_days_target * achievement_rate
pattern_based_projection = total_disbursement + projected_remaining

# Method 3: Weighted Prediction (Conservative)
# Assumes 80% efficiency in remaining days
conservative_projection = total_disbursement + (remaining_days_target * achievement_rate * 0.8)

# Method 4: Optimistic Prediction
# Assumes improvement to 100% target achievement rate
optimistic_projection = total_disbursement + remaining_days_target

# Use pattern-based as primary prediction
projected_month_end = pattern_based_projection

# Calculate projected shortfall
projected_shortfall = (total_target * 10000000) - projected_month_end
projected_achievement_pct = (projected_month_end / (total_target * 10000000) * 100) if total_target > 0 else 0

# SG Score - Shows Projected Month-End
sg_score = format_total(projected_month_end)

# Header
st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 style='color: white; margin: 0; font-size: 36px;'>⭐ SG Score: {sg_score}</h1>
                <p style='color: rgba(255, 255, 255, 0.9); margin: 10px 0 0 0; font-size: 18px;'>Performance Console</p>
            </div>
            <div style='text-align: right;'>
                <p style='color: white; margin: 0; font-size: 18px;'>📅 {current_date}</p>
                <p style='color: rgba(255, 255, 255, 0.9); margin: 5px 0 0 0; font-size: 16px;'>⏰ {days_left} days left in month</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Display summary cards in vertical layout (3 columns)
cols = st.columns(3, gap="medium")

# Monthly Goal Status Card
with cols[0]:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='margin: 0 0 20px 0; font-size: 20px;'>🌍 Monthly Goal Status</h3>
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Total Target</div>
                <div style='font-size: 24px; font-weight: bold;'>₹{total_target} Cr</div>
            </div>
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Total MTD Disbursement</div>
                <div style='font-size: 24px; font-weight: bold;'>{format_total(total_disbursement)}</div>
            </div>
            <div style='background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 8px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Achievement</div>
                <div style='font-size: 28px; font-weight: bold;'>{(total_disbursement / (total_target * 10000000) * 100):.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Monthly Shortfall Card
with cols[1]:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='margin: 0 0 20px 0; font-size: 20px;'>📈 Monthly Shortfall</h3>
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Total MTD Target</div>
                <div style='font-size: 24px; font-weight: bold;'>{format_total(mtd_target_amount)}</div>
            </div>
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Total MTD Disbursement</div>
                <div style='font-size: 24px; font-weight: bold;'>{format_total(total_disbursement)}</div>
            </div>
            <div style='background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 8px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Shortfall (Amount and %)</div>
                <div style='font-size: 22px; font-weight: bold;'>{format_total(abs(mtd_shortfall))}</div>
                <div style='font-size: 20px; font-weight: bold; margin-top: 5px;'>{'↓' if mtd_shortfall > 0 else '↑'} {shortfall_percentage:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# MoM Growth Card
with cols[2]:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='margin: 0 0 20px 0; font-size: 20px;'>🏆 MoM Growth</h3>
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Total PMTD Disbursement</div>
                <div style='font-size: 24px; font-weight: bold;'>{format_total(total_pmtd_disbursement)}</div>
            </div>
            <div style='background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>Total MTD Disbursement</div>
                <div style='font-size: 24px; font-weight: bold;'>{format_total(total_disbursement)}</div>
            </div>
            <div style='background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 8px;'>
                <div style='font-size: 13px; opacity: 0.9; margin-bottom: 5px;'>MOM Growth (Amount and %)</div>
                <div style='font-size: 22px; font-weight: bold;'>{format_total(abs(mom_growth))}</div>
                <div style='font-size: 20px; font-weight: bold; margin-top: 5px;'>{'↑' if mom_growth >= 0 else '↓'} {abs(mom_growth_percentage):.1f}%</div>
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
            yet_to_achieve_value = brand_yet_to_achieve.get(brand['name'], "N/A")
            
            with cols[j]:
                st.markdown(f"""
                    <div class='brand-card'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                            <h3 style='margin: 0; color: #333; font-size: 18px;'>{brand['name']}</h3>
                            <span style='font-size: 32px;'>{brand['icon']}</span>
                        </div>
                        <div style='margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #eee;'>
                            <div style='color: #666; font-size: 13px;'>👤 {brand['description']}</div>
                        </div>
                        <div class='metric-row'>
                            <span style='color: #666; font-size: 13px;'>🎯 Target:</span>
                            <span style='font-weight: bold; color: #333;'>{brand['target']}</span>
                        </div>
                        <div class='metric-row'>
                            <span style='color: #666; font-size: 13px;'>📊 {brand['metric_label']}:</span>
                            <span style='font-weight: bold; color: #667eea;'>{metric_value}</span>
                        </div>
                        <div class='metric-row'>
                            <span style='color: #666; font-size: 13px;'>💰 Collection MTD:</span>
                            <span style='font-weight: bold; color: #28a745;'>{collection_value}</span>
                        </div>
                        <div class='metric-row'>
                            <span style='color: #666; font-size: 13px;'>🎯 Yet to Achieve:</span>
                            <span style='font-weight: bold; color: #f5576c;'>{yet_to_achieve_value}</span>
                        </div>
                        <a href='{brand['url']}' target='_blank' style='display: block; margin-top: 15px; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold; transition: transform 0.2s;'>
                            View Dashboard →
                        </a>
                    </div>
                """, unsafe_allow_html=True)
    
    # Add spacing between rows
    if i + 4 < len(brand_dashboards):
        st.markdown("<br>", unsafe_allow_html=True)
