import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="MS Bal Shikshan Tracker", layout="wide")

# --- SYLLABUS DATA ---
SYLLABUS = {
    "Maths": [
        "1. Basic Concepts in Geometry", "2. Angles", "3. Integers", 
        "4. Operations on Fractions", "5. Decimal Fractions", "6. Bar Graphs", 
        "7. Symmetry", "8. Divisibility", "9. HCF - LCM", "10. Equations", 
        "11. Ratio and Proportion", "12. Percentage", "13. Profit - Loss", 
        "14. Banks and Simple Interest", "15. Triangles", "16. Quadrilaterals", 
        "17. Geometrical Constructions", "18. 3D Shapes"
    ],
    "Science": [
        "1. Natural Resources", "2. The Living World", "3. Diversity in Living Things",
        "4. Disaster Management", "5. Substances in Surroundings", "6. Substances in Daily Use",
        "7. Nutrition and Diet", "8. Skeletal System & Skin", "9. Motion & Types of Motion",
        "10. Force & Types of Force", "11. Work & Energy", "12. Simple Machines", 
        "13. Sound", "14. Light & Shadows", "15. Fun with Magnets", "16. The Universe"
    ]
}

# --- DATA STORAGE ENGINE ---
DB_FILE = "school_progress.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        # Create fresh data structure
        data = []
        for subj, chapters in SYLLABUS.items():
            for ch in chapters:
                data.append({"Subject": subj, "Chapter": ch, "Covered": False, "Revised": False, "Approved": False})
        return pd.DataFrame(data)

# Initialize Session State
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- LOGIN SYSTEM ---
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def login():
    st.title("🔑 MS Bal Shikshan Login")
    role = st.selectbox("Who is logging in?", ["Select", "Student", "Mother"])
    pwd = st.text_input("Enter Password", type="password")
    
    if st.button("Log In"):
        if role == "Student" and pwd == "pune123":
            st.session_state.user_role = "Student"
            st.rerun()
        elif role == "Mother" and pwd == "mother456":
            st.session_state.user_role = "Mother"
            st.rerun()
        else:
            st.error("Incorrect password! Hint: pune123 or mother456")

if st.session_state.user_role is None:
    login()
    st.stop()

# --- HEADER & LOGOUT ---
st.sidebar.title(f"Hello, {st.session_state.user_role}! 👋")
if st.sidebar.button("Logout"):
    st.session_state.user_role = None
    st.rerun()

# --- SUBJECT REPORTS (THE DASHBOARD) ---
st.title("📊 Study Progress Report")
col1, col2 = st.columns(2)

def show_metric(subj, column):
    subj_data = st.session_state.df[st.session_state.df["Subject"] == subj]
    total = len(subj_data)
    # Work is considered "Done" only if Mother Approved
    done = subj_data["Approved"].sum()
    pending = total - done
    
    with column:
        st.subheader(f"{subj} Report")
        st.metric(label="Completed", value=f"{done}/{total}", delta=f"{pending} Pending", delta_color="inverse")
        progress_val = int((done / total) * 100)
        st.progress(progress_val / 100)
        st.write(f"**{progress_val}% Finish**")

show_metric("Maths", col1)
show_metric("Science", col2)

st.divider()

# --- INTERACTIVE CHECKLIST ---
tab1, tab2 = st.tabs(["🔢 Maths Syllabus", "🔬 Science Syllabus"])

def render_table(subj, tab_choice):
    with tab_choice:
        st.write(f"### {subj} Checklist")
        # Get indices for rows belonging to this subject
        indices = st.session_state.df[st.session_state.df["Subject"] == subj].index
        
        # Display Columns
        c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
        c1.write("**Chapter**")
        c2.write("**Covered**")
        c3.write("**Revised**")
        c4.write("**Mom's Approval**")
        
        for idx in indices:
            row = st.session_state.df.iloc[idx]
            col_a, col_b, col_c, col_d = st.columns([4, 2, 2, 2])
            
            col_a.write(row["Chapter"])
            
            if st.session_state.user_role == "Student":
                # Student can edit Covered and Revised
                st.session_state.df.at[idx, "Covered"] = col_b.checkbox("Yes", value=row["Covered"], key=f"cov_{idx}")
                st.session_state.df.at[idx, "Revised"] = col_c.checkbox("Yes", value=row["Revised"], key=f"rev_{idx}")
                col_d.write("✅ Approved" if row["Approved"] else "⏳ Pending")
            else:
                # Mother View
                col_b.write("✅" if row["Covered"] else "❌")
                col_c.write("✅" if row["Revised"] else "❌")
                # Mother can only approve if covered
                if row["Covered"]:
                    st.session_state.df.at[idx, "Approved"] = col_d.checkbox("Approve", value=row["Approved"], key=f"app_{idx}")
                else:
                    col_d.write("Not ready")

render_table("Maths", tab1)
render_table("Science", tab2)

# --- SAVE BUTTON ---
st.sidebar.divider()
st.sidebar.write("### Save Progress")
if st.sidebar.button("💾 SAVE CHANGES"):
    st.session_state.df.to_csv(DB_FILE, index=False)
    st.sidebar.success("Saved! Now your data won't be lost.")
