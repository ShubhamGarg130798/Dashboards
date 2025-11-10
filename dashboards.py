import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Brand Dashboards",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #1f77b4;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# App header
st.title("📊 Brand Dashboards Portal")
st.markdown("### Access dashboards for all your brands")
st.markdown("---")

# Define your brand dashboards here
# Format: {"Brand Name": "Dashboard URL"}
brand_dashboards = {
    "Brand A": "https://your-brand-a-dashboard.com",
    "Brand B": "https://your-brand-b-dashboard.com",
    "Brand C": "https://your-brand-c-dashboard.com",
    "Brand D": "https://your-brand-d-dashboard.com",
}

# Display dashboards in a grid layout
st.subheader("Select a brand to view its dashboard:")
st.markdown("")

# Create columns for grid layout (3 columns per row)
cols_per_row = 3
brands = list(brand_dashboards.items())

for i in range(0, len(brands), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        if i + j < len(brands):
            brand_name, url = brands[i + j]
            with col:
                if st.button(f"📈 {brand_name}", key=brand_name, use_container_width=True):
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)
                    st.success(f"Opening {brand_name} dashboard...")

# Alternative: Quick links section
st.markdown("---")
with st.expander("📎 Quick Links (Click to open in new tab)"):
    cols = st.columns(2)
    for idx, (name, url) in enumerate(brand_dashboards.items()):
        with cols[idx % 2]:
            st.markdown(f"**[🔗 {name} Dashboard]({url})**")

# Footer
st.markdown("---")
st.caption("Brand Dashboards Portal | Built with Streamlit 🎈")
