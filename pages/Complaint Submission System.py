import streamlit as st
from pymongo import MongoClient

# 🔹 MongoDB Connection
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["hostel_maintenance"]  # Database Name

st.title("📢 Student Grievance Express")

# 🔹 Form Fields
name = st.text_input("Name")
reg_no = st.text_input("Registration No")
issue_type = st.selectbox("Type", ["Hostel", "Department", "General"])
general = st.selectbox("General", ["Sports Management", "Transport Management", "Canteen Management"]) if issue_type == "General" else None

hostel = st.selectbox("Hostel", ["A Block", "Narmada", "Nilgiri"]) if issue_type == "Hostel" else None
department = st.text_input("Department Name") if issue_type == "Department" else None
floor = st.radio("Floor", ["I", "II", "III", "IV"]) if issue_type == "Hostel" else None
room_no = st.text_input("Room No") if issue_type == "Hostel" else None
category = st.selectbox("Category", ["Plumbing", "Electrical", "Civil", "HR", "Food"]) if issue_type in ["Hostel"] else None
category = st.selectbox("Category", ["Curriculum", "Faculty", "Classroom Management", "Fee", "Placement"]) if issue_type in ["Department"] else None
details = st.text_area("Details")

# 🔹 Submit Button
if st.button("Submit"):
    # Check for required fields
    if name and reg_no and category != "Select" and details:
        # Create a dictionary for MongoDB
        issue_data = {
            "name": name,
            "reg_no": reg_no,
            "type": issue_type,
            "category": category,
            "details": details
        }

        # Add extra fields based on issue type
        if issue_type == "Hostel":
            issue_data["hostel"] = hostel
            issue_data["floor"] = floor
            issue_data["room_no"] = room_no
            collection_name = "hostel_issues"

        elif issue_type == "Department":
            issue_data["department"] = department
            collection_name = "dept_issues"

        else:
            issue_data["general_category"] = general
            collection_name = "general_issues"

        # Store issue in the specific collection
        db[collection_name].insert_one(issue_data)

        # Also store the issue in the admin collection
        db["admin_issues"].insert_one(issue_data)
        
        st.success(f"✅ Issue successfully submitted to {collection_name} & Admin Database!")
    else:
        st.warning("⚠ Please fill all required fields.")