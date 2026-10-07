import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "roshinikalidoss@gmail.com"    
SENDER_PASSWORD = "odng licd pnxl tfed"   

def send_student_email(student_email, student_name, marks, fees,status):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = student_email
        msg['Subject'] = "BCA Marks & Fee Alert"
        
        body = f"Hello {student_name},\n\nYour marks: {marks}\nPending fees: {fees}\nStatus:{status}"

        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP Server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, student_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {student_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {student_email} .Error: {e}")
        import streamlit as st
        return False
import pandas as pd

# 1. Load the existing bca_students.csv file
csv_file = 'bca_students_new.csv'
df = pd.read_csv(csv_file)

# 2. Add 'email' and 'whatsapp_no' columns if they are not already present
# if 'email' not in df.columns:
#     df['email'] = [f"bca_student_{i+1}@college.edu" for i in range(len(df))]

# if 'whatsapp_no' not in df.columns:
#     df['whatsapp_no'] = [f"91987654{i:03d}" for i in range(len(df))]
# 3. Analyze each student's marks and pending fees
for index, row in df.iterrows():
    name = row.get('Student Name', 'Student')
    marks = row.get('marks', 0)
    if pd.isna(marks): marks = 0
    
    fees_due = row.get('fees_due', 0)
    if pd.isna(fees_due): fees_due = 0
    
    email = row['email']
    whatsapp = row['whatsapp_no']
    

    if marks < 50:
        status = "Low Scorer - Needs Motivation & Improvement"
    elif marks >= 85:
        status = "High Scorer - Excellent Performance"
    else:
        status = "Average Scorer - Keep it up"
        send_student_email(email,name,marks,fees_due,status)
    # Draft messages
    motivation_msg = f"Hello {name}, your performance status is '{status}' with {marks} marks. Focus on your subjects and work hard!"
    fee_msg = f" Reminder: Your pending college fee is Rs. {fees_due}. Please clear it soon." if fees_due > 0 else " Your fee dues are fully cleared!"
    
    final_alert = motivation_msg + fee_msg
    
    # Print simulation of sending email and whatsapp messages
    print(f"--- Alert for {name} ---")
    print(f"To Email ({email}): {final_alert}")
    print(f"To WhatsApp ({whatsapp}): {final_alert}\n")

# 4. Save the updated data back to bca_students.csv (with email and whatsapp)
df.to_csv(csv_file, index=False)
print("Success! 'bca_students_new.csv' updated with email and whatsapp numbers.")
# Total students count-a return panrathuku
def run_alerts():
    # (unga complete loop code inga irukkum)
    return len(df)