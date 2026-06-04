import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="DICS Self-Diagnosis System",
    layout="centered"
)

records_file = "screening_records.csv"

if not os.path.exists(records_file):
    pd.DataFrame(columns=[
        "time", "student_name", "grade", "gender",
        "health_score", "top_condition", "top_score"
    ]).to_csv(records_file, index=False, encoding="utf-8-sig")

st.title("DICS Self-Diagnosis System")
st.write("Health screening application for DICS students.")

st.warning(
    "This app is for educational health screening only. "
    "It does not provide medical diagnosis or prescription."
)

st.markdown("---")

if "form_key" not in st.session_state:
    st.session_state.form_key = 0

with st.form(f"diagnosis_form_{st.session_state.form_key}"):
    student_name = st.text_input("Student Name")

    grade = st.selectbox(
        "Grade",
        ["Select grade", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"]
    )

    gender = st.radio("Gender", ["Male", "Female", "Other"])

    st.subheader("Basic Health Information")

    height_cm = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=220.0,
        value=170.0,
        step=1.0
    )

    weight_kg = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=150.0,
        value=60.0,
        step=1.0
    )

    sleep_hours = st.slider(
        "Sleep Hours Last Night",
        0,
        12,
        7
    )

    stress_level = st.slider(
        "Stress Level",
        1,
        10,
        5
    )

    st.subheader("Select Your Symptoms")

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    sore_throat = st.checkbox("Sore throat")
    runny_nose = st.checkbox("Runny nose")
    headache = st.checkbox("Headache")
    muscle_pain = st.checkbox("Muscle pain")
    fatigue = st.checkbox("Fatigue")
    shortness_breath = st.checkbox("Shortness of breath")
    vomiting = st.checkbox("Vomiting")
    diarrhea = st.checkbox("Diarrhea")

    submitted = st.form_submit_button("Analyze Symptoms")

if submitted:
    if student_name == "" or grade == "Select grade":
        st.error("Please enter your name and grade first.")

    else:
        cold_score = 0
        flu_score = 0
        covid_score = 0
        allergy_score = 0
        stomach_flu_score = 0

        if fever:
            flu_score += 25
            covid_score += 20
            stomach_flu_score += 10

        if cough:
            cold_score += 25
            flu_score += 15
            covid_score += 20

        if sore_throat:
            cold_score += 20
            flu_score += 10
            covid_score += 10

        if runny_nose:
            cold_score += 25
            allergy_score += 30

        if headache:
            flu_score += 15
            covid_score += 10

        if muscle_pain:
            flu_score += 25
            covid_score += 10

        if fatigue:
            flu_score += 20
            covid_score += 15
            stomach_flu_score += 10

        if shortness_breath:
            covid_score += 30

        if vomiting:
            stomach_flu_score += 35

        if diarrhea:
            stomach_flu_score += 35

        results = {
            "Common Cold": cold_score,
            "Flu": flu_score,
            "COVID-19-like Symptoms": covid_score,
            "Allergic Rhinitis": allergy_score,
            "Stomach Flu / Gastroenteritis": stomach_flu_score
        }

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        top_disease, top_score = sorted_results[0]

        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Healthy Weight"
        elif bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obesity Range"

        health_score = 100
        health_score -= top_score * 0.4

        if bmi_category != "Healthy Weight":
            health_score -= 10

        if sleep_hours < 6:
            health_score -= 15
        elif sleep_hours < 7:
            health_score -= 8

        if stress_level >= 8:
            health_score -= 15
        elif stress_level >= 6:
            health_score -= 8

        if shortness_breath:
            health_score -= 20

        health_score = max(0, min(100, int(health_score)))

        new_record = pd.DataFrame([{
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "student_name": student_name,
            "grade": grade,
            "gender": gender,
            "health_score": health_score,
            "top_condition": top_disease,
            "top_score": top_score
        }])

        new_record.to_csv(
            records_file,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig"
        )

        st.markdown("---")
        st.subheader(f"{student_name}'s Screening Result")

        st.write("Grade:", grade)
        st.write("Gender:", gender)

        st.subheader("Overall Health Score")

        if health_score >= 80:
            st.success(f"{health_score}/100 - Good Condition")
        elif health_score >= 60:
            st.warning(f"{health_score}/100 - Moderate Risk")
        else:
            st.error(f"{health_score}/100 - High Risk")

        st.write(f"BMI: {bmi:.1f}")
        st.write(f"BMI Category: {bmi_category}")
        st.write(f"Sleep Hours: {sleep_hours} hours")
        st.write(f"Stress Level: {stress_level}/10")

        st.subheader("Disease Possibility")

        if top_score >= 70:
            st.error(f"Most likely condition: {top_disease}: {top_score}%")
        elif top_score >= 40:
            st.warning(f"Most likely condition: {top_disease}: {top_score}%")
        else:
            st.info(f"Most likely condition: {top_disease}: {top_score}%")

        st.write("Other possibilities:")
        for disease, score in sorted_results[1:]:
            st.write(f"{disease}: {score}%")

        st.subheader("Detailed Feedback")

        if health_score >= 80:
            st.success("Your overall condition appears stable based on the information you entered.")
        elif health_score >= 60:
            st.warning("Some risk factors were detected. Monitor your symptoms, rest well, and stay hydrated.")
        else:
            st.error("Several risk factors were detected. Please consider visiting the school nurse or a healthcare professional.")

        if bmi_category == "Underweight":
            st.info("Your BMI is below the general healthy range. Regular meals and balanced nutrition may be helpful.")
        elif bmi_category == "Overweight":
            st.info("Your BMI is above the general healthy range. Regular physical activity and balanced eating habits may help.")
        elif bmi_category == "Obesity Range":
            st.warning("Your BMI is in a higher range. This is not a diagnosis, but professional health guidance may be helpful.")

        if sleep_hours < 6:
            st.warning("Your sleep time is low. Lack of sleep can affect concentration, immune function, and recovery.")
        elif sleep_hours < 7:
            st.info("Your sleep time is slightly low. Try to maintain a more regular sleep schedule.")

        if stress_level >= 8:
            st.warning("Your stress level is high. Taking breaks, reducing screen time before sleep, and talking to a trusted adult may help.")
        elif stress_level >= 6:
            st.info("Your stress level is moderate. Continue monitoring your mental and physical condition.")

        if shortness_breath:
            st.error("Shortness of breath can be a serious warning sign. Please visit the school nurse or seek medical help immediately.")

        st.subheader("Symptom-Based Suggestions")

        if fever:
            st.write("- Fever: Drink plenty of water, rest, and monitor your temperature. If fever is high or lasts more than 2 days, visit the school nurse or a doctor.")

        if cough:
            st.write("- Cough: Drink warm fluids, avoid cold drinks, and wear a mask to reduce spreading infection.")

        if sore_throat:
            st.write("- Sore throat: Warm water gargling and voice rest may help. If pain is severe, seek medical advice.")

        if runny_nose:
            st.write("- Runny nose: It may be related to a cold or allergy. Avoid dust and stay hydrated.")

        if headache:
            st.write("- Headache: Rest in a quiet place, drink water, and reduce screen time.")

        if muscle_pain:
            st.write("- Muscle pain: Avoid intense physical activity and rest until symptoms improve.")

        if fatigue:
            st.write("- Fatigue: Sleep, hydration, and balanced meals are important for recovery.")

        if vomiting:
            st.write("- Vomiting: Drink small amounts of water frequently. Avoid heavy meals until symptoms improve.")

        if diarrhea:
            st.write("- Diarrhea: Hydration is very important. Avoid greasy food and dairy products temporarily.")

        if not any([
            fever, cough, sore_throat, runny_nose, headache,
            muscle_pain, fatigue, shortness_breath, vomiting, diarrhea
        ]):
            st.info("No major symptoms were selected. Continue maintaining healthy habits and monitor your condition.")

        st.caption(
            "This result is not a medical diagnosis. "
            "Please consult a healthcare professional for accurate diagnosis and treatment."
        )

st.markdown("---")

if st.button("New Student"):
    st.session_state.form_key += 1
    st.rerun()

st.markdown("---")
st.subheader("Screening Records")

records = pd.read_csv(records_file)

if records.empty:
    st.info("No students have been screened yet.")
else:
    for index, row in records.iterrows():
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"{row['time']} | {row['student_name']} | "
                f"{row['grade']} | Score: {row['health_score']} | "
                f"{row['top_condition']} ({row['top_score']}%)"
            )

        with col2:
            if st.button("Delete", key=f"delete_{index}"):
                records = records.drop(index)
                records.to_csv(records_file, index=False, encoding="utf-8-sig")
                st.rerun()

if st.button("Clear All Screening Records"):
    pd.DataFrame(columns=[
        "time", "student_name", "grade", "gender",
        "health_score", "top_condition", "top_score"
    ]).to_csv(records_file, index=False, encoding="utf-8-sig")

    st.success("All screening records cleared.")
    st.rerun()
