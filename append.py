import os
from datetime import datetime, timezone, timedelta
import uuid # For generating UUIDs for auth.users references and class_name

# Import Supabase client and dotenv
from supabase import create_client, Client
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv() # This loads variables from the .env file into os.environ

# --- Supabase Configuration ---
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
    print("Please ensure you have a .env file in the same directory with these variables defined.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Helper for IST Time ---
def get_ist_time(days_ago=0, hours_ago=0, minutes_ago=0):
    """Returns a timezone-aware IST datetime object relative to now."""
    utc_now = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    target_time = utc_now + ist_offset - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return target_time

# --- Placeholder UUIDs for auth.users references ---
# These would typically come from your actual Supabase auth.users table
TEACHER_AUTH_UUID = str(uuid.uuid4())
STUDENT_AUTH_UUIDS = [str(uuid.uuid4()) for _ in range(4)] # For 4 students

# --- Start Data Insertion ---
print("Starting data insertion into Supabase (Max 5 rows per table)...")

try:
    # 1. School (Max 5 rows: 1 row)
    school_data = {
        "created_at": get_ist_time().isoformat(),
        "school_name": "Punjab Public School"
    }
    response = supabase.table('School').insert(school_data).execute()
    school_id = response.data[0]['id']
    print(f"Inserted School (ID: {school_id})")

    # 2. Class (Max 5 rows: 1 row)
    class_data = {
        "created_at": get_ist_time(minutes_ago=1).isoformat(),
        "class_name": str(uuid.uuid4()), # Generates a random UUID for class_name
        "batch": 2025,
        "school_id": school_id
    }
    response = supabase.table('Class').insert(class_data).execute()
    class_id = response.data[0]['id']
    print(f"Inserted Class (ID: {class_id})")

    # 3. Subject (Max 5 rows: 1 row)
    subject_data = {
        "created_at": get_ist_time(minutes_ago=2).isoformat(),
        "subject_name": "Science"
    }
    response = supabase.table('Subject').insert(subject_data).execute()
    subject_id = response.data[0]['id']
    print(f"Inserted Subject (ID: {subject_id})")

    # 4. User (Max 5 rows: 1 Teacher + 4 Students)
    user_data_to_insert = []
    user_data_to_insert.append({
        "created_at": get_ist_time(days_ago=5, hours_ago=1).isoformat(),
        "first_name": "Rachna", "last_name": "Verma",
        "email": "rachna.v@example.com", "role": "teacher"
    })
    # Students
    student_first_names = ["Priya", "Rohan", "Fatima", "Sameer"]
    for i, name in enumerate(student_first_names):
        user_data_to_insert.append({
            "created_at": get_ist_time(days_ago=4, hours_ago=1, minutes_ago=i).isoformat(),
            "first_name": name, "last_name": f"{name}wal", # Simple last names
            "email": f"{name.lower()}@example.com", "role": "student"
        })
    response = supabase.table('User').insert(user_data_to_insert).execute()
    public_user_ids = [user['id'] for user in response.data] # public_user_ids[0] for teacher, [1-4] for students
    print(f"Inserted Users (IDs: {public_user_ids})")

    # 5. Device (Max 5 rows: 1 for teacher, 4 for students, all device_type='sahayak')
    device_data = []
    device_data.append({
        "created_at": get_ist_time(days_ago=4, hours_ago=2).isoformat(),
        "device_name": "Rachna_sahayakx",
        "device_type": "sahayak",
        "user_id": TEACHER_AUTH_UUID
    })
    for i, student_uuid in enumerate(STUDENT_AUTH_UUIDS):
        device_data.append({
            "created_at": get_ist_time(days_ago=4, hours_ago=2, minutes_ago=i).isoformat(),
            "device_name": f"{student_first_names[i]}_sahayakx",
            "device_type": "sahayak",
            "user_id": student_uuid
        })
    response = supabase.table('Device').insert(device_data).execute()
    print(f"Inserted Devices ({len(response.data)} rows)")

    # 6. GuardRail (Max 5 rows: 2 rows)
    guardrail_data = []
    guardrail_data.append({"created_at": get_ist_time(days_ago=5, hours_ago=2).isoformat(), "prompt": "Discourage copying answers directly.", "intensity": 0.8})
    guardrail_data.append({"created_at": get_ist_time(days_ago=5, hours_ago=2, minutes_ago=1).isoformat(), "prompt": "Encourage detailed explanations for subjective questions.", "intensity": 0.6})
    response = supabase.table('GuardRail').insert(guardrail_data).execute()
    guardrail_ids = [g['id'] for g in response.data]
    print(f"Inserted GuardRails (IDs: {guardrail_ids})")

    # 7. Chapter (Max 5 rows: 4 chapters)
    chapter_data = []
    chapter_data.append({"created_at": get_ist_time(days_ago=3, hours_ago=1).isoformat(), "chapter_name": "Force and Pressure", "subject_id": subject_id}) # CH1
    chapter_data.append({"created_at": get_ist_time(days_ago=3, hours_ago=1, minutes_ago=1).isoformat(), "chapter_name": "Light", "subject_id": subject_id}) # CH2
    chapter_data.append({"created_at": get_ist_time(days_ago=3, hours_ago=1, minutes_ago=2).isoformat(), "chapter_name": "Sound", "subject_id": subject_id}) # CH3
    chapter_data.append({"created_at": get_ist_time(days_ago=3, hours_ago=1, minutes_ago=3).isoformat(), "chapter_name": "Chemical Effects of Electric Current", "subject_id": subject_id}) # CH4
    response = supabase.table('Chapter').insert(chapter_data).execute()
    chapter_ids = [ch['id'] for ch in response.data]
    print(f"Inserted Chapters (IDs: {chapter_ids})")

    # 8. Concept (Max 5 rows: 5 concepts across first 3 chapters)
    concept_data = []
    concept_data.append({"created_at": get_ist_time(days_ago=3, hours_ago=2).isoformat(), "concept_name": "Types of Force", "concept_description": "Explores contact and non-contact forces.", "chapter_id": chapter_ids[0]}) # C1
    concept_data.append({"created_at": get_ist_time(days_ago=3, hours_ago=2, minutes_ago=1).isoformat(), "concept_name": "Pressure in Fluids", "concept_description": "Understanding pressure exerted by liquids and gases.", "chapter_id": chapter_ids[0]}) # C2
    concept_data.append({"created_at": get_ist_time(days_ago=2, hours_ago=1).isoformat(), "concept_name": "Reflection of Light", "concept_description": "Laws of reflection and types of mirrors.", "chapter_id": chapter_ids[1]}) # C3
    concept_data.append({"created_at": get_ist_time(days_ago=2, hours_ago=1, minutes_ago=1).isoformat(), "concept_name": "Refraction of Light", "concept_description": "Bending of light as it passes through different media.", "chapter_id": chapter_ids[1]}) # C4
    concept_data.append({"created_at": get_ist_time(days_ago=2, hours_ago=1, minutes_ago=2).isoformat(), "concept_name": "Production of Sound", "concept_description": "How sound is produced by vibrations.", "chapter_id": chapter_ids[2]}) # C5
    response = supabase.table('Concept').insert(concept_data).execute()
    concept_ids = [c['id'] for c in response.data]
    print(f"Inserted Concepts (IDs: {concept_ids})")

    # 9. Rubric (Max 5 rows: 4 rows)
    rubric_data = []
    rubric_data.append({"created_at": get_ist_time(days_ago=1, hours_ago=3).isoformat(), "correct_marking": 2, "incorrect_marking": -1, "name": "Basic Assessment"}) # R1
    rubric_data.append({"created_at": get_ist_time(days_ago=1, hours_ago=3, minutes_ago=1).isoformat(), "correct_marking": 3, "incorrect_marking": -0.5, "name": "Fair Assessment"}) # R2
    rubric_data.append({"created_at": get_ist_time(days_ago=1, hours_ago=3, minutes_ago=2).isoformat(), "correct_marking": 4, "incorrect_marking": 0, "name": "Good Assessment"}) # R3
    rubric_data.append({"created_at": get_ist_time(days_ago=1, hours_ago=3, minutes_ago=3).isoformat(), "correct_marking": 5, "incorrect_marking": 0, "name": "Excellent Assessment"}) # R4
    response = supabase.table('Rubric').insert(rubric_data).execute()
    rubric_ids = [r['id'] for r in response.data]
    print(f"Inserted Rubrics (IDs: {rubric_ids})")

    # 10. QuestionOption (Max 5 rows: 5 options)
    question_option_data = []
    question_option_data.append({"created_at": get_ist_time(hours_ago=5).isoformat(), "option_text": "Push", "is_correct": False}) # QO1
    question_option_data.append({"created_at": get_ist_time(hours_ago=5, minutes_ago=1).isoformat(), "option_text": "Pull", "is_correct": False}) # QO2
    question_option_data.append({"created_at": get_ist_time(hours_ago=5, minutes_ago=2).isoformat(), "option_text": "Force", "is_correct": True}) # QO3 (for Q1)
    question_option_data.append({"created_at": get_ist_time(hours_ago=4).isoformat(), "option_text": "30 degrees", "is_correct": True}) # QO4 (for Q3)
    question_option_data.append({"created_at": get_ist_time(hours_ago=4, minutes_ago=1).isoformat(), "option_text": "Water", "is_correct": True}) # QO5 (for Q4)
    response = supabase.table('QuestionOption').insert(question_option_data).execute()
    question_option_ids = [qo['id'] for qo in response.data]
    print(f"Inserted Question Options (IDs: {question_option_ids})")

    # 11. Question (Max 5 rows: 4 questions)
    question_data = []
    question_data.append({"created_at": get_ist_time(hours_ago=3).isoformat(), "question_text": "What causes an object to change its state of motion?", "question_type": "MCQ", "rubric_id": rubric_ids[0], "options_id": question_option_ids[2], "concept_id": concept_ids[0]}) # Q1
    question_data.append({"created_at": get_ist_time(hours_ago=3, minutes_ago=1).isoformat(), "question_text": "Define pressure and state its unit.", "question_type": "Short Answer", "rubric_id": rubric_ids[0], "options_id": question_option_ids[0], "concept_id": concept_ids[1]}) # Q2
    question_data.append({"created_at": get_ist_time(hours_ago=2).isoformat(), "question_text": "If a light ray strikes a plane mirror at an angle of 30 degrees to the normal, what is the angle of reflection?", "question_type": "MCQ", "rubric_id": rubric_ids[1], "options_id": question_option_ids[3], "concept_id": concept_ids[2]}) # Q3
    question_data.append({"created_at": get_ist_time(hours_ago=2, minutes_ago=1).isoformat(), "question_text": "Name a liquid that conducts electricity.", "question_type": "Short Answer", "rubric_id": rubric_ids[1], "options_id": question_option_ids[4], "concept_id": concept_ids[3]}) # Q4
    response = supabase.table('Question').insert(question_data).execute()
    question_ids = [q['id'] for q in response.data]
    print(f"Inserted Questions (IDs: {question_ids})")

    # 12. Session (Max 5 rows: 4 sessions)
    session_data = []
    session_data.append({"created_at": get_ist_time(days_ago=3).isoformat(), "session_name": "Forces Intro", "start_time": get_ist_time(days_ago=3, hours_ago=1).replace(tzinfo=None).isoformat(), "end_time": get_ist_time(days_ago=3, minutes_ago=30).replace(tzinfo=None).isoformat(), "subject_id": subject_id, "teacher_id": TEACHER_AUTH_UUID}) # S1
    session_data.append({"created_at": get_ist_time(days_ago=2).isoformat(), "session_name": "Pressure Concepts", "start_time": get_ist_time(days_ago=2, hours_ago=1).replace(tzinfo=None).isoformat(), "end_time": get_ist_time(days_ago=2, minutes_ago=30).replace(tzinfo=None).isoformat(), "subject_id": subject_id, "teacher_id": TEACHER_AUTH_UUID}) # S2
    session_data.append({"created_at": get_ist_time(days_ago=1).isoformat(), "session_name": "Light Reflection", "start_time": get_ist_time(days_ago=1, hours_ago=1).replace(tzinfo=None).isoformat(), "end_time": get_ist_time(days_ago=1, minutes_ago=30).replace(tzinfo=None).isoformat(), "subject_id": subject_id, "teacher_id": TEACHER_AUTH_UUID}) # S3
    session_data.append({"created_at": get_ist_time(hours_ago=5).isoformat(), "session_name": "Electric Conduction", "start_time": get_ist_time(hours_ago=5, minutes_ago=30).replace(tzinfo=None).isoformat(), "end_time": get_ist_time(hours_ago=4, minutes_ago=30).replace(tzinfo=None).isoformat(), "subject_id": subject_id, "teacher_id": TEACHER_AUTH_UUID}) # S4
    response = supabase.table('Session').insert(session_data).execute()
    session_ids = [s['id'] for s in response.data]
    print(f"Inserted Sessions (IDs: {session_ids})")

    # 13. Worksheet (Max 5 rows: 4 worksheets)
    worksheet_data = []
    worksheet_data.append({"created_at": get_ist_time(days_ago=3, minutes_ago=20).isoformat(), "title": "Forces Q&A", "guardrail_id": guardrail_ids[0], "session_id": session_ids[0]}) # WS1
    worksheet_data.append({"created_at": get_ist_time(days_ago=2, minutes_ago=20).isoformat(), "title": "Pressure Problems", "guardrail_id": guardrail_ids[0], "session_id": session_ids[1]}) # WS2
    worksheet_data.append({"created_at": get_ist_time(days_ago=1, minutes_ago=20).isoformat(), "title": "Mirror Mania", "guardrail_id": guardrail_ids[1], "session_id": session_ids[2]}) # WS3
    worksheet_data.append({"created_at": get_ist_time(hours_ago=4, minutes_ago=20).isoformat(), "title": "Conductor Check", "guardrail_id": guardrail_ids[1], "session_id": session_ids[3]}) # WS4
    response = supabase.table('Worksheet').insert(worksheet_data).execute()
    worksheet_ids = [ws['id'] for ws in response.data]
    print(f"Inserted Worksheets (IDs: {worksheet_ids})")

    # 14. WorksheetGradingBatch (Max 5 rows: 1 batch)
    grading_batch_data = {
        "created_at": get_ist_time(hours_ago=1).isoformat(),
        "start_time": get_ist_time(hours_ago=1, minutes_ago=10).replace(tzinfo=None).isoformat(),
        "end_time": get_ist_time(minutes_ago=5).replace(tzinfo=None).isoformat()
    }
    response = supabase.table('WorksheetGradingBatch').insert(grading_batch_data).execute()
    batch_id = response.data[0]['id']
    print(f"Inserted WorksheetGradingBatch (ID: {batch_id})")

    # --- Data for student activity (focus on first student to fit 5 rows) ---
    # First student's UUID: STUDENT_AUTH_UUIDS[0]

    # 15. WorksheetQuestion (Max 5 rows: Priya attempts first 4 questions on Worksheet 1)
    wq_data = []
    for i, q_id in enumerate(question_ids):
        wq_data.append({
            "created_at": get_ist_time(hours_ago=3, minutes_ago=10 + i).isoformat(),
            "worksheet_id": worksheet_ids[0], # All for Worksheet 1
            "question_id": q_id,
            "user_id": STUDENT_AUTH_UUIDS[0] # Priya Sharma
        })
    response = supabase.table('WorksheetQuestion').insert(wq_data).execute()
    print(f"Inserted WorksheetQuestions ({len(response.data)} rows)")

    # 16. Resource (Max 5 rows: 2 submissions + 2 reports = 4 resources)
    resource_data = []
    resource_data.append({"created_at": get_ist_time(hours_ago=2, minutes_ago=30).isoformat(), "type": "document", "bucket": "worksheet-submissions", "identifier": "submission_priya_w1.pdf", "size": 150}) # R1 (W1 submission)
    resource_data.append({"created_at": get_ist_time(hours_ago=1, minutes_ago=30).isoformat(), "type": "document", "bucket": "worksheet-submissions", "identifier": "submission_priya_w2.pdf", "size": 160}) # R2 (W2 submission)
    resource_data.append({"created_at": get_ist_time(hours_ago=1, minutes_ago=20).isoformat(), "type": "document", "bucket": "worksheet-reports", "identifier": "report_priya_w1.pdf", "size": 200}) # R3 (W1 report)
    resource_data.append({"created_at": get_ist_time(minutes_ago=20).isoformat(), "type": "document", "bucket": "worksheet-reports", "identifier": "report_priya_w2.pdf", "size": 210}) # R4 (W2 report)
    response = supabase.table('Resource').insert(resource_data).execute()
    resource_ids = [r['id'] for r in response.data]
    print(f"Inserted Resources (IDs: {resource_ids})")

    # 17. WorksheetSubmission (Max 5 rows: Priya's submissions for W1, W2)
    submission_data = []
    submission_data.append({"created_at": get_ist_time(hours_ago=2, minutes_ago=25).isoformat(), "worksheet_id": worksheet_ids[0], "resource_id": resource_ids[0]}) # W1 submission
    submission_data.append({"created_at": get_ist_time(hours_ago=1, minutes_ago=25).isoformat(), "worksheet_id": worksheet_ids[1], "resource_id": resource_ids[1]}) # W2 submission
    response = supabase.table('WorksheetSubmission').insert(submission_data).execute()
    submission_ids = [s['id'] for s in response.data]
    print(f"Inserted WorksheetSubmissions (IDs: {submission_ids})")

    # 18. WorksheetGradingJob (Max 5 rows: Grading jobs for Priya's W1, W2 submissions)
    grading_job_data = []
    grading_job_data.append({
        "created_at": get_ist_time(hours_ago=2, minutes_ago=15).isoformat(),
        "worksheet_id": worksheet_ids[0],
        "start_time": get_ist_time(hours_ago=2, minutes_ago=15).replace(tzinfo=None).isoformat(),
        "end_time": get_ist_time(hours_ago=2, minutes_ago=10).replace(tzinfo=None).isoformat(),
        "status": "completed", "batch_id": batch_id
    }) # Job for W1
    grading_job_data.append({
        "created_at": get_ist_time(hours_ago=1, minutes_ago=15).isoformat(),
        "worksheet_id": worksheet_ids[1],
        "start_time": get_ist_time(hours_ago=1, minutes_ago=15).replace(tzinfo=None).isoformat(),
        "end_time": get_ist_time(hours_ago=1, minutes_ago=10).replace(tzinfo=None).isoformat(),
        "status": "completed", "batch_id": batch_id
    }) # Job for W2
    response = supabase.table('WorksheetGradingJob').insert(grading_job_data).execute()
    job_ids = [j['id'] for j in response.data]
    print(f"Inserted WorksheetGradingJobs (IDs: {job_ids})")

    # 19. WorksheetReport (Max 5 rows: Reports for Priya's W1, W2 jobs)
    report_data = []
    report_data.append({"created_at": get_ist_time(hours_ago=1, minutes_ago=5).isoformat(), "job_id": job_ids[0], "resource_id": resource_ids[2]}) # Report for W1
    report_data.append({"created_at": get_ist_time(minutes_ago=10).isoformat(), "job_id": job_ids[1], "resource_id": resource_ids[3]}) # Report for W2
    response = supabase.table('WorksheetReport').insert(report_data).execute()
    print(f"Inserted WorksheetReports ({len(response.data)} rows)")

    print("\nAll data insertion attempts complete. Check your Supabase project for inserted rows.")

except Exception as e:
    print(f"\nAn error occurred during data insertion: {e}")
    print("Please check:")
    print("1. Your .env file is correctly set up with SUPABASE_URL and SUPABASE_KEY.")
    print("2. Your Supabase tables exist and have correct 'Enable RLS' and 'Policy' settings for inserts (e.g., 'anon' role can insert).")
    print("3. Your foreign key references (especially user_id in Device, Session, WorksheetQuestion) match existing UUIDs in auth.users.")