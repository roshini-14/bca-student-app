"""
=============================================================================
BCA Class Management and Topper Finder Web Application
=============================================================================
Academic Year 2024–2027 | Department of Computer Applications
f"Batch: {len(df)} Students | 5 Core Subjects (CIA 1, CIA 2, Model Exam each)

Subjects & Faculty Mapping:
1. Fundamentals of Algorithm       -> T. Nagarathinam (Assoc. Prof & HOD i/c)
2. Mobile Application Development   -> A. Narayanan (Asst. Prof)
3. Computer Networks                -> K. Prakash (Assoc. Prof)
4. Web Technology                   -> V. Bhuvaneshwari (Asst. Prof)
5. Data Mining and Warehouse        -> S. Srinath (Asst. Prof)

Technology Stack: Python, Streamlit, Pandas, Plotly, Hugging Face Hub
=============================================================================
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_student_email(student_email, student_name, marks, fees, status):
    SENDER_EMAIL = "roshinikalidoss@gmail.com"
    SENDER_PASSWORD = "odng licd pnxl tfed"
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = student_email
    msg['Subject'] = f"Academic & Fee Alert: {student_name}"
    
    body = f"Hello {student_name},\n\nStatus: {status}\nMarks: {marks}\nFees Due: {fees}\n\nPlease take necessary action."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Port 465 use panrathu romba stable-ah irukkum
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, student_email, msg.as_string())
        server.quit()
        print(f"Email successfully sent to {student_email}")
    except Exception as e:
        print(f"Email failed: {e}")
import os
import urllib.parse
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Faculty details and chatbot engine
from teachers_data import TEACHERS, SUBJECT_MAP
from chatbot_helper import ask_huggingface_assistant, query_local_engine

# ---------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="BCA Class Management & Topper Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Top Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        border-radius: 16px;
        padding: 24px 30px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
    }
    .hero-banner h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 6px;
        color: #ffffff;
    }
    .hero-banner p {
        font-size: 1.02rem;
        color: #e0f2fe;
        margin-bottom: 0px;
    }

    /* Metric Cards */
    .kpi-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    .kpi-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 700;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Topper Gold Showcase Card */
    .overall-topper-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 40%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.25);
    }
    .overall-topper-badge {
        display: inline-block;
        background: #d97706;
        color: #ffffff;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 5px 14px;
        border-radius: 999px;
        margin-bottom: 10px;
    }
    .overall-topper-name {
        font-size: 2.1rem;
        font-weight: 800;
        color: #78350f;
        margin-bottom: 4px;
    }
    .overall-topper-meta {
        font-size: 1.05rem;
        color: #92400e;
        font-weight: 600;
    }

    /* Subject Topper Card */
    .subj-topper-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    .subj-topper-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #6366f1);
    }
    .subj-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #4338ca;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        margin-bottom: 6px;
    }
    .subj-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e293b;
    }
    .subj-faculty {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 8px;
    }
    .subj-student {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0f172a;
    }
    .subj-score {
        display: inline-block;
        background: #ecfdf5;
        color: #047857;
        font-weight: 800;
        font-size: 0.95rem;
        padding: 4px 10px;
        border-radius: 8px;
        margin-top: 8px;
    }

    /* Faculty Card */
    .faculty-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }
    .faculty-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07);
    }
    .faculty-pill {
        display: inline-block;
        background: #ede9fe;
        color: #6d28d9;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .faculty-name {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0f172a;
    }
    .faculty-desig {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 10px;
    }

    /* Phone Mockup */
    .phone-mockup {
        background: #0f172a;
        border-radius: 24px;
        padding: 16px;
        color: white;
        max-width: 420px;
        margin: 0 auto;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
        border: 4px solid #334155;
    }
    .phone-screen {
        background: #f8fafc;
        border-radius: 16px;
        padding: 16px;
        color: #1e293b;
        min-height: 250px;
    }
    .sms-bubble {
        background: #3b82f6;
        color: white;
        border-radius: 16px 16px 2px 16px;
        padding: 12px 16px;
        font-size: 0.88rem;
        line-height: 1.45;
        margin-top: 10px;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    .sms-sender {
        font-size: 0.75rem;
        color: #94a3b8;
        font-weight: 600;
        text-align: center;
        margin-bottom: 6px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 3. DATA LOADING & CACHING
# ---------------------------------------------------------------------------
@st.cache_data
def load_student_data():
    """Load the official BCA 57-student dataset from CSV with 5 subjects."""
    csv_path = os.path.join(os.path.dirname(__file__), "bca_students_new.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # Fallback to generating fresh data
        from generate_data import df as fresh_df
        df = fresh_df.copy()

    # Recalculate subject totals (out of 300 each)
    df["FOA_Total"] = df["FOA_CIA1"] + df["FOA_CIA2"] + df["FOA_Model"]
    df["MAD_Total"] = df["MAD_CIA1"] + df["MAD_CIA2"] + df["MAD_Model"]
    df["CN_Total"]  = df["CN_CIA1"]  + df["CN_CIA2"]  + df["CN_Model"]
    df["WT_Total"]  = df["WT_CIA1"]  + df["WT_CIA2"]  + df["WT_Model"]
    df["DMW_Total"] = df["DMW_CIA1"] + df["DMW_CIA2"] + df["DMW_Model"]

    # Exam totals across 5 subjects (out of 500 each)
    df["Total_CIA1"] = df["FOA_CIA1"] + df["MAD_CIA1"] + df["CN_CIA1"] + df["WT_CIA1"] + df["DMW_CIA1"]
    df["Total_CIA2"] = df["FOA_CIA2"] + df["MAD_CIA2"] + df["CN_CIA2"] + df["WT_CIA2"] + df["DMW_CIA2"]
    df["Total_Model"] = df["FOA_Model"] + df["MAD_Model"] + df["CN_Model"] + df["WT_Model"] + df["DMW_Model"]

    # Grand total and percentage (out of 1500)
    df["Overall_Total"] = df["FOA_Total"] + df["MAD_Total"] + df["CN_Total"] + df["WT_Total"] + df["DMW_Total"]
    df["Overall_Percentage"] = (df["Overall_Total"] / 1500.0) * 100.0

    # Class rank
    df["Rank"] = df["Overall_Total"].rank(ascending=False, method="min").astype(int)
    return df

# Initialize session state for persistent data
if "students_df" not in st.session_state:
    st.session_state.students_df = load_student_data()

if "sms_log" not in st.session_state:
    st.session_state.sms_log = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "👋 **Welcome to the BCA AI Assistant!** Ask me about class toppers, subject-wise marks across all 5 subjects, fee statuses, or faculty details."
        }
    ]

# Shortcut dataframe
df = st.session_state.students_df.copy()
# Ensure Rank is calculated
df["Rank"] = df["Overall_Total"].rank(ascending=False, method="min").astype(int)

# ---------------------------------------------------------------------------
# 4. SIDEBAR: NAVIGATION, FILTERS & HUGGING FACE SETTINGS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/identicon/svg?seed=BCA5Subjects", width=65)
    st.title("🎓 BCA Portal")
    st.caption(f"{len(df)} Students • 5 Core Subjects • 3 Exams Each")
    st.markdown("---")

    app_section = st.radio(
        "📌 Navigate To:",
        [
            "🏠 Dashboard Overview",
            "🏆 Topper Analysis",
            "📋 Student Directory",
            "⚠️ Fee & Low Mark Alerts",
            "👨‍🏫 Faculty & Subjects",
            "📊 Analytics & Charts",
            "🤖 AI Assistant (Hugging Face)"
        ],
        index=0
    )

    st.markdown("---")

    # Hugging Face Settings Expander
    with st.expander("🤗 Hugging Face AI Settings", expanded=False):
        st.write("Connect to Hugging Face Inference API for live generative AI responses:")
        hf_token_input = st.text_input(
            "Hugging Face User Access Token:",
            type="password",
            value=st.session_state.get("hf_token", ""),
            placeholder="hf_xxxxxxxxxxxxxxxx",
            help="Free token from huggingface.co/settings/tokens. Leave blank to use Fast Local BCA Smart Engine."
        )
        if hf_token_input != st.session_state.get("hf_token", ""):
            st.session_state.hf_token = hf_token_input

        hf_model_choice = st.selectbox(
            "LLM Model:",
            [
                "Qwen/Qwen2.5-7B-Instruct",
                "meta-llama/Llama-3.2-3B-Instruct",
                "mistralai/Mistral-7B-Instruct-v0.3",
                "HuggingFaceH4/zephyr-7b-beta"
            ],
            index=0
        )
        st.session_state.hf_model = hf_model_choice

        if st.session_state.get("hf_token"):
            st.success("✨ Hugging Face API Mode: Active")
        else:
            st.info("⚡ Mode: Local BCA Smart Engine (Instant & offline ready)")

    st.markdown("---")

    # Quick summary of 5 subjects
    st.markdown("### 📚 5 Core Subjects")
    for t in TEACHERS:
        st.caption(f"• **{t['short_name']}** (`{t['subject_code']}`): {t['teacher_name']}")
    st.markdown("---")
    st.caption("🛡️ BCA Academic Portal | Python & Streamlit")


# ---------------------------------------------------------------------------
# 5. TOP HERO BANNER & KPI METRICS
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>🎓 BCA Class Management & Topper Finder</h1>
            <p>{len(df)} Students • 5 Core Subjects (Algorithm, MAD, Networks, Web Tech, Data Mining) • CIA 1, CIA 2 & Model Exams</p>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 999px; font-weight: 700; font-size: 0.85rem;">
                🚀 Streamlit + Hugging Face AI
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Metrics calculation
total_students = len(df)
overall_top_idx = df["Overall_Total"].idxmax()
overall_topper = df.loc[overall_top_idx]
overall_max_score = df["Overall_Total"].max()
overall_max_pct = (overall_max_score / 1500.0) * 100.0

class_avg_total = df["Overall_Total"].mean()
class_avg_pct = df["Overall_Percentage"].mean()

fee_pending_count = (df["Fee Status"] == "Pending").sum()
fee_paid_count = (df["Fee Status"] == "Paid").sum()
fee_collection_rate = (fee_paid_count / total_students) * 100

# Exam column names for checking low marks
all_exam_cols = [
    "FOA_CIA1", "FOA_CIA2", "FOA_Model",
    "MAD_CIA1", "MAD_CIA2", "MAD_Model",
    "CN_CIA1", "CN_CIA2", "CN_Model",
    "WT_CIA1", "WT_CIA2", "WT_Model",
    "DMW_CIA1", "DMW_CIA2", "DMW_Model"
]
low_mark_candidates = df[(df[all_exam_cols] < 40).any(axis=1)]
low_mark_count = len(low_mark_candidates)

# 5 KPI Cards
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">👥 Class Strength</div>
        <div class="kpi-value">{total_students}</div>
        <div class="kpi-subtitle">5 Core Subjects</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏆 Overall Topper</div>
        <div class="kpi-value">{overall_max_score}<span style="font-size: 0.95rem; color: #64748b;">/1500</span></div>
        <div class="kpi-subtitle">{overall_topper['Student Name'].split()[0]} ({overall_max_pct:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📈 Class Average</div>
        <div class="kpi-value">{class_avg_pct:.1f}%</div>
        <div class="kpi-subtitle">{class_avg_total:.1f} / 1500 Marks</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Fee Status</div>
        <div class="kpi-value">{fee_pending_count} <span style="font-size: 0.95rem; color: #ef4444; font-weight: 700;">Pending</span></div>
        <div class="kpi-subtitle" style="color: #64748b;">{fee_collection_rate:.1f}% Paid</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">⚠️ Low Mark Alert</div>
        <div class="kpi-value" style="color: #ea580c;">{low_mark_count}</div>
        <div class="kpi-subtitle" style="color: #dc2626;">&lt; 40 in any exam</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)


# ===========================================================================
# SECTION 1: 🏠 DASHBOARD OVERVIEW
# ===========================================================================
if app_section == "🏠 Dashboard Overview":
    st.markdown("## 🏠 BCA Class Dashboard Overview")
    st.write("Unified console tracking academic performance across all 5 core subjects: **Fundamentals of Algorithm**, **Mobile App Dev**, **Computer Networks**, **Web Technology**, and **Data Mining & Warehouse**.")

    col_d1, col_d2 = st.columns([1.1, 0.9])
    
    with col_d1:
        st.markdown(f"""
        <div class="overall-topper-card">
            <span class="overall-topper-badge">🌟 OVERALL CLASS TOPPER (RANK 1) 🌟</span>
            <div class="overall-topper-name">{overall_topper['Student Name']}</div>
            <div class="overall-topper-meta">
                Register No: <strong>{overall_topper['Register Number']}</strong> • Total Marks: <strong>{overall_topper['Overall_Total']} / 1500 ({overall_max_pct:.2f}%)</strong>
            </div>
            <div style="margin-top: 14px; display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: white; padding: 5px 10px; border-radius: 8px; font-weight: 600; font-size: 0.85rem;">
                    🧠 FOA: <strong>{overall_topper['FOA_Total']}/300</strong>
                </span>
                <span style="background: white; padding: 5px 10px; border-radius: 8px; font-weight: 600; font-size: 0.85rem;">
                    📱 MAD: <strong>{overall_topper['MAD_Total']}/300</strong>
                </span>
                <span style="background: white; padding: 5px 10px; border-radius: 8px; font-weight: 600; font-size: 0.85rem;">
                    🌐 CN: <strong>{overall_topper['CN_Total']}/300</strong>
                </span>
                <span style="background: white; padding: 5px 10px; border-radius: 8px; font-weight: 600; font-size: 0.85rem;">
                    💻 WT: <strong>{overall_topper['WT_Total']}/300</strong>
                </span>
                <span style="background: white; padding: 5px 10px; border-radius: 8px; font-weight: 600; font-size: 0.85rem;">
                    📦 DMW: <strong>{overall_topper['DMW_Total']}/300</strong>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 Subject Toppers Snapshot")
        s_cols = st.columns(5)
        
        # 5 Subject Toppers mini summary
        subjs_info = [
            ("FOA", "FOA_Total", "Algorithm", "T. Nagarathinam"),
            ("MAD", "MAD_Total", "Mobile App", "A. Narayanan"),
            ("CN",  "CN_Total",  "Networks",   "K. Prakash"),
            ("WT",  "WT_Total",  "Web Tech",   "V. Bhuvaneshwari"),
            ("DMW", "DMW_Total", "Data Mining", "S. Srinath"),
        ]
        
        for idx, (sid, tot_col, sname, fname) in enumerate(subjs_info):
            stop_idx = df[tot_col].idxmax()
            stop_row = df.loc[stop_idx]
            with s_cols[idx]:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                    <div style="font-size: 0.72rem; color: #3b82f6; font-weight: 700;">{sid}</div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #0f172a; margin-top: 2px;">{stop_row['Student Name'].split()[0]}</div>
                    <div style="font-size: 0.82rem; font-weight: 700; color: #059669; margin-top: 4px;">{stop_row[tot_col]}/300</div>
                    <div style="font-size: 0.68rem; color: #64748b; margin-top: 2px;">{fname.split()[-1]}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_d2:
        st.markdown("### 🔔 Important Action Alerts")
        st.warning(
            f"**💰 {fee_pending_count} Students have Pending Fees**\n\n"
            "Action required: Send fee clearance reminders via the Fee Alert section."
        )
        st.error(
            f"**⚠️ {low_mark_count} Students scored &lt; 40 in CIA/Model Exams**\n\n"
            "Action required: Remedial coaching and parent intimation needed."
        )

        st.markdown("### 👨‍🏫 Faculty & Subject Roster")
        for t in TEACHERS:
            st.markdown(
                f"- **{t['subject_name']}**: `{t['teacher_name']}` ({t['cabin']})"
            )


# ===========================================================================
# SECTION 2: 🏆 DETAILED TOPPER ANALYSIS
# ===========================================================================
elif app_section == "🏆 Topper Analysis":
    st.markdown("## 🏆 Detailed BCA Class Topper Analysis")
    st.write("Complete rankings and topper breakdowns: **Overall Class Topper**, **Subject-wise Toppers**, and **Exam-wise Toppers** across all 5 subjects.")

    # 1. Overall Topper Showcase Card
    st.markdown(f"""
    <div class="overall-topper-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <span class="overall-topper-badge">🥇 OVERALL CLASS TOPPER (RANK 1)</span>
                <div class="overall-topper-name">{overall_topper['Student Name']}</div>
                <div class="overall-topper-meta">
                    Register Number: <strong>{overall_topper['Register Number']}</strong> | Mobile: <strong>{overall_topper['Mobile Number']}</strong> | Fee Status: <strong>{overall_topper['Fee Status']}</strong>
                </div>
            </div>
            <div style="text-align: right; margin-top: 10px;">
                <div style="font-size: 2.7rem; font-weight: 900; color: #b45309; line-height: 1;">
                    {overall_topper['Overall_Total']} <span style="font-size: 1.3rem; color: #92400e;">/ 1500</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #78350f;">
                    {overall_max_pct:.2f}% (Distinction)
                </div>
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid #fde68a; margin: 14px 0;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px;">
            <div style="background: rgba(255,255,255,0.7); padding: 8px 12px; border-radius: 8px;">
                🧠 <strong>Algorithm:</strong> {overall_topper['FOA_Total']}/300
            </div>
            <div style="background: rgba(255,255,255,0.7); padding: 8px 12px; border-radius: 8px;">
                📱 <strong>Mobile App:</strong> {overall_topper['MAD_Total']}/300
            </div>
            <div style="background: rgba(255,255,255,0.7); padding: 8px 12px; border-radius: 8px;">
                🌐 <strong>Networks:</strong> {overall_topper['CN_Total']}/300
            </div>
            <div style="background: rgba(255,255,255,0.7); padding: 8px 12px; border-radius: 8px;">
                💻 <strong>Web Tech:</strong> {overall_topper['WT_Total']}/300
            </div>
            <div style="background: rgba(255,255,255,0.7); padding: 8px 12px; border-radius: 8px;">
                📦 <strong>Data Mining:</strong> {overall_topper['DMW_Total']}/300
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Individual Subject Toppers (5 Specific Subjects)
    st.markdown("### 📚 Individual Subject Toppers (Across CIA 1, CIA 2 & Model)")
    subj_cols = st.columns(5)

    subjs_topper_def = [
        ("FOA", "FOA_Total", "Fundamentals of Algorithm", "T. Nagarathinam", "BCA401"),
        ("MAD", "MAD_Total", "Mobile Application Dev", "A. Narayanan", "BCA402"),
        ("CN",  "CN_Total",  "Computer Networks", "K. Prakash", "BCA403"),
        ("WT",  "WT_Total",  "Web Technology", "V. Bhuvaneshwari", "BCA404"),
        ("DMW", "DMW_Total", "Data Mining & Warehouse", "S. Srinath", "BCA405")
    ]

    for idx, (sid, tot_col, sname, fname, scode) in enumerate(subjs_topper_def):
        m_val = df[tot_col].max()
        s_top = df[df[tot_col] == m_val].iloc[0]
        with subj_cols[idx]:
            st.markdown(f"""
            <div class="subj-topper-card">
                <span class="subj-badge">{scode} • {sid}</span>
                <div class="subj-name">{sname}</div>
                <div class="subj-faculty">👨‍🏫 {fname}</div>
                <hr style="margin: 8px 0; border: 0; border-top: 1px solid #f1f5f9;">
                <div style="font-size: 0.75rem; color: #64748b;">Topper:</div>
                <div class="subj-student">{s_top['Student Name']}</div>
                <div style="font-size: 0.8rem; color: #64748b;">{s_top['Register Number']}</div>
                <div class="subj-score">Score: {m_val} / 300</div>
                <div style="font-size: 0.75rem; color: #475569; margin-top: 6px;">
                    CIA1: {s_top[f'{sid}_CIA1']} | CIA2: {s_top[f'{sid}_CIA2']} | Model: {s_top[f'{sid}_Model']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Overall Exam Toppers across all 5 subjects
    st.markdown("### 🎯 Exam-wise Overall Toppers (Sum of all 5 Subjects)")
    ex_c1, ex_c2, ex_c3 = st.columns(3)

    with ex_c1:
        top_cia1_val = df["Total_CIA1"].max()
        top_cia1_stu = df[df["Total_CIA1"] == top_cia1_val].iloc[0]
        st.markdown(f"""
        <div class="subj-topper-card">
            <span class="subj-badge" style="background: #dbeafe; color: #1e40af;">EXAM 1</span>
            <div class="subj-name">Overall CIA 1 Topper</div>
            <div class="subj-student" style="margin-top: 8px;">{top_cia1_stu['Student Name']}</div>
            <div style="font-size: 0.85rem; color: #64748b;">{top_cia1_stu['Register Number']}</div>
            <div class="subj-score" style="background: #eff6ff; color: #1d4ed8;">Score: {top_cia1_val} / 500 Marks</div>
        </div>
        """, unsafe_allow_html=True)

    with ex_c2:
        top_cia2_val = df["Total_CIA2"].max()
        top_cia2_stu = df[df["Total_CIA2"] == top_cia2_val].iloc[0]
        st.markdown(f"""
        <div class="subj-topper-card">
            <span class="subj-badge" style="background: #f3e8ff; color: #7e22ce;">EXAM 2</span>
            <div class="subj-name">Overall CIA 2 Topper</div>
            <div class="subj-student" style="margin-top: 8px;">{top_cia2_stu['Student Name']}</div>
            <div style="font-size: 0.85rem; color: #64748b;">{top_cia2_stu['Register Number']}</div>
            <div class="subj-score" style="background: #faf5ff; color: #7e22ce;">Score: {top_cia2_val} / 500 Marks</div>
        </div>
        """, unsafe_allow_html=True)

    with ex_c3:
        top_mod_val = df["Total_Model"].max()
        top_mod_stu = df[df["Total_Model"] == top_mod_val].iloc[0]
        st.markdown(f"""
        <div class="subj-topper-card">
            <span class="subj-badge" style="background: #dcfce7; color: #15803d;">EXAM 3</span>
            <div class="subj-name">Overall Model Exam Topper</div>
            <div class="subj-student" style="margin-top: 8px;">{top_mod_stu['Student Name']}</div>
            <div style="font-size: 0.85rem; color: #64748b;">{top_mod_stu['Register Number']}</div>
            <div class="subj-score" style="background: #f0fdf4; color: #15803d;">Score: {top_mod_val} / 500 Marks</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. Top 10 Merit Leaderboard
    st.markdown("### 🏅 BCA Class Merit Leaderboard (Top 10)")
    top_n = st.slider("Select number of rankers to display:", min_value=5, max_value=25, value=10)
    top_df = df.sort_values(by="Overall_Total", ascending=False).head(top_n).copy()

    def get_medal(rank):
        if rank == 1: return "🥇 1st"
        elif rank == 2: return "🥈 2nd"
        elif rank == 3: return "🥉 3rd"
        else: return f"#{rank}"

    top_df["Position"] = [get_medal(i+1) for i in range(len(top_df))]
    top_df["Percentage (%)"] = top_df["Overall_Percentage"].round(2)

    disp_cols = [
    "Register Number", 
    "Student Name", 
    "email", 
    "whatsapp_no", 
    "Mobile Number", 
    # CIA 1 Section
    "FOA_CIA1", "MAD_CIA1", "CN_CIA1", "WT_CIA1", "DMW_CIA1", "Total_CIA1",
    # CIA 2 Section
    "FOA_CIA2", "MAD_CIA2", "CN_CIA2", "WT_CIA2", "DMW_CIA2", "Total_CIA2",
    # Model Exam Section
    "FOA_Model", "MAD_Model", "CN_Model", "WT_Model", "DMW_Model", "Total_Model",
    "Overall_Total", "Overall_Percentage", "Rank"
]
    st.dataframe(top_df[disp_cols], use_container_width=True, hide_index=True)

    # Download Merit List
    csv_toppers = top_df[disp_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Merit List (CSV)",
        data=csv_toppers,
        file_name="bca_top_rankers.csv",
        mime="text/csv"
    )


# ===========================================================================
# SECTION 3: 📋 STUDENT DIRECTORY & SEARCH
# ===========================================================================
elif app_section == "📋 Student Directory":
    st.markdown(f"## 📋 BCA Student Directory (All {len(df)} Students)")
    st.write(f"Search, filter, view and manage all {len(df)} student records across the 5 subjects.")

    c_s1, c_s2, c_s3 = st.columns([2, 1, 1])
    with c_s1:
        search_query = st.text_input("🔍 Search by Student Name or Register Number:", placeholder="e.g. Divya, 24BCA017")
    with c_s2:
        fee_filter = st.selectbox("💳 Filter by Fee Status:", ["All", "Paid", "Pending"])
    with c_s3:
        perf_filter = st.selectbox("📊 Academic Standing:", ["All", "Distinction (≥75%)", "Pass (40-74%)", "Needs Attention (<40%)"])

    filtered_df = df.copy()

    if search_query:
        sq = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df["Student Name"].str.lower().str.contains(sq) |
            filtered_df["Register Number"].str.lower().str.contains(sq)
        ]

    if fee_filter != "All":
        filtered_df = filtered_df[filtered_df["Fee Status"] == fee_filter]

    if perf_filter == "Distinction (≥75%)":
        filtered_df = filtered_df[filtered_df["Overall_Percentage"] >= 75]
    elif perf_filter == "Pass (40-74%)":
        filtered_df = filtered_df[(filtered_df["Overall_Percentage"] >= 40) & (filtered_df["Overall_Percentage"] < 75)]
    elif perf_filter == "Needs Attention (<40%)":
        filtered_df = filtered_df[(filtered_df[all_exam_cols] < 40).any(axis=1)]

    st.caption(f"Showing **{len(filtered_df)}** of **{len(df)}** student records")

    # Table View Options (Summary vs Detailed 15 exams)
    view_mode = st.radio("View Columns:", ["Subject Totals Summary", "Detailed 15 Exam Marks"], horizontal=True)

    if view_mode == "Subject Totals Summary":
        show_cols = [
        "Rank", "Register Number", "Student Name", "Mobile Number",
        
        # CIA 1 Section
        "FOA_CIA1", "MAD_CIA1", "CN_CIA1", "WT_CIA1", "DMW_CIA1", "Total_CIA1",
        
        # CIA 2 Section
        "FOA_CIA2", "MAD_CIA2", "CN_CIA2", "WT_CIA2", "DMW_CIA2", "Total_CIA2",
        
        # Model Exam Section
        "FOA_Model", "MAD_Model", "CN_Model", "WT_Model", "DMW_Model", "Total_Model",
        
        "Overall_Total", "Overall_Percentage", "Fee Status"
    ]
        display_tbl = filtered_df[show_cols].copy()
        display_tbl["Overall_Percentage"] = display_tbl["Overall_Percentage"].round(2)
        st.dataframe(display_tbl, use_container_width=True, hide_index=True)
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Student Detail Report Card Inspector
    st.markdown("### 🔍 Individual Student Academic Scorecard")
    student_options = [f"{s['Register Number']} - {s['Student Name']}" for _, s in df.iterrows()]
    selected_option = st.selectbox("Select student to view 5-subject marksheet:", student_options)

    if selected_option:
        sel_reg = selected_option.split(" - ")[0]
        s_data = df[df["Register Number"] == sel_reg].iloc[0]

        sc_col1, sc_col2 = st.columns([1, 1.1])

        with sc_col1:
            fee_color = "#15803d" if s_data['Fee Status'] == 'Paid' else "#b91c1c"
            st.markdown(f"""
            <div style="background: #ffffff; padding: 22px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between;">
                    <h3 style="margin: 0; color: #1e293b;">{s_data['Student Name']}</h3>
                    <span style="font-size: 0.95rem; font-weight: 700; color: #3b82f6;">Rank #{s_data['Rank']}</span>
                </div>
                <div style="color: #64748b; margin-top: 4px;">Register Number: <strong>{s_data['Register Number']}</strong></div>
                <div style="color: #64748b;">Mobile: <strong>{s_data['Mobile Number']}</strong></div>
                <div style="margin-top: 6px;">Fee Status: <strong style="color: {fee_color};">{s_data['Fee Status']}</strong></div>
                <hr style="margin: 12px 0;">
                <div style="font-size: 0.88rem; line-height: 1.8;">
                    • <strong>Fundamentals of Algorithm:</strong> {s_data['FOA_Total']}/300 (CIA1: {s_data['FOA_CIA1']}, CIA2: {s_data['FOA_CIA2']}, Model: {s_data['FOA_Model']})<br>
                    • <strong>Mobile App Dev (MAD):</strong> {s_data['MAD_Total']}/300 (CIA1: {s_data['MAD_CIA1']}, CIA2: {s_data['MAD_CIA2']}, Model: {s_data['MAD_Model']})<br>
                    • <strong>Computer Networks:</strong> {s_data['CN_Total']}/300 (CIA1: {s_data['CN_CIA1']}, CIA2: {s_data['CN_CIA2']}, Model: {s_data['CN_Model']})<br>
                    • <strong>Web Technology:</strong> {s_data['WT_Total']}/300 (CIA1: {s_data['WT_CIA1']}, CIA2: {s_data['WT_CIA2']}, Model: {s_data['WT_Model']})<br>
                    • <strong>Data Mining & Warehouse:</strong> {s_data['DMW_Total']}/300 (CIA1: {s_data['DMW_CIA1']}, CIA2: {s_data['DMW_CIA2']}, Model: {s_data['DMW_Model']})
                </div>
                <div style="margin-top: 14px; background: #f8fafc; padding: 10px; border-radius: 8px; text-align: center;">
                    <strong>Grand Total: {s_data['Overall_Total']} / 1500</strong> ({s_data['Overall_Percentage']:.2f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)

        with sc_col2:
            # Bar chart of 5 subjects
            fig_subj_bar = go.Figure(data=[
                go.Bar(
                    name="Subject Total (/300)",
                    x=["Algorithm", "MAD", "Networks", "Web Tech", "Data Mining"],
                    y=[s_data['FOA_Total'], s_data['MAD_Total'], s_data['CN_Total'], s_data['WT_Total'], s_data['DMW_Total']],
                    marker_color=['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'],
                    text=[f"{m}/300" for m in [s_data['FOA_Total'], s_data['MAD_Total'], s_data['CN_Total'], s_data['WT_Total'], s_data['DMW_Total']]],
                    textposition="auto"
                )
            ])
            fig_subj_bar.update_layout(
                title=f"5-Subject Scores: {s_data['Student Name']}",
                yaxis=dict(range=[0, 315], title="Subject Total"),
                height=280,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_subj_bar, use_container_width=True)

    # Download CSV
    st.markdown("---")
    csv_all = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Student Dataset (CSV)",
        data=csv_all,
        file_name="bca_class_5_subjects.csv",
        mime="text/csv",
    )


# ===========================================================================
# SECTION 4: ⚠️ FEE & LOW MARK ALERT SYSTEM
# ===========================================================================
elif app_section == "⚠️ Fee & Low Mark Alerts":
    st.markdown("## ⚠️ Fee & Low Mark Alert System")
    st.write("Filter students requiring academic intervention or fee clearance across the 5 subjects, with simulated SMS/WhatsApp dispatch.")

    alert_type = st.radio(
        "🚨 Select Alert Criteria:",
        [
            "All Attention Required (Pending Fees OR Low Marks)",
            "Fee Pending Only",
            "Low Marks Only (< Threshold in any exam)",
            "Critical: Both Fee Pending AND Low Marks"
        ],
        horizontal=True
    )

    pass_threshold = st.slider("Low Mark Threshold (Marks < Threshold in any exam):", min_value=30, max_value=50, value=40)

    # Identify low mark candidates
    low_mask = (df[all_exam_cols] < pass_threshold).any(axis=1)

    if alert_type == "Fee Pending Only":
        alert_df = df[df["Fee Status"] == "Pending"].copy()
    elif alert_type == "Low Marks Only (< Threshold in any exam)":
        alert_df = df[low_mask].copy()
    elif alert_type == "Critical: Both Fee Pending AND Low Marks":
        alert_df = df[(df["Fee Status"] == "Pending") & low_mask].copy()
    else:
        alert_df = df[(df["Fee Status"] == "Pending") | low_mask].copy()

    st.warning(f"🚨 **{len(alert_df)} students** match the selected alert criteria.")

    # Function to build alert reason
    def get_alert_reasons(row):
        reasons = []
        if row["Fee Status"] == "Pending":
            reasons.append("💳 Fee Due")
        # Check 5 subjects
        for sid, sname in [("FOA", "Algorithm"), ("MAD", "MAD"), ("CN", "Networks"), ("WT", "Web Tech"), ("DMW", "Data Mining")]:
            failed_exams = []
            for ex in ["CIA1", "CIA2", "Model"]:
                col = f"{sid}_{ex}"
                if row[col] < pass_threshold:
                    failed_exams.append(f"{ex}({row[col]})")
            if failed_exams:
                reasons.append(f"{sname}: {', '.join(failed_exams)}")
        return " | ".join(reasons)

    if not alert_df.empty:
        alert_df["Alert Reason"] = alert_df.apply(get_alert_reasons, axis=1)
        st.dataframe(
            alert_df[[
                "Register Number", "Student Name", "Mobile Number",
                "FOA_Total", "MAD_Total", "CN_Total", "WT_Total", "DMW_Total",
                "Fee Status", "Alert Reason"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("🎉 No students match the alert criteria!")

    st.markdown("---")

    # SMS Dispatch Simulator
    st.markdown("### 📱 Simulated SMS / WhatsApp Notification Dispatcher")
    col_sms_form, col_sms_preview = st.columns([1.1, 0.9])

    with col_sms_form:
        st.markdown("#### 1. Compose Notification")
        sms_recipient_mode = st.radio("Dispatch Mode:", ["Individual Student", "📢 Bulk Dispatch to ALL Filtered Students"])

        if sms_recipient_mode == "Individual Student":
            if not alert_df.empty:
                recipient_opts = [f"{r['Register Number']} - {r['Student Name']} ({r['Mobile Number']})" for _, r in alert_df.iterrows()]
            else:
                recipient_opts = [f"{r['Register Number']} - {r['Student Name']} ({r['Mobile Number']})" for _, r in df.iterrows()]
            selected_student_opt = st.selectbox("Select Student:", recipient_opts)
            target_reg = selected_student_opt.split(" - ")[0]
            target_student = df[df["Register Number"] == target_reg].iloc[0]
        else:
            target_student = alert_df.iloc[0] if not alert_df.empty else df.iloc[0]

        msg_template = st.selectbox(
            "Select Message Template:",
            [
                "Academic Performance Warning (Low Marks in Core Subjects)",
                "Fee Payment Due Reminder",
                "Combined Academic & Fee Due Alert"
            ]
        )

        # Build dynamic message
        if msg_template == "Fee Payment Due Reminder":
            msg_text = (
                f"Dear Parent/Student ({target_student['Student Name']}, Reg No: {target_student['Register Number']}), "
                f"This is an official intimation from the BCA Department. Tuition fee payment is PENDING. "
                f"Kindly clear dues at the college finance counter before the due date. - HOD, BCA Dept."
            )
        elif msg_template == "Academic Performance Warning (Low Marks in Core Subjects)":
            reasons = get_alert_reasons(target_student)
            msg_text = (
                f"Dear Parent of {target_student['Student Name']} ({target_student['Register Number']}), "
                f"Your ward scored below minimum passing mark in internal examinations: {reasons}. "
                f"Mandatory remedial classes start Monday. Contact faculty coordinator. - BCA Academic Committee."
            )
        else:
            msg_text = (
                f"URGENT NOTICE - BCA Dept: Student {target_student['Student Name']} ({target_student['Register Number']}) "
                f"has pending fee dues and low exam performance (Total: {target_student['Overall_Total']}/1500). "
                f"Please meet the Faculty Advisor on Wednesday between 2-4 PM. Contact: +91 98412 11001."
            )

        customized_msg = st.text_area("Message Content (Editable):", value=msg_text, height=130)

        # Action buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📲 Simulate Send SMS", type="primary", use_container_width=True):
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if sms_recipient_mode == "Individual Student":
                    st.session_state.sms_log.append({
                        "Timestamp": now_str,
                        "Recipient": target_student["Student Name"],
                        "Register Number": target_student["Register Number"],
                        "Mobile": target_student["Mobile Number"],
                        "Type": msg_template,
                        "Status": "✅ Delivered (Simulated)"
                    })
                    st.toast(f"✅ SMS sent to {target_student['Student Name']} ({target_student['Mobile Number']})!", icon="📲")
                    st.success(f"SMS dispatched to **{target_student['Mobile Number']}** successfully!")
                else:
                    for _, s in alert_df.iterrows():
                        st.session_state.sms_log.append({
                            "Timestamp": now_str,
                            "Recipient": s["Student Name"],
                            "Register Number": s["Register Number"],
                            "Mobile": s["Mobile Number"],
                            "Type": msg_template,
                            "Status": "✅ Delivered (Simulated)"
                        })
                    st.toast(f"🚀 Bulk SMS sent to all {len(alert_df)} students!", icon="📢")
                    st.success(f"Bulk SMS dispatched to all **{len(alert_df)} students** successfully!")

        with btn_col2:
            encoded_text = urllib.parse.quote(customized_msg)
            wa_link = f"https://wa.me/91{target_student['Mobile Number']}?text={encoded_text}"
            st.markdown(
                f"""
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <div style="background: #25d366; color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: 700;">
                        💬 Open WhatsApp Web
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    with col_sms_preview:
        st.markdown("#### 2. Live SMS Smartphone Preview")
        st.markdown(f"""
        <div class="phone-mockup">
            <div class="phone-screen">
                <div class="sms-sender">
                    COLLEGE-BCA-DEPT<br>
                    <span style="font-size: 0.7rem; color: #64748b;">To: +91 {target_student['Mobile Number']}</span>
                </div>
                <div class="sms-bubble">
                    {customized_msg}
                </div>
                <div style="text-align: right; font-size: 0.65rem; color: #94a3b8; margin-top: 4px;">
                    Just now • SMS via Gateway
                </div>
            </div>
            <div style="text-align: center; margin-top: 10px; font-size: 0.75rem; color: #94a3b8;">
                Characters: {len(customized_msg)} | 1 Message Unit
            </div>
        </div>
        """, unsafe_allow_html=True)

    # SMS Log Table
    st.markdown("---")
    st.markdown("### 📜 Simulated SMS Dispatch History")
    if st.session_state.sms_log:
        st.dataframe(pd.DataFrame(st.session_state.sms_log), use_container_width=True)
        if st.button("🗑️ Clear SMS Dispatch Log"):
            st.session_state.sms_log = []
            st.rerun()
    else:
        st.info("No SMS sent yet during this session.")


# ===========================================================================
# SECTION 5: 👨‍🏫 FACULTY & SUBJECT DIRECTORY
# ===========================================================================
elif app_section == "👨‍🏫 Faculty & Subjects":
    st.markdown("## 👨‍🏫 BCA Faculty & Subject Directory")
    st.write("Official subject allocation for the 5 core BCA subjects.")

    t_search = st.text_input("🔍 Search by Teacher Name, Subject, or Subject Code:", placeholder="e.g. Algorithm, Narayanan, Prakash")

    filtered_teachers = TEACHERS
    if t_search:
        ts = t_search.lower().strip()
        filtered_teachers = [
            t for t in TEACHERS
            if ts in t["teacher_name"].lower() or
               ts in t["subject_name"].lower() or
               ts in t["subject_code"].lower()
        ]

    st.markdown(f"**Showing {len(filtered_teachers)} faculty members**")

    # Render Faculty Cards in 2 columns
    t_col1, t_col2 = st.columns(2)

    for idx, t in enumerate(filtered_teachers):
        target_col = t_col1 if idx % 2 == 0 else t_col2
        with target_col:
            st.markdown(f"""
            <div class="faculty-card">
                <span class="faculty-pill">{t['subject_code']} • {t['credits']} Credits</span>
                <div class="faculty-name">{t['teacher_name']}</div>
                <div class="faculty-desig">{t['designation']} • {t['qualification']}</div>
                <div style="font-weight: 700; color: #1e3a8a; margin-bottom: 8px;">
                    📖 Subject: {t['subject_name']}
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.6;">
                    📍 <strong>Cabin:</strong> {t['cabin']}<br>
                    ⏰ <strong>Office Hours:</strong> {t['office_hours']}<br>
                    ⏳ <strong>Workload:</strong> {t['hours_per_week']} hours per week<br>
                    📧 <strong>Email:</strong> <a href="mailto:{t['email']}">{t['email']}</a><br>
                    📱 <strong>Mobile:</strong> <code>{t['mobile']}</code>
                </div>
                <div style="margin-top: 10px; background: #f1f5f9; padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; color: #334155;">
                    💡 <strong>Syllabus Highlights:</strong> {t['syllabus_highlight']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quick Table Reference
    st.markdown("### 📋 Faculty Allocation Summary Table")
    fac_df = pd.DataFrame(TEACHERS)[[
        "subject_code", "subject_name", "teacher_name",
        "designation", "cabin", "email", "mobile"
    ]].rename(columns={
        "subject_code": "Code",
        "subject_name": "Subject Handled",
        "teacher_name": "Faculty In-Charge",
        "designation": "Designation",
        "cabin": "Cabin",
        "email": "Email",
        "mobile": "Contact"
    })
    st.dataframe(fac_df, use_container_width=True, hide_index=True)


# ===========================================================================
# SECTION 6: 📊 ANALYTICS & CHARTS
# ===========================================================================
elif app_section == "📊 Analytics & Charts":
    st.markdown("## 📊 BCA Academic Performance Analytics")
    st.write("Visual statistical breakdowns across the 5 core subjects and examinations.")

    c_g1, c_g2 = st.columns(2)

    with c_g1:
        # 1. Total Marks Distribution
        fig_hist = px.histogram(
            df,
            x="Overall_Total",
            nbins=15,
            title="Overall Score Distribution (Grand Total out of 1500)",
            color_discrete_sequence=["#3b82f6"],
            marginal="box"
        )
        fig_hist.add_vline(x=df["Overall_Total"].mean(), line_dash="dash", line_color="red", annotation_text=f"Mean: {df['Overall_Total'].mean():.1f}")
        fig_hist.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)

    with c_g2:
        # 2. Fee Clearance Doughnut
        fee_counts = df["Fee Status"].value_counts().reset_index()
        fee_counts.columns = ["Status", "Count"]
        fig_fee = px.pie(
            fee_counts,
            names="Status",
            values="Count",
            title="Fee Clearance Distribution",
            color="Status",
            color_discrete_map={"Paid": "#10b981", "Pending": "#ef4444"},
            hole=0.45
        )
        fig_fee.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_fee, use_container_width=True)

    c_g3, c_g4 = st.columns(2)

    with c_g3:
        # 3. Subject-wise Average Marks Comparison
        subj_means = pd.DataFrame({
            "Subject": ["Algorithm", "MAD", "Networks", "Web Tech", "Data Mining"],
            "Average Marks": [
                df["FOA_Total"].mean(),
                df["MAD_Total"].mean(),
                df["CN_Total"].mean(),
                df["WT_Total"].mean(),
                df["DMW_Total"].mean()
            ]
        })
        fig_subj = px.bar(
            subj_means,
            x="Subject",
            y="Average Marks",
            color="Subject",
            title="Class Average Marks by Subject (out of 300)",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_subj.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
        st.plotly_chart(fig_subj, use_container_width=True)

    with c_g4:
        # 4. Exam Comparison Boxplot (Total CIA 1 vs CIA 2 vs Model)
        melted_exams = pd.melt(
            df,
            id_vars=["Student Name", "Register Number"],
            value_vars=["Total_CIA1", "Total_CIA2", "Total_Model"],
            var_name="Exam",
            value_name="Aggregate Marks"
        )
        fig_ex_box = px.box(
            melted_exams,
            x="Exam",
            y="Aggregate Marks",
            color="Exam",
            title="Aggregate Exam Performance Comparison (out of 500)",
            color_discrete_map={
                "Total_CIA1": "#3b82f6",
                "Total_CIA2": "#8b5cf6",
                "Total_Model": "#06b6d4"
            }
        )
        fig_ex_box.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_ex_box, use_container_width=True)


# ===========================================================================
# SECTION 7: 🤖 AI ASSISTANT (HUGGING FACE)
# ===========================================================================
elif app_section == "🤖 AI Assistant (Hugging Face)":
    st.markdown("## 🤖 BCA AI Assistant (Powered by Hugging Face)")
    st.write(
        "Ask queries in natural language about our BCA students across all 5 subjects, toppers, fee statuses, or faculty members. "
        "Supports both the **Hugging Face Inference API** and the **Fast Local Smart Engine**."
    )

    hf_token = st.session_state.get("hf_token", "")
    hf_model = st.session_state.get("hf_model", "Qwen/Qwen2.5-7B-Instruct")

    if hf_token:
        st.success(f"🤗 Connected to Hugging Face Model: **{hf_model}**")
    else:
        st.info("⚡ Active Engine: **Fast Local Smart Engine** (Instant response, offline ready). Add a Hugging Face token in the sidebar for cloud generative LLMs.")

    st.markdown("##### 💡 Suggested Questions (Click to ask):")
    p_cols = st.columns(4)
    quick_query = None

    if p_cols[0].button("🏆 Who is the overall topper?", use_container_width=True):
        quick_query = "Who is the overall class topper?"
    if p_cols[1].button("🥇 Who topped Web Technology?", use_container_width=True):
        quick_query = "Who topped Web Technology?"
    if p_cols[2].button("⚠️ List pending fee students", use_container_width=True):
        quick_query = "Show students with pending fees"
    if p_cols[3].button("👨‍🏫 Who teaches Algorithm?", use_container_width=True):
        quick_query = "Who teaches Fundamentals of Algorithm?"

    # Chat history
    for msg in st.session_state.chat_messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask about any student, subject topper, fee, or faculty...")
    query_to_process = user_prompt or quick_query

    if query_to_process:
        st.session_state.chat_messages.append({"role": "user", "content": query_to_process})
        with st.chat_message("user", avatar="👤"):
            st.markdown(query_to_process)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing BCA 5-subject database..."):
                response_text, provider = ask_huggingface_assistant(
                    prompt=query_to_process,
                    df=df,
                    teachers=TEACHERS,
                    hf_token=hf_token,
                    hf_model=hf_model
                )
                st.markdown(response_text)
                st.caption(f"Engine: {provider}")

        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

    if len(st.session_state.chat_messages) > 1:
        if st.button("🗑️ Reset Chat History"):
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": "Chat history cleared. How can I help you today?"
                }
            ]
            st.rerun()


# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 10px 0;">
    🎓 BCA Class Management & Topper Finder Portal • 5 Core Subjects Edition • Built with Python, Streamlit & Hugging Face<br>
    Academic Year 2024–2027 • Department of Computer Applications
</div>
""", unsafe_allow_html=True)
# --- Student Notification & Alert Agent ---
import pandas as pd
import streamlit as st

st.markdown("---")
st.subheader("🤖 AI Student Notification & Fee Alert System")

if st.button("🚀 Trigger Marks & Fee Alerts to All Students"):
    csv_file = 'bca_students_new.csv'
    df = pd.read_csv(csv_file)
    
    success_count = 0
    for index, row in df.iterrows():
        name = row.get('name', 'Student')
        marks = row.get('Overall_Total', 0)
        fees_due = row.get('Fee Status', 0)
        email = row.get('email', '')
        if email: 
            send_student_email(email, name, marks, fees_due,"Status Check Active")
        whatsapp = row.get('whatsapp_no', '')
       
        # Logic / Simulation
    print(f"Alert sent to {name} | Email: {email} | WhatsApp: {whatsapp}")
    success_count += 1
        
    st.success(f"Successfully processed and triggered alerts for all {success_count} students (Email & WhatsApp)!")
    # --- AI Student Notification & Fee Alert System (Agentic Upgrade) ---
import pandas as pd
import streamlit as st

st.markdown("---")
st.subheader("🤖 AI Agent: Smart Notification & Fee Alert System")

if st.button("🚀 Run AI Audit & Send Smart Alerts"):
    csv_file = 'bca_students_new.csv'
    df = pd.read_csv(csv_file)
    
    alerts_sent = 0
    
    for index, row in df.iterrows():
        name = row.get('Student Name', 'Student')
        fees_due = row.get('fees_due', 0)
        percentage = row.get('Overall_Percentage', 0)
        if pd.isna(percentage):
            percentage = 0
        email = row.get('email', '')
        whatsapp = row.get('whatsapp_no', '')
        alerts_sent+=1
        # Agentic Reasoning & Condition Check
        issues = []
        if percentage < 40:
            issues.append(f"Low Academic Performance ({percentage}%)")
        if fees_due > 0:
            issues.append(f"Pending Fees: Rs. {fees_due}")
            
        # Send alert only if student needs attention
        # Condition illama direct-ah mail anuppura maathri maththalam
        status = " | ".join(issues) if issues else "All Clear / Verified"
        
        # Itha loop-oda correct alignment-ku kondu vanthutom
        send_student_email(email, name, percentage, fees_due, status)
        alerts_sent += 1
    st.success(f"🤖 AI Agent successfully audited all records and triggered smart custom alerts for {alerts_sent} students!")