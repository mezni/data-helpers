import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Representative Copilot",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for dark theme and layout ---
st.markdown(
    """
    <style>
    /* General dark theme */
    .reportview-container .main .block-container {{ 
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    .stApp {{ background-color: #1E1E1E; color: #FFFFFF; }}
    header {{ background-color: #2A2A2A; padding: 10px 0;}}
    .css-18e3thc {{ background-color: #2A2A2A;}}
    
    /* Sidebar styling */
    .st-emotion-sidebar {{ background-color: #2A2A2A; }}
    .st-emotion-sidebar .st-emotion-sidebar-item a {{ color: #B0B0B0; }}
    .st-emotion-sidebar .st-emotion-sidebar-item a:hover {{ color: #FFFFFF; }}
    
    /* Card styling */
    .st-emotion-card {{ 
        background-color: #2A2A2A;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    .st-emotion-card h3 {{ color: #64B5F6; }}
    
    /* Button styling */
    .stButton>button {{ 
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        color: #FFFFFF;
    }}
    .stButton>button.primary {{ background-color: #4CAF50; }}
    .stButton>button.secondary {{ background-color: #607D8B; }}

    /* Input styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{ 
        background-color: #3A3A3A;
        border: 1px solid #4A4A4A;
        color: #FFFFFF;
    }}
    .stTextInput label, .stSelectbox label {{ color: #B0B0B0; }}

    </style>
    
    <div style="background-color: #2A2A2A; padding: 20px; border-radius: 8px;">
        <h1 style="color: #64B5F6; text-align: center;">AI Sales Copilot</h1>
        <p style="color: #B0B0B0; text-align: center;">Representative View</p>
    </div>
    
    <div style="height: 30px;"></div> <!-- Spacer -->
    """, unsafe_allow_html=True)

# --- Sidebar for Customer Selection ---
with st.sidebar:
    st.header("Customer")
    customer_options = ["Eleanor Whitfield (P-1001)", "John Doe (P-1002)", "Jane Smith (P-1003)"]
    selected_customer = st.selectbox("Select Customer", customer_options, label_visibility="collapsed")
    st.write(f"**Selected Customer:** {selected_customer}")

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True) # Spacer

    # Example Action Button
    if st.button("Start New Interaction", key="new_interaction_btn", type="secondary", use_container_width=True):
        st.info("Starting new interaction.")

# --- Main Application Layout --- 

# Columns for the main content: Customer Case | Agent System | Decision
col1, col2, col3 = st.columns([1, 2, 1])

# --- Column 1: Customer Case Details ---
with col1:
    st.subheader("CUSTOMER CASE -- P-1001")
    st.markdown("<div class='st-emotion-card'>", unsafe_allow_html=True)
    
    st.text_input("Name", "Eleanor Whitfield", label_visibility="visible")
    st.text_input("Age / Sex", "74 / F", label_visibility="visible")
    st.text_area("Presenting", "Chest tightness, shortness of breath", height=70, label_visibility="visible")
    
    st.subheader("Vitals")
    st.text("HR / BP / RR / SpO2 /")
    st.text("Temp / Pain")
    st.text("104 / 148-92 / 22 / 94% ")
    st.text("37.1C / 6 / 10")

    st.subheader("History")
    st.button("NOT VISIBLE TO AGENT", key="history_btn", type="secondary", use_container_width=True)
    
    st.subheader("Medications")
    st.button("NOT VISIBLE TO AGENT", key="medications_btn", type="secondary", use_container_width=True)
    
    st.subheader("Allergies")
    st.button("NOT VISIBLE TO AGENT", key="allergies_btn", type="secondary", use_container_width=True)
    
    st.subheader("Previous Encounters")
    st.button("NOT VISIBLE TO AGENT", key="previous_encounters_btn", type="secondary", use_container_width=True)

    st.subheader("Available Labs")
    st.text("none listed")
    
    st.subheader("Notes / Documents")
    st.button("NOT VISIBLE TO AGENT", key="notes_btn", type="secondary", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# --- Column 2: Agent System Run Trace ---
with col2:
    st.subheader("AGENT SYSTEM -- RUN TRACE")
    st.markdown("<div class='st-emotion-card'>", unsafe_allow_html=True)
    st.text_input("Run ID", "run_0595ec261c", label_visibility="collapsed")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**Intake**", unsafe_allow_html=True)
    st.write("Loaded record for Eleanor Whitfield (symptoms + vitals only).")
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**Triage**", unsafe_allow_html=True)
    st.write("Urgency classified as MEDIUM.")
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**Knowledge Engineering**", unsafe_allow_html=True)
    st.write("Symptoms + vitals only -- no structured knowledge layer")
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**Context Retrieval**", unsafe_allow_html=True)
    st.write("Generic context bundle only (context engineering disabled).")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**Semantic Resolution**", unsafe_allow_html=True)
    st.write("Resolved concepts: none.")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**Knowledge Retrieval**", unsafe_allow_html=True)
    st.write("Retrieved 0 knowledge document(s).")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("**General Decision Route**", unsafe_allow_html=True)
    st.write("Routed to the single generic decision path; triage urgency was not consulted for routing.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Column 3: Decision ---
with col3:
    st.subheader("DECISION")
    st.markdown("<div class='st-emotion-card'>", unsafe_allow_html=True)
    
    # Urgency and Verification Buttons
    urgency_col1, urgency_col2 = st.columns(2)
    with urgency_col1:
        st.button("URGENCY: MEDIUM", key="urgency_medium", type="primary", use_container_width=True)
    with urgency_col2:
        st.button("VERIFICATION: NOT_RUN", key="verification_not_run", type="secondary", use_container_width=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.subheader("RECOMMENDED NEXT STEP")
    st.write("Reviewed presenting symptoms and vitals (urgency: MEDIUM). Obtain standard labs, monitor, reassess based on clinical judgment.")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.subheader("EVIDENCE")
    st.button("No supporting evidence retrieved", key="no_evidence_btn", type="secondary", use_container_width=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer

    st.subheader("SYSTEM CONFIDENCE")
    st.button("LOW - not yet verified", key="low_confidence_btn", type="secondary", use_container_width=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True) # Spacer

    st.text_input("Run ID", "run_0595ec261c", label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer or Action Buttons ---
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # Spacer at the bottom

# Example of an action button for the representative
if st.button("Suggest Next Best Action", key="suggest_action_btn", type="primary", use_container_width=True):
    st.info("Suggesting next best action... (Backend integration not yet implemented)")
