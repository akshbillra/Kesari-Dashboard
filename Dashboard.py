import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kesari Immigration", layout="wide")

# logo to base64
def logo_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str

# logo
logo = Image.open("KESARI LOGO.png")  # Use your transparent PNG

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation function
def go_to_dashboard():
    st.session_state.page = "dashboard"

# Landing Page
if st.session_state.page == "home":
    # Centered logo and heading
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{logo_to_base64(logo)}' width='200'/>
            <h1 style='color: #1f4e79;'>Kesari Immigration</h1>
            <p style='font-size: 18px; color: gray;'>Your trusted visa consultancy partner.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### ")
    st.markdown("### ")
    col = st.columns([4, 2, 4])[1]  # Center the button
    with col:
        st.button("➡️ Go to Dashboard", on_click=go_to_dashboard)

# Actual Dashboard 
elif st.session_state.page == "dashboard":
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{logo_to_base64(logo)}' width='120'/></div>", unsafe_allow_html=True)
    st.title("Kesari Immigration Dashboard")
    st.markdown(
    "<title style='text-align: center; color: #1f4e79;'> Kesari Immigration Dashboard</title>",
    unsafe_allow_html=True
)

    st.button("🏠 Home", on_click=lambda: st.session_state.update(page="home"))
    
    # Load data
    df = pd.read_excel("data/Book1.xlsx")
    df.columns = df.columns.str.strip()
    df['Decision'] = df['Decision'].astype(str).str.strip().str.title()
    df['Decision'] = df['Decision'].replace({
        'Approval': 'Approved',
        'Approv': 'Approved',
        'Reject': 'Refused',
        'Pending': 'Decision Pending',
        'Nan': None,
        'Na': None
    })

    # Metrics
    approved = df[df["Decision"] == "Approved"].shape[0]
    Refused = df[df["Decision"] == "Refused"].shape[0]
    pending = df[df["Decision"] == "Decision Pending"].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Approved", approved)
    col2.metric("❌ Refused", Refused)
    col3.metric("⏳ Pending", pending)

    # Sidebar
    st.sidebar.header("🎛️ View Options")
    view_choice = st.sidebar.radio("Select display type:", ["📊 Pie Chart", "📈 Bar Graph",])
    st.subheader("🔍 Decision Analysis")

    if view_choice == "📊 Pie Chart":
        fig = px.pie(df, names='Decision', title='🧮 Decision Breakdown', color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

    elif view_choice == "📈 Bar Graph":
        counts = df['Decision'].value_counts().reset_index()
        counts.columns = ['Decision', 'Count']
        fig = px.bar(counts, x='Decision', y='Count', color='Decision', title='📊 Decision Counts by Type')
        st.plotly_chart(fig, use_container_width=True)

    
