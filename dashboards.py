import streamlit as st
from datetime import datetime, timedelta
import calendar
import requests
import time
from zoneinfo import ZoneInfo
import hashlib
import json
import os

# PASSWORD PROTECTION
PASSWORD = "nbfcsecure123"
TOKEN_FILE = "auth_tokens.json"

def generate_token():
    timestamp = str(datetime.now().timestamp())
    random_str = os.urandom(16).hex()
    return hashlib.sha256((timestamp + random_str).encode()).hexdigest()

def save_token(token):
    tokens = load_tokens()
    expiry = (datetime.now() + timedelta(days=10)).isoformat()
    tokens[token] = expiry
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def validate_token(token):
    if not token:
        return False
    tokens = load_tokens()
    if token in tokens:
        try:
            expiry = datetime.fromisoformat(tokens[token])
            if datetime.now() < expiry:
                return True
            else:
                del tokens[token]
                with open(TOKEN_FILE, 'w') as f:
                    json.dump(tokens, f)
        except:
            pass
    return False

def clean_expired_tokens():
    tokens = load_tokens()
    now = datetime.now()
    tokens = {k: v for k, v in tokens.items() 
              if datetime.fromisoformat(v) > now}
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

clean_expired_tokens()

query_params = st.query_params
auth_token = query_params.get("auth_token", None)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if auth_token and validate_token(auth_token):
    st.session_state.authenticated = True

if not st.session_state.authenticated:
    password = st.text_input("Enter password to access dashboard:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        new_token = generate_token()
        save_token(new_token)
        st.query_params["auth_token"] = new_token
        st.success("Access granted. Welcome!")
        st.rerun()
    elif password:
        st.error("Incorrect password")
    st.stop()

st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

METABASE_URL = "http://43.205.95.106:3000"
METABASE_USERNAME = "shubham.garg@fintechcloud.in"
METABASE_PASSWORD = "Qwerty@12345"

def get_metabase_token():
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
            return response.json()['id']
        return None
    except:
        return None

def fetch_metabase_data(card_id, token):
    if not token:
        return None
    
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
                    return 0
                
                if isinstance(value, (int, float)):
                    return value
                return 0
            return 0
        return None
    except:
        return None

def format_amount(value):
    if value >= 10000000:
        return f"₹{value/10000000:.2f} Cr"
    elif value >= 100000:
        return f"₹{value/100000:.2f} L"
    else:
        return f"₹{value:,.0f}"

def format_percentage(value):
    if isinstance(value, (int, float)):
        return f"{value:.1f}%"
    return "N/A"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
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
    
    section[data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    .header-section {
        margin-bottom: 3rem;
        padding-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }
    
    .header-left {
        flex: 1;
        text-align: center;
    }
    
    .header-left-score {
        position: absolute;
        left: 3rem;
        top: 2rem;
    }
    
    .sg-score-card {
        font-size: 1rem;
        font-weight: 700;
        color: #2563eb;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 2px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sg-score-value {
        font-size: 1.1rem;
        font-weight: 800;
        color: #1e40af;
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
    
    .brand-card {
        border-radius: 16px;
        padding: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .brand-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .card-blue { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
    .card-green { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
    .card-orange { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
    .card-teal { background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); }
    .card-purple { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }
    .card-indigo { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }
    .card-red { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
    .card-pink { background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); }
    
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
        font-size: 0.88rem;
        color: rgba(255, 255, 255, 1);
        font-weight: 800;
        background: rgba(255, 255, 255, 0.25);
        padding: 0.35rem 0.7rem;
        border-radius: 8px;
        display: inline-block;
        margin-top: 0.25rem;
        margin-right: 0.35rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        line-height: 1.3;
    }
    
    a {
        text-decoration: none !important;
        color: inherit !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    [data-testid="column"] {
        padding: 0 0.4rem;
    }
    
    @media (max-width: 768px) {
        .header-section {
            flex-direction: column;
            gap: 1rem;
        }
        
        .header-left-score {
            position: relative;
            left: auto;
            top: auto;
            margin-bottom: 1rem;
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
        .main-title {
            font-size: 2.5rem;
        }
        .title-underline {
            width: 150px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

ist_timezone = ZoneInfo("Asia/Kolkata")
now = datetime.now(ist_timezone)
current_date = now.strftime("%d %B %Y")
current_day = now.day
days_in_month = calendar.monthrange(now.year, now.month)[1]
days_left = days_in_month - current_day

# Get token
metabase_token = get_metabase_token()

brands = [
    {"name": "FundoBaBa", "url": "https://tinyurl.com/5n9abwcx", "icon": "💼", "description": "Mumbai Team", "target": "₹25 Cr", "target_value": 25, "mtd_card": 441, "pmtd_card": 456, "coll_card": 453, "color": "blue"},
    {"name": "FastPaise", "url": "https://tinyurl.com/59dtjd88", "icon": "⚡", "description": "Ashutosh", "target": "₹18 Cr", "target_value": 18, "mtd_card": 432, "pmtd_card": 460, "coll_card": 445, "color": "green"},
    {"name": "SnapPaisa", "url": "https://tinyurl.com/2p9mdevt", "icon": "📸", "description": "Mumbai Team", "target": "₹18 Cr", "target_value": 18, "mtd_card": 437, "pmtd_card": 464, "coll_card": 449, "color": "purple"},
    {"name": "BlinkR", "url": "", "icon": "⚡", "description": "Anurag", "target": "₹15 Cr", "target_value": 15, "manual_mtd": 65049130, "manual_pmtd": 49800000, "manual_coll": 83.0, "color": "indigo"},
    {"name": "Duniya", "url": "https://tinyurl.com/nhzvpuy6", "icon": "🌍", "description": "Harsh", "target": "₹15 Cr", "target_value": 15, "mtd_card": 433, "pmtd_card": 459, "coll_card": 444, "color": "blue"},
    {"name": "Tejas", "url": "https://tinyurl.com/29sb8js4", "icon": "✨", "description": "Nitin", "target": "₹15 Cr", "target_value": 15, "mtd_card": 439, "pmtd_card": 466, "coll_card": 451, "color": "red"},
    {"name": "Salary 4 Sure", "url": "https://tinyurl.com/bdfdufas", "icon": "💸", "description": "Vivek & Pranit", "target": "₹15 Cr", "target_value": 15, "mtd_card": 436, "pmtd_card": 463, "coll_card": 448, "color": "orange"},
    {"name": "Salary Setu", "url": "https://tinyurl.com/2we6eyvf", "icon": "💵", "description": "Prajwal", "target": "₹11 Cr", "target_value": 11, "mtd_card": 443, "pmtd_card": 458, "coll_card": 455, "color": "green"},
    {"name": "Salary Adda", "url": "https://tinyurl.com/4cd79c5b", "icon": "💳", "description": "Asim", "target": "₹10 Cr", "target_value": 10, "mtd_card": 442, "pmtd_card": 457, "coll_card": 454, "color": "teal"},
    {"name": "Zepto Finance", "url": "https://tinyurl.com/44cj83rw", "icon": "⚡", "description": "Arvind Jaiswal", "target": "₹9 Cr", "target_value": 9, "mtd_card": 440, "mtd_card2": 476, "pmtd_card": 467, "pmtd_card2": 477, "coll_card": 452, "color": "pink"},
    {"name": "Paisa on Salary", "url": "https://tinyurl.com/fpxzjfsk", "icon": "💰", "description": "Ajay", "target": "₹5 Cr", "target_value": 5, "mtd_card": 435, "pmtd_card": 462, "coll_card": 447, "color": "teal"},
    {"name": "Squid Loan", "url": "https://tinyurl.com/mphk5xpc", "icon": "🦑", "description": "Shashikant", "target": "₹5 Cr", "target_value": 5, "mtd_card": 438, "pmtd_card": 465, "coll_card": 450, "color": "indigo"},
    {"name": "Jhatpat", "url": "https://tinyurl.com/294bc6ns", "icon": "🚀", "description": "Vivek", "target": "₹3 Cr", "target_value": 3, "mtd_card": 434, "pmtd_card": 461, "coll_card": 446, "color": "orange"},
    {"name": "Minutes Loan", "url": "https://tinyurl.com/yj3mss22", "icon": "⏱️", "description": "Pranit", "target": "₹3 Cr", "target_value": 3, "mtd_card": 470, "pmtd_card": 471, "color": "indigo"},
    {"name": "Paisa Pop", "url": "https://tinyurl.com/4jd65fut", "icon": "🎈", "description": "Priyanka", "target": "₹3 Cr", "target_value": 3, "mtd_card": 473, "pmtd_card": 474, "color": "pink"},
    {"name": "Qua Loans", "url": "https://tinyurl.com/bdhj328e", "icon": "🔷", "description": "Harsha & Nitin", "target": "₹3 Cr", "target_value": 3, "manual_mtd": 26458000, "manual_pmtd": 14700000, "manual_coll": 74.0, "color": "blue"},
    {"name": "Salary 4 You", "url": "https://tinyurl.com/p43ptyp4", "icon": "💵", "description": "Nadeem", "target": "₹3 Cr", "target_value": 3, "mtd_card": 486, "pmtd_card": 488, "coll_card": 491, "color": "green"},
    {"name": "Udhaar Portal", "url": "https://tinyurl.com/wb6n38dx", "icon": "🏦", "description": "Manas", "target": "₹1 Cr", "target_value": 1, "mtd_card": 498, "pmtd_card": 500, "coll_card": 499, "color": "teal"},
    {"name": "Rupee Hype", "url": "https://tinyurl.com/39ztaew8", "icon": "🚀", "description": "Nadeem", "target": "₹1 Cr", "target_value": 1, "mtd_card": 485, "pmtd_card": 487, "coll_card": 492, "color": "purple"}
]

total_mtd = 0
total_pmtd = 0
brand_data = {}

for brand in brands:
    if "manual_mtd" in brand:
        mtd = brand["manual_mtd"]
        pmtd = brand.get("manual_pmtd", 0)
        coll = brand.get("manual_coll", None)
    else:
        mtd_val = fetch_metabase_data(brand.get("mtd_card"), metabase_token)
        mtd = mtd_val if mtd_val is not None else 0
        
        if "mtd_card2" in brand:
            mtd2 = fetch_metabase_data(brand["mtd_card2"], metabase_token)
            if mtd2:
                mtd += mtd2
        
        pmtd_val = fetch_metabase_data(brand.get("pmtd_card"), metabase_token)
        pmtd = pmtd_val if pmtd_val is not None else 0
        
        if "pmtd_card2" in brand:
            pmtd2 = fetch_metabase_data(brand["pmtd_card2"], metabase_token)
            if pmtd2:
                pmtd += pmtd2
        
        coll = fetch_metabase_data(brand.get("coll_card"), metabase_token)
    
    total_mtd += mtd
    total_pmtd += pmtd
    
    target_amt = brand["target_value"] * 10000000
    yet_to_achieve = target_amt - mtd
    yet_pct = (yet_to_achieve / target_amt * 100) if target_amt > 0 else 0
    
    brand_data[brand["name"]] = {
        "mtd": mtd,
        "pmtd": pmtd,
        "coll": coll,
        "yet": yet_to_achieve if yet_to_achieve > 0 else 0,
        "yet_pct": yet_pct if yet_to_achieve > 0 else 0
    }

total_target = sum([b["target_value"] for b in brands]) * 10000000
mom_growth = total_mtd - total_pmtd
mom_pct = (mom_growth / total_pmtd * 100) if total_pmtd > 0 else 0

def calc_mtd_target(day, target):
    if 1 <= day <= 5:
        return target * 21.23 * (day / 5) / 100
    elif 6 <= day <= 10:
        return target * (21.23 + 11.61 * ((day - 5) / 5)) / 100
    elif 11 <= day <= 15:
        return target * (21.23 + 11.61 + 8.13 * ((day - 10) / 5)) / 100
    elif 16 <= day <= 20:
        return target * (21.23 + 11.61 + 8.13 + 7.75 * ((day - 15) / 5)) / 100
    elif 21 <= day <= 25:
        return target * (21.23 + 11.61 + 8.13 + 7.75 + 12.96 * ((day - 20) / 5)) / 100
    else:
        days_in_mo = calendar.monthrange(now.year, now.month)[1]
        return target * (21.23 + 11.61 + 8.13 + 7.75 + 12.96 + 38.31 * ((day - 25) / (days_in_mo - 25))) / 100

mtd_target = calc_mtd_target(current_day, total_target)
shortfall = mtd_target - total_mtd
shortfall_pct = (abs(shortfall) / mtd_target * 100) if mtd_target > 0 else 0

st.markdown(f"""
    <div class="header-section">
        <div class="header-left-score">
            <div class="sg-score-card">
                <span>⭐ Month-End Projection:</span>
                <span class="sg-score-value">₹137 Cr</span>
            </div>
        </div>
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

cols = st.columns(3, gap="medium")

with cols[0]:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border-radius: 20px; padding: 2rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.1); height: 380px; display: flex; flex-direction: column;">
            <div style="font-size: 1.5rem; color: #ffffff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                🌍 Monthly Goal Status
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total Target</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #3b82f6;">{format_amount(total_target)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">{format_amount(total_mtd)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Achievement</div>
                    <div style="font-size: 2rem; font-weight: 900; color: {'#10b981' if total_mtd >= total_target else '#f59e0b'};">
                        {(total_mtd / total_target * 100):.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with cols[1]:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border-radius: 20px; padding: 2rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.1); height: 380px; display: flex; flex-direction: column;">
            <div style="font-size: 1.5rem; color: #ffffff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                📈 Monthly Shortfall
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Target</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #3b82f6;">{format_amount(mtd_target)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">{format_amount(total_mtd)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Shortfall (Amount and %)</div>
                    <div style="font-size: 2rem; font-weight: 900; color: {'#ef4444' if shortfall > 0 else '#10b981'};">
                        {format_amount(abs(shortfall))}
                    </div>
                    <div style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.8); font-weight: 700; margin-top: 0.3rem;">
                        {'↓' if shortfall > 0 else '↑'} {shortfall_pct:.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with cols[2]:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border-radius: 20px; padding: 2rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.1); height: 380px; display: flex; flex-direction: column;">
            <div style="font-size: 1.5rem; color: #ffffff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                🏆 MoM Growth
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total PMTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #8b5cf6;">{format_amount(total_pmtd)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">Total MTD Disbursement</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">{format_amount(total_mtd)}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); font-weight: 600;">MOM Growth (Amount and %)</div>
                    <div style="font-size: 2rem; font-weight: 900; color: {'#10b981' if mom_growth >= 0 else '#ef4444'};">
                        {format_amount(abs(mom_growth))}
                    </div>
                    <div style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.8); font-weight: 700; margin-top: 0.3rem;">
                        {'↑' if mom_growth >= 0 else '↓'} {abs(mom_pct):.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

for i in range(0, len(brands), 4):
    cols = st.columns(4, gap="large")
    
    for j in range(4):
        if i + j < len(brands):
            brand = brands[i + j]
            data = brand_data[brand["name"]]
            
            yet_text = f"{format_amount(data['yet'])} ({data['yet_pct']:.0f}%)" if data['yet'] > 0 else "Target Achieved! 🎉"
            coll_text = format_percentage(data['coll']) if data['coll'] is not None else "N/A"
            
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
                                <div style="display: flex; flex-wrap: wrap; gap: 0.25rem; margin-top: 0.3rem;">
                                    <div class="card-metric">📊 MTD Disb: {format_amount(data['mtd'])}</div>
                                    <div class="card-metric">💰 Collection MTD: {coll_text}</div>
                                </div>
                                <div style="margin-top: 0.25rem;">
                                    <div class="card-metric">🎯 Yet to Achieve: {yet_text}</div>
                                </div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
    
    if i + 4 < len(brands):
        st.markdown("<br>", unsafe_allow_html=True)
