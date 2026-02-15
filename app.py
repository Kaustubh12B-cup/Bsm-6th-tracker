import streamlit as st
import pandas as pd
import os

# --- 1. SETUP & SYLLABUS ---
st.set_page_config(page_title="MS Bal Shikshan Mandir Tracker", layout="wide")

# This is your database file
DATA_FILE = "study_data.csv"

syllabus = {
    "Maths": ["Basic Geometry", "Angles", "Integers", "Fractions", "Decimals", "Graphs", "Symmetry", "Divisibility", "HCF-LCM"],
    "Science": ["Natural Resources", "Living World", "Classification", "Disaster Mgmt", "Substances", "Nutrition", "Skeletal System", "Motion", "Force"]
}

# --- 2. DATA LOADING/SAVING ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create empty data if file doesn't exist
        rows = []
        for subj, chapters in syllabus.items():
            for ch in chapters:
                rows.append({"Subject": subj, "Chapter": ch, "Covered": False, "Revised": False, "Approved": False})
        return pd.DataFrame(rows)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Initial load into session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- 3. LOGIN SYSTEM ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login():
    st.title("🔑 School Tracker Login")
    user = st.selectbox("Who are you?", ["Select", "Student", "Mother"])
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if user == "Student" and password == "pune123":
            st.session_state.auth = "Student"
            st.rerun()
        elif user == "Mother" and password == "parent456":
            st.session_state.auth = "Mother"
            st.rerun()
        else:
            st.error("Wrong password!")

if not st.session_state.auth:
    login()
    st.stop()

# --- 4. MAIN APP INTERFACE ---
st.sidebar.title(f"Logged in: {st.session_state.auth}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

st.title("📖 MS Bal Shikshan Mandir - 6th Std")

# --- 5. REPORT CARD (DASHBOARD) ---
st.subheader("📊 Work Report")
total_chapters = len(st.session_state.df)
approved_count = st.session_state.df["Approved"].sum()
pending_count = total_chapters - approved_count

col1, col2 = st.columns(2)
col1.metric("Done (Approved)", f"{approved_count}")
col2.metric("Pending Work", f"{pending_count}")
st.progress(int((approved_count / total_chapters) * 100))

# --- 6. SUBJECT TABS ---
tab1, tab2 = st.tabs(["Maths", "Science"])

def show_subject(subj, tab_obj):
    with tab_obj:
        st.write(f"### {subj} Checklist")
        # Filter data for this subject
        subj_df = st.session_state.df[st.session_state.df["Subject"] == subj]
        
        for idx, row in subj_df.iterrows():
            c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
            c1.text(row["Chapter"])
            
            # STUDENT VIEW
            if st.session_state.auth == "Student":
                # Checkboxes for Student
                new_cov = c2.checkbox("Covered", value=row["Covered"], key=f"c_{idx}")
                new_rev = c3.checkbox("Revised", value=row["Revised"], key=f"r_{idx}")
                st.session_state.df.at[idx, "Covered"] = new_cov
                st.session_state.df.at[idx, "Revised"] = new_rev
                # Show status
                status = "✅ Approved" if row["Approved"] else "⏳ Waiting for Mom"
                c4.info(status)
            
            # MOTHER VIEW
            else:
                c2.write("✅" if row["Covered"] else "❌")
                c3.write("✅" if row["Revised"] else "❌")
                if row["Covered"]:
                    new_app = c4.checkbox("Approve Chapter", value=row["Approved"], key=f"a_{idx}")
                    st.session_state.df.at[idx, "Approved"] = new_app
                else:
                    c4.warning("Student must finish first")

show_subject("Maths", tab1)
show_subject("Science", tab2)

# --- 7. THE SAVE BUTTON ---
st.divider()
if st.button("💾 SAVE ALL CHANGES"):
    save_data(st.session_state.df)
    st.success("Work saved successfully! Your Mom can now see your progress.")
