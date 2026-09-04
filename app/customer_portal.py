import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Enterprise Customer Service Operations Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1f4788; font-weight: bold;}
    .sub-header {font-size: 1.2rem; color: #555; margin-bottom: 2rem;}
    .chat-message {padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;}
    .user-message {background-color: #e3f2fd; border-left: 4px solid #2196f3;}
    .agent-message {background-color: #f5f5f5; border-left: 4px solid #4caf50;}
    .citation {font-size: 0.9rem; color: #666; font-style: italic; margin-top: 0.5rem;}
    .route-badge {display: inline-block; font-size: 0.8rem; padding: 0.1rem 0.6rem; border-radius: 1rem;
                  margin-bottom: 0.4rem; font-weight: bold;}
    .route-knowledge {background-color: #e8f5e9; color: #2e7d32;}
    .route-service {background-color: #fff3e0; color: #e65100;}
    .stButton>button {background-color: #1f4788; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Main UI
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<p class="main-header">🏦 Enterprise Customer Service Operations Portal</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Customer Portal</p>',
                unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Customer Information")
    st.text_input("Customer ID", placeholder="e.g. CUST-1001", key="customer_id_sidebar")
    st.button("View Account Summary", type="secondary", use_container_width=True)
    st.button("View Transactions", type="secondary", use_container_width=True)
    st.button("Open New Service Request", type="secondary", use_container_width=True)

    st.markdown("---")
    st.header("Quick Actions")
    st.button("Go to Representative View", type="primary", use_container_width=True)

# Placeholder for main content area
col1_main, col2_main = st.columns([3, 1])

with col1_main:
    st.markdown("## Welcome to the Customer Portal")
    st.markdown("This is the main area where customer-specific information or actions will be displayed.")
    st.markdown("### Recent Activity")
    st.write("- Transaction 1: Deposit of $1000 on 2023-10-26")
    st.write("- Service Request #12345: Opened on 2023-10-25")
    st.write("- Account Summary Updated on 2023-10-20")

with col2_main:
    st.markdown("### Account Summary")
    st.metric("Current Balance", "$", "12,345.67")
    st.metric("Available Credit", "$", "5,000.00")
    st.metric("Last Login", "2023-10-26 08:30 AM")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9rem;'>
    Enterprise Customer Service Operations Portal | Customer Portal Layout
</div>
""", unsafe_allow_html=True)
