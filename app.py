import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MS Bal Shikshan Mandir - Tracker", layout="wide")
DATA_FILE = "persistent_syllabus_data.csv"

# Subject Syllabus
syllabus = {
    "Maths": [
        "Basic Geometry", "Angles", "Integers", "Operations on Fractions",
        "Decimal Fractions", "Bar Graphs", "Symmetry", "Divisibility", 
        "HCF - LCM", "Equations", "Ratio & Proportion", "Percentage", 
        "Profit - Loss", "Banks & Simple Interest", "Triangles", 
        "Quadrilaterals", "Geometrical Constructions", "3D Shapes"
    ],
    "Science": [
        "Natural Resources", "The Living World", "Diversity in Living Things", 
        "Disaster Management", "Substances in Surroundings", "Substances in Daily Use",
        "Nutrition and Diet", "Skeletal System & Skin", "Motion & Types of Motion",
        "Force & Types of Force", "Work and Energy", "Simple Machines", "Sound",
        "Light & Shadows", "Fun with Magnets", "The Universe"
    ]
}

# --- 2. DATA ENGINE ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        rows = []
        for subj, chapters in syllabus.items():
            for ch in chapters:
                rows.append({"Subject": subj, "Chapter": ch, "Covered": False, "Revised": False, "Approved": False})
        return pd.DataFrame(rows)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- 3. LOGIN GATE ---
if 'auth' not in st.session_state:
    st.session_state.auth = None

def login_screen():
    st.title("🛡️ Secure School Portal")
    col1, col2 = st.columns(2)
    with col1:
        user = st.selectbox("Select User", ["Student", "Mother"])
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            if user == "Student" and password == "student123":
                st.session_state.auth = "Student"
                st.rerun()
            elif user == "Mother" and password == "pune2026":
                st.session_state.auth = "Mother"
                st.rerun()
            else:
                st.error("Incorrect Password!")

if not st.session_state.auth:
    login_screen()
    st.stop()

# --- 4. NAVIGATION & LOGOUT ---
st.sidebar.title(f"Logged in: {st.session_state.auth}")
if st.sidebar.button("Log Out"):
    st.session_state.auth = None
    st.rerun()

# --- 5. SEPARATE SUBJECT REPORTS ---
st.title("📊 MS Bal Shikshan Mandir - 6th Std")

# Metrics Header
m_col1, m_col2 = st.columns(2)

def draw_report(subject, col):
    subj_df = st.session_state.df[st.session_state.df["Subject"] == subject]
    total = len(subj_df)
    done = subj_df["Approved"].sum()
    percent = int((done/total)*100) if total > 0 else 0
    col.metric(f"{subject} Progress", f"{done}/{total} Chapters", f"{percent}% Done")
    col.progress(percent / 100)

draw_report("Maths", m_col1)
draw_report("Science", m_col2)

st.divider()

# --- 6. CHAPTER MANAGEMENT ---
tab1, tab2 = st.tabs(["🔢 Maths Syllabus", "🔬 Science Syllabus"])

def render_subject_ui(subject, tab):
    with tab:
        st.subheader(f"Manage {subject}")
        # Get indices for this subject
        indices = st.session_state.df[st.session_state.df["Subject"] == subject].index
        
        # Table Header
        h1, h2, h3, h4 = st.columns([3, 1, 1, 2])
        h1.write("**Chapter**")
        h2.write("**Covered**")
        h3.write("**Revised**")
        h4.write("**Status/Approval**")

        for i in indices:
            row = st.session_state.df.iloc[i]
            c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
            c1.write(row["Chapter"])
            
            if st.session_state.auth == "Student":
                # Student marks progress
                st.session_state.df.at[i, "Covered"] = c2.checkbox("Done", value=row["Covered"], key=f"c_{i}")
                st.session_state.df.at[i, "Revised"] = c3.checkbox("Done", value=row["Revised"], key=f"r_{i}")
                status = "✅ Approved" if row["Approved"] else "⏳ Pending Mom"
                c4.info(status)
            else:
                # Mother approves progress
                c2.write("✅" if row["Covered"] else "❌")
                c3.write("✅" if row["Revised"] else "❌")
                if row["Covered"]:
                    st.session_state.df.at[i, "Approved"] = c4.checkbox("Approve", value=row["Approved"], key=f"a_{i}")
                else:
                    c4.warning("Not finished yet")

render_subject_ui("Maths", tab1)
render_subject_ui("Science", tab2)

# --- 7. SAVE ACTION ---
st.sidebar.divider()
if st.sidebar.button("💾 SAVE PROGRESS"):
    save_data(st.session_state.df)
    st.sidebar.success("All data saved to Cloud!")
