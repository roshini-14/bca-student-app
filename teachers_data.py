"""
teachers_data.py
BCA Department Faculty and Subject Allocation Details
Explicitly defines and exports both TEACHERS and SUBJECT_MAP.
"""

from typing import List, Dict, Any

# List of all 5 BCA Core Faculty and Subjects
TEACHERS: List[Dict[str, Any]] = [
    {
        "subject_id": "FOA",
        "subject_code": "BCA401",
        "subject_name": "Fundamentals of Algorithm",
        "short_name": "Algorithm",
        "teacher_name": "T. Nagarathinam",
        "designation": "Associate Professor & HOD i/c",
        "qualification": "M.C.A., M.Phil., Ph.D.",
        "email": "t.nagarathinam@college.edu",
        "mobile": "+91 98412 11001",
        "cabin": "CS Block - Room 201 (Cabin 1)",
        "office_hours": "Mon, Wed: 10:00 AM - 12:00 PM",
        "credits": 4,
        "hours_per_week": 5,
        "syllabus_highlight": "Asymptotic Notations, Divide & Conquer, Greedy Method, Dynamic Programming, Backtracking, Branch & Bound"
    },
    {
        "subject_id": "MAD",
        "subject_code": "BCA402",
        "subject_name": "Mobile Application Development",
        "short_name": "MAD",
        "teacher_name": "A. Narayanan",
        "designation": "Assistant Professor",
        "qualification": "M.E. (CSE), Ph.D.",
        "email": "a.narayanan@college.edu",
        "mobile": "+91 98412 11002",
        "cabin": "CS Block - Room 203",
        "office_hours": "Tue, Thu: 2:00 PM - 4:00 PM",
        "credits": 4,
        "hours_per_week": 4,
        "syllabus_highlight": "Android Architecture, Activities, Intents, UI Layouts, SQLite Database, Flutter/React Native Overview, API Integration"
    },
    {
        "subject_id": "CN",
        "subject_code": "BCA403",
        "subject_name": "Computer Networks",
        "short_name": "Networks",
        "teacher_name": "K. Prakash",
        "designation": "Associate Professor",
        "qualification": "M.Tech., Ph.D.",
        "email": "k.prakash@college.edu",
        "mobile": "+91 98412 11003",
        "cabin": "CS Block - Room 205",
        "office_hours": "Mon, Thu: 11:00 AM - 1:00 PM",
        "credits": 4,
        "hours_per_week": 4,
        "syllabus_highlight": "OSI & TCP/IP Reference Models, Data Link Layer, IP Addressing (IPv4/IPv6), Routing Protocols, TCP/UDP, Network Security"
    },
    {
        "subject_id": "WT",
        "subject_code": "BCA404",
        "subject_name": "Web Technology",
        "short_name": "Web Tech",
        "teacher_name": "V. Bhuvaneshwari",
        "designation": "Assistant Professor",
        "qualification": "M.Sc. (CS), M.Phil., NET",
        "email": "v.bhuvaneshwari@college.edu",
        "mobile": "+91 98412 11004",
        "cabin": "CS Block - Room 208",
        "office_hours": "Wed, Fri: 3:00 PM - 5:00 PM",
        "credits": 3,
        "hours_per_week": 4,
        "syllabus_highlight": "HTML5, CSS3, JavaScript ES6+, DOM Manipulation, JSON, RESTful Web Services, Bootstrap & Streamlit UI"
    },
    {
        "subject_id": "DMW",
        "subject_code": "BCA405",
        "subject_name": "Data Mining and Warehouse",
        "short_name": "Data Mining",
        "teacher_name": "S. Srinath",
        "designation": "Assistant Professor",
        "qualification": "M.Tech. (IT), Ph.D.",
        "email": "s.srinath@college.edu",
        "mobile": "+91 98412 11005",
        "cabin": "CS Block - Room 210",
        "office_hours": "Tue, Fri: 10:30 AM - 12:30 PM",
        "credits": 3,
        "hours_per_week": 3,
        "syllabus_highlight": "Data Warehouse Schemas, OLAP, Data Preprocessing, Apriori Association Rule Mining, Classification (Decision Trees, Naive Bayes), Clustering (K-Means)"
    }
]

# Robust dictionary mapping supporting lookup by:
# 1. Subject ID (e.g., 'FOA', 'MAD', 'CN', 'WT', 'DMW')
# 2. Lowercase Subject ID (e.g., 'foa', 'mad', 'cn', 'wt', 'dmw')
# 3. Subject Code (e.g., 'BCA401', 'BCA402', ...)
# 4. Full Subject Name (e.g., 'Fundamentals of Algorithm', ...)
# 5. Short Name (e.g., 'Algorithm', 'Networks', ...)
SUBJECT_MAP: Dict[str, Dict[str, Any]] = {}

for teacher in TEACHERS:
    # Key by primary uppercase ID
    s_id = teacher["subject_id"]
    SUBJECT_MAP[s_id] = teacher
    
    # Key by lowercase ID
    SUBJECT_MAP[s_id.lower()] = teacher
    
    # Key by subject code
    SUBJECT_MAP[teacher["subject_code"]] = teacher
    SUBJECT_MAP[teacher["subject_code"].lower()] = teacher
    
    # Key by full subject name
    SUBJECT_MAP[teacher["subject_name"]] = teacher
    SUBJECT_MAP[teacher["subject_name"].lower()] = teacher
    
    # Key by short name
    SUBJECT_MAP[teacher["short_name"]] = teacher
    SUBJECT_MAP[teacher["short_name"].lower()] = teacher

# Explicit module exports
__all__ = ["TEACHERS", "SUBJECT_MAP"]
