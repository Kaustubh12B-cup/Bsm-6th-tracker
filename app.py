import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(page_title="MS Bal Shikshan Mandir Tracker", layout="wide")

# --- SYLLABUS DATA ---
syllabus_data = {
    "Maths": [
        "Basic Concepts in Geometry", "Angles", "Integers", "Operations on Fractions",
        "Decimal Fractions", "Bar Graphs", "Symmetry", "Divisibility", "HCF - LCM",
        "Equations", "Ratio and Proportion", "Percentage", "Profit - Loss",
        "Banks and Simple Interest", "Triangles", "Quadrilaterals", "Geometrical Constructions", "3D Shapes"
    ],
    "Science": [
        "Natural Resources", "The Living World", "Diversity in Living Things", 
        "Disaster Management", "Substances in Surroundings", "Substances in Daily Use",
        "Nutrition and Diet", "Skeletal System & Skin", "Motion & Types of Motion",
        "Force & Types of Force", "Work and Energy", "Simple Machines", "Sound",
        "Light & Shadows", "Fun with Magnets", "The Universe"
    ]
}

# --- SESSION STATE INITIALIZATION ---
# This mimics a database to store progress during the session
if 'progress' not in st.session_state:
    st.session_state.progress = {
        subj: {ch: {"Covered": False, "Revised": False, "Approved": False} for ch in chapters}
        for subj, chapters in syllabus_data.items()
    }

# --- SIDEBAR: USER SELECTION ---
st.sidebar.title("👤 User Login")
user_role = st.sidebar.radio("Who is using the app?", ["Student", "Mother"])

st.title("📚 6th Std Syllabus Tracker")
st.subheader("MS Bal Shikshan Mandir English Medium School")

# --- MAIN APP LOGIC ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Science", "🔢 Maths"])

with tab1:
    st.header("Work Report")
    for subj in ["Maths", "Science"]:
        total = len(syllabus_data[subj])
        done = sum(1 for ch in st.session_state.progress[subj].values() if ch["Approved"])
        pending = total - done
        
        col1, col2, col3 = st.columns(3)
        col1.metric(f"{subj} Completed", f"{done}/{total}")
        col2.metric(f"{subj} Pending", pending)
        col3.progress(done / total if total > 0 else 0)
    
    st.divider()
    st.info("Note: Work is only counted as 'Completed' once the Mother approves it.")

# Function to render subject tables
def render_subject(subject):
    st.header(f"{subject} Syllabus")
    
    # Create a table-like structure
    cols = st.columns([4, 2, 2, 2])
    cols[0].write("**Chapter Name**")
    cols[1].write("**Covered**")
    cols[2].write("**Revised**")
    cols[3].write("**Mother's Approval**")

    for chapter in syllabus_data[subject]:
        c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
        
        c1.write(chapter)
        
        # Student Controls
        if user_role == "Student":
            st.session_state.progress[subject][chapter]["Covered"] = c2.checkbox("Done", value=st.session_state.progress[subject][chapter]["Covered"], key=f"cov_{subject}_{chapter}")
            st.session_state.progress[subject][chapter]["Revised"] = c3.checkbox("Done", value=st.session_state.progress[subject][chapter]["Revised"], key=f"rev_{subject}_{chapter}")
            # Show approval status but disable editing for student
            c4.write("✅ Approved" if st.session_state.progress[subject][chapter]["Approved"] else "⏳ Pending")
        
        # Mother Controls
        else:
            c2.write("✅" if st.session_state.progress[subject][chapter]["Covered"] else "❌")
            c3.write("✅" if st.session_state.progress[subject][chapter]["Revised"] else "❌")
            # Only allow approval if student marked it covered
            if st.session_state.progress[subject][chapter]["Covered"]:
                st.session_state.progress[subject][chapter]["Approved"] = c4.checkbox("Approve", value=st.session_state.progress[subject][chapter]["Approved"], key=f"app_{subject}_{chapter}")
            else:
                c4.write("Not ready")

with tab2:
    render_subject("Science")

with tab3:
    render_subject("Maths")
