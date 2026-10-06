"""
chatbot_helper.py
AI Assistant for BCA Class Management & Topper Finder
Supports both Hugging Face Inference API and an instant, zero-latency Local Smart Query Engine.
Configured for the 5 BCA subjects:
- Fundamentals of Algorithm (T. Nagarathinam)
- Mobile Application Development (A. Narayanan)
- Computer Networks (K. Prakash)
- Web Technology (V. Bhuvaneshwari)
- Data Mining and Warehouse (S. Srinath)
"""

import re
import pandas as pd
from typing import Tuple, Dict, Any, List

SUBJECT_KEYS = {
    "foa": ("FOA_Total", "Fundamentals of Algorithm", "T. Nagarathinam", ["algorithm", "foa", "fundamentals of algorithm"]),
    "mad": ("MAD_Total", "Mobile Application Development", "A. Narayanan", ["mad", "mobile app", "mobile application", "android"]),
    "cn":  ("CN_Total", "Computer Networks", "K. Prakash", ["cn", "network", "networks", "computer networks"]),
    "wt":  ("WT_Total", "Web Technology", "V. Bhuvaneshwari", ["wt", "web tech", "web technology", "web"]),
    "dmw": ("DMW_Total", "Data Mining and Warehouse", "S. Srinath", ["dmw", "data mining", "data warehouse", "warehouse", "mining"])
}

def query_local_engine(query: str, df: pd.DataFrame, teachers: List[Dict[str, Any]]) -> str:
    """
    Intelligent NLP query engine answering questions about:
    - Overall Class Topper (out of 1500)
    - Subject Toppers (FOA, MAD, CN, WT, DMW)
    - Exam Toppers (CIA 1, CIA 2, Model)
    - Specific Student Lookup with 5-subject marks
    - Faculty allocation & Cabin/Contact lookup
    - Fee Pending & Low Mark Alerts
    - Class Statistics
    """
    q = query.lower().strip()
    
    # Ensure totals are present
    if "Overall_Total" not in df.columns:
        df["FOA_Total"] = df["FOA_CIA1"] + df["FOA_CIA2"] + df["FOA_Model"]
        df["MAD_Total"] = df["MAD_CIA1"] + df["MAD_CIA2"] + df["MAD_Model"]
        df["CN_Total"]  = df["CN_CIA1"]  + df["CN_CIA2"]  + df["CN_Model"]
        df["WT_Total"]  = df["WT_CIA1"]  + df["WT_CIA2"]  + df["WT_Model"]
        df["DMW_Total"] = df["DMW_CIA1"] + df["DMW_CIA2"] + df["DMW_Model"]
        df["Overall_Total"] = df["FOA_Total"] + df["MAD_Total"] + df["CN_Total"] + df["WT_Total"] + df["DMW_Total"]
        df["Overall_Percentage"] = (df["Overall_Total"] / 1500.0) * 100.0

    # 1. Subject-specific Topper Query
    for s_key, (tot_col, s_name, fac_name, aliases) in SUBJECT_KEYS.items():
        if any(a in q for a in aliases) and any(w in q for w in ["topper", "highest", "rank 1", "top mark", "first", "best"]):
            max_val = df[tot_col].max()
            subj_toppers = df[df[tot_col] == max_val]
            res = f"🏆 **Subject Topper: {s_name}**\n\n"
            res += f"- **Faculty In-Charge:** `{fac_name}`\n"
            res += f"- **Highest Total Score:** **{max_val} / 300 Marks** ({(max_val/3):.2f}%)\n\n"
            for _, s in subj_toppers.iterrows():
                res += (
                    f"🥇 **{s['Student Name']}** (`{s['Register Number']}`)\n"
                    f"   - CIA 1: `{s[f'{s_key.upper()}_CIA1']}/100` | CIA 2: `{s[f'{s_key.upper()}_CIA2']}/100` | Model: `{s[f'{s_key.upper()}_Model']}/100`\n"
                    f"   - Mobile: `{s['Mobile Number']}` | Fee Status: `{s['Fee Status']}`\n"
                )
            return res

    # 2. Overall Class Topper
    if any(k in q for k in ["overall topper", "first rank", "rank 1", "class topper", "highest total", "who topped the class", "highest marks overall", "topper of the class"]):
        top_idx = df["Overall_Total"].idxmax()
        topper = df.loc[top_idx]
        pct = (topper["Overall_Total"] / 1500.0) * 100.0
        return (
            f"🏆 **Overall BCA Class Topper: {topper['Student Name']}**\n\n"
            f"- **Register Number:** `{topper['Register Number']}`\n"
            f"- **Grand Total:** **{topper['Overall_Total']} / 1500 Marks** ({pct:.2f}% Distinction)\n"
            f"- **Subject Performance Breakdown (out of 300):**\n"
            f"  - 🧠 **Fundamentals of Algorithm:** `{topper['FOA_Total']}/300` (CIA1: {topper['FOA_CIA1']}, CIA2: {topper['FOA_CIA2']}, Model: {topper['FOA_Model']})\n"
            f"  - 📱 **Mobile App Development:** `{topper['MAD_Total']}/300` (CIA1: {topper['MAD_CIA1']}, CIA2: {topper['MAD_CIA2']}, Model: {topper['MAD_Model']})\n"
            f"  - 🌐 **Computer Networks:** `{topper['CN_Total']}/300` (CIA1: {topper['CN_CIA1']}, CIA2: {topper['CN_CIA2']}, Model: {topper['CN_Model']})\n"
            f"  - 💻 **Web Technology:** `{topper['WT_Total']}/300` (CIA1: {topper['WT_CIA1']}, CIA2: {topper['WT_CIA2']}, Model: {topper['WT_Model']})\n"
            f"  - 📦 **Data Mining & Warehouse:** `{topper['DMW_Total']}/300` (CIA1: {topper['DMW_CIA1']}, CIA2: {topper['DMW_CIA2']}, Model: {topper['DMW_Model']})\n"
            f"- **Fee Status:** {topper['Fee Status']} | 📱 Mobile: `{topper['Mobile Number']}`\n\n"
            f"🎖️ Heartiest congratulations to {topper['Student Name']}!"
        )

    # 3. Overall Exam Toppers (CIA 1, CIA 2, Model across 5 subjects)
    if any(k in q for k in ["cia 1 topper", "cia1 topper", "highest in cia 1", "topped cia 1", "cia-1 topper"]):
        if "Total_CIA1" in df.columns:
            max_m = df["Total_CIA1"].max()
            toppers = df[df["Total_CIA1"] == max_m]
            res = f"🥇 **Overall CIA 1 Exam Topper (Across all 5 subjects - Score: {max_m}/500)**\n\n"
            for _, s in toppers.iterrows():
                res += f"- **{s['Student Name']}** (`{s['Register Number']}`) — Total CIA 1: **{max_m}/500** | Mobile: `{s['Mobile Number']}`\n"
            return res

    if any(k in q for k in ["cia 2 topper", "cia2 topper", "highest in cia 2", "topped cia 2", "cia-2 topper"]):
        if "Total_CIA2" in df.columns:
            max_m = df["Total_CIA2"].max()
            toppers = df[df["Total_CIA2"] == max_m]
            res = f"🥈 **Overall CIA 2 Exam Topper (Across all 5 subjects - Score: {max_m}/500)**\n\n"
            for _, s in toppers.iterrows():
                res += f"- **{s['Student Name']}** (`{s['Register Number']}`) — Total CIA 2: **{max_m}/500** | Mobile: `{s['Mobile Number']}`\n"
            return res

    if any(k in q for k in ["model topper", "model exam topper", "highest in model", "topped model"]):
        if "Total_Model" in df.columns:
            max_m = df["Total_Model"].max()
            toppers = df[df["Total_Model"] == max_m]
            res = f"🥉 **Overall Model Exam Topper (Across all 5 subjects - Score: {max_m}/500)**\n\n"
            for _, s in toppers.iterrows():
                res += f"- **{s['Student Name']}** (`{s['Register Number']}`) — Total Model: **{max_m}/500** | Mobile: `{s['Mobile Number']}`\n"
            return res

    # 4. Teacher / Faculty Queries
    for t in teachers:
        subj_words = [w for w in re.findall(r'\b\w+\b', t["subject_name"].lower()) if len(w) > 2]
        teacher_parts = [w for w in re.findall(r'\b\w+\b', t["teacher_name"].lower()) if len(w) > 2]
        
        if any(w in q for w in subj_words) or any(w in q for w in teacher_parts) or t["subject_code"].lower() in q or t["short_name"].lower() in q:
            return (
                f"👨‍🏫 **Faculty Profile: {t['teacher_name']}**\n\n"
                f"- **Subject Handled:** **{t['subject_name']}** (`{t['subject_code']}`)\n"
                f"- **Designation:** {t['designation']} ({t['qualification']})\n"
                f"- **Cabin Location:** {t['cabin']}\n"
                f"- **Office Hours:** {t['office_hours']}\n"
                f"- **Weekly Load:** {t['credits']} Credits ({t['hours_per_week']} hrs/week)\n"
                f"- **Contact:** 📧 [{t['email']}](mailto:{t['email']}) | 📱 `{t['mobile']}`\n"
                f"- **Core Syllabus Topics:** {t['syllabus_highlight']}"
            )
            
    if any(k in q for k in ["who teaches", "teachers", "faculty", "staff", "professors", "subjects"]):
        res = "📚 **BCA Faculty & Subjects Allocation:**\n\n"
        for t in teachers:
            res += f"- **{t['subject_name']}** (`{t['subject_code']}`): **{t['teacher_name']}** ({t['designation']}, Cabin: {t['cabin']})\n"
        return res

    # 5. Specific Student by Register Number regex (e.g. 24BCA017)
    reg_match = re.search(r'24bca\d{3}', q)
    if reg_match:
        target_reg = reg_match.group(0).upper()
        found = df[df["Register Number"].str.upper() == target_reg]
        if not found.empty:
            s = found.iloc[0]
            pct = (s['Overall_Total'] / 1500.0) * 100.0
            fee_pill = "✅ Paid" if s['Fee Status'] == 'Paid' else "⚠️ Pending"
            return (
                f"👤 **Student Record: {s['Student Name']}**\n\n"
                f"- **Register Number:** `{s['Register Number']}` | 📱 **Mobile:** `{s['Mobile Number']}`\n"
                f"- **Fee Status:** {fee_pill}\n"
                f"- **Grand Total:** **{s['Overall_Total']} / 1500 Marks** ({pct:.1f}%)\n\n"
                f"📊 **Subject Marks Breakdown:**\n"
                f"- **Fundamentals of Algorithm:** `{s['FOA_Total']}/300` (CIA1: {s['FOA_CIA1']}, CIA2: {s['FOA_CIA2']}, Model: {s['FOA_Model']})\n"
                f"- **Mobile App Dev (MAD):** `{s['MAD_Total']}/300` (CIA1: {s['MAD_CIA1']}, CIA2: {s['MAD_CIA2']}, Model: {s['MAD_Model']})\n"
                f"- **Computer Networks:** `{s['CN_Total']}/300` (CIA1: {s['CN_CIA1']}, CIA2: {s['CN_CIA2']}, Model: {s['CN_Model']})\n"
                f"- **Web Technology:** `{s['WT_Total']}/300` (CIA1: {s['WT_CIA1']}, CIA2: {s['WT_CIA2']}, Model: {s['WT_Model']})\n"
                f"- **Data Mining & Warehouse:** `{s['DMW_Total']}/300` (CIA1: {s['DMW_CIA1']}, CIA2: {s['DMW_CIA2']}, Model: {s['DMW_Model']})"
            )

    # 6. Student Search by Name
    for _, s in df.iterrows():
        s_name_lower = s["Student Name"].lower()
        name_parts = s_name_lower.split()
        if s_name_lower in q or (len(name_parts[0]) > 3 and name_parts[0] in q):
            pct = (s['Overall_Total'] / 1500.0) * 100.0
            fee_pill = "✅ Paid" if s['Fee Status'] == 'Paid' else "⚠️ Pending"
            return (
                f"👤 **Found Student: {s['Student Name']}** (`{s['Register Number']}`)\n\n"
                f"- **Mobile:** `{s['Mobile Number']}` | **Fee Status:** {fee_pill}\n"
                f"- **Grand Total:** **{s['Overall_Total']} / 1500 Marks** ({pct:.1f}%)\n"
                f"- **FOA:** `{s['FOA_Total']}/300` | **MAD:** `{s['MAD_Total']}/300` | **CN:** `{s['CN_Total']}/300`\n"
                f"- **WT:** `{s['WT_Total']}/300` | **DMW:** `{s['DMW_Total']}/300`"
            )

    # 7. Fee Pending Query
    if any(k in q for k in ["fee pending", "pending fee", "fees pending", "unpaid fee", "due fee", "who has not paid"]):
        pending_df = df[df["Fee Status"] == "Pending"]
        count = len(pending_df)
        res = f"⚠️ **Students with Pending Fees ({count} out of {len(df)}):**\n\n"
        for _, s in pending_df.iterrows():
            res += f"- `{s['Register Number']}`: **{s['Student Name']}** (📱 `{s['Mobile Number']}`)\n"
        res += "\n💡 *Tip: Go to the 'Fee & Alert' tab to simulate sending instant SMS fee reminders.*"
        return res

    # 8. Low Marks / Academic Alert Query
    if any(k in q for k in ["low mark", "failed", "less than 40", "need improvement", "arrear", "poor marks", "below 40", "attention"]):
        exam_cols = [
            "FOA_CIA1", "FOA_CIA2", "FOA_Model",
            "MAD_CIA1", "MAD_CIA2", "MAD_Model",
            "CN_CIA1", "CN_CIA2", "CN_Model",
            "WT_CIA1", "WT_CIA2", "WT_Model",
            "DMW_CIA1", "DMW_CIA2", "DMW_Model"
        ]
        low_df = df[(df[exam_cols] < 40).any(axis=1)]
        count = len(low_df)
        res = f"🚨 **Students with Low Marks (&lt; 40 in one or more exams - {count} students):**\n\n"
        for _, s in low_df.head(10).iterrows():
            low_subjects = []
            for col in exam_cols:
                if s[col] < 40:
                    low_subjects.append(f"{col.replace('_', ' ')}: {s[col]}")
            res += f"- `{s['Register Number']}` **{s['Student Name']}**: {', '.join(low_subjects[:3])}\n"
        if count > 10:
            res += f"\n*(Showing 10 of {count} students. View all in the Alert tab)*"
        return res

    # 9. Class Statistics / Averages
    if any(k in q for k in ["class average", "average", "statistics", "stats", "pass percentage", "class strength", "total students"]):
        total_students = len(df)
        avg_total = df["Overall_Total"].mean()
        avg_pct = df["Overall_Percentage"].mean()
        paid_count = (df["Fee Status"] == "Paid").sum()
        pending_count = (df["Fee Status"] == "Pending").sum()
        
        return (
            f"📊 **BCA Class 2024–2027 Key Statistics (5 Subjects):**\n\n"
            f"- **Total Class Strength:** **{total_students} Students**\n"
            f"- **Overall Class Average:** **{avg_total:.1f} / 1500 Marks** ({avg_pct:.1f}%)\n"
            f"- **Subject Averages (out of 300):**\n"
            f"  - Fundamentals of Algorithm: `{df['FOA_Total'].mean():.1f}/300`\n"
            f"  - Mobile Application Dev (MAD): `{df['MAD_Total'].mean():.1f}/300`\n"
            f"  - Computer Networks: `{df['CN_Total'].mean():.1f}/300`\n"
            f"  - Web Technology: `{df['WT_Total'].mean():.1f}/300`\n"
            f"  - Data Mining and Warehouse: `{df['DMW_Total'].mean():.1f}/300`\n"
            f"- **Fee Collection:** {paid_count} Paid ({paid_count/total_students*100:.1f}%) | {pending_count} Pending ({pending_count/total_students*100:.1f}%)\n"
        )

    # 10. Greetings & Help
    if any(k in q for k in ["hello", "hi", "hey", "help", "who are you", "what can you do"]):
        return (
            "👋 **Hello! I am your BCA AI Class Assistant.**\n\n"
            "I can answer queries instantly about our 57 BCA students across all 5 subjects:\n"
            "- *'Who is the overall class topper?'*\n"
            "- *'Who topped Web Technology?'* or *'Who topped Algorithm?'*\n"
            "- *'Who topped Mobile Application Development?'*\n"
            "- *'Show students with pending fees'*\n"
            "- *'Who teaches Computer Networks or MAD?'*\n"
            "- *'Find details for student 24BCA017'* or *'Marks of Divya Pillai'*\n"
            "- *'Which students have low marks?'*\n\n"
            "💬 Type your question below!"
        )

    return (
        f"🤔 I didn't find an exact match for *'{query}'*.\n\n"
        "Here are common questions you can ask me:\n"
        "- 🏆 *'Who is the overall class topper?'*\n"
        "- 🥇 *'Who topped Fundamentals of Algorithm / Web Technology / CN / MAD / DMW?'*\n"
        "- 💰 *'List all students with pending fees'*\n"
        "- ⚠️ *'Who scored low marks?'*\n"
        "- 👨‍🏫 *'Who teaches Computer Networks?'*\n"
        "- 🔍 *'Tell me about [Student Name or Register No]'*\n"
        "- 📈 *'Show class averages'*."
    )


def ask_huggingface_assistant(
    prompt: str,
    df: pd.DataFrame,
    teachers: List[Dict[str, Any]],
    hf_token: str = "",
    hf_model: str = "Qwen/Qwen2.5-7B-Instruct"
) -> Tuple[str, str]:
    """
    Sends the request to Hugging Face Inference API if a token is present,
    or falls back seamlessly to the fast local query engine.
    """
    if not hf_token or not hf_token.strip():
        resp = query_local_engine(prompt, df, teachers)
        return resp, "Local BCA Engine"

    # Build concise context for Hugging Face LLM
    top_overall = df.loc[df["Overall_Total"].idxmax()]
    pending_count = (df["Fee Status"] == "Pending").sum()
    teachers_summary = "\n".join([f"- {t['subject_name']} ({t['subject_code']}): {t['teacher_name']} ({t['designation']})" for t in teachers])
    
    system_instruction = f"""You are the official AI Assistant for the BCA Department class of 57 students.
Academic Subjects (5 Core Subjects):
1. Fundamentals of Algorithm (FOA) - Faculty: T. Nagarathinam
2. Mobile Application Development (MAD) - Faculty: A. Narayanan
3. Computer Networks (CN) - Faculty: K. Prakash
4. Web Technology (WT) - Faculty: V. Bhuvaneshwari
5. Data Mining and Warehouse (DMW) - Faculty: S. Srinath

Exams conducted: CIA 1, CIA 2, Model Exam for each subject (Total: 1500 marks).
Overall Topper: {top_overall['Student Name']} ({top_overall['Register Number']}) with {top_overall['Overall_Total']}/1500 marks.
Fee status: {pending_count} pending, {len(df)-pending_count} paid.
Faculty directory:
{teachers_summary}

Be polite, accurate, concise and use clean markdown bullet points."""

    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=hf_token.strip())
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]
        
        completion = client.chat.completions.create(
            model=hf_model,
            messages=messages,
            max_tokens=450,
            temperature=0.3
        )
        
        output = completion.choices[0].message.content
        return output, f"Hugging Face ({hf_model.split('/')[-1]})"
    except Exception as e:
        fallback_resp = query_local_engine(prompt, df, teachers)
        return f"{fallback_resp}\n\n*(Note: Hugging Face API encountered: `{str(e)[:90]}...`. Switched to Local Smart Engine.)*", "Local Fallback"
