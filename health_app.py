import streamlit as st

st.title("Symptom-Based Health Screening App")

st.warning("This app is for educational screening only. It does not provide medical diagnosis or prescription.")

name = st.text_input("Patient Name")

st.subheader("Select Symptoms")

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

if st.button("Analyze Symptoms"):

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
        "COVID-19-like symptoms": covid_score,
        "Allergic Rhinitis": allergy_score,
        "Stomach Flu / Gastroenteritis": stomach_flu_score
    }

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    st.subheader(f"{name}'s Screening Result")

    top_disease, top_score = sorted_results[0]

    st.write("Most likely condition:")
    st.success(f"{top_disease}: {top_score}%")

    st.write("Other possibilities:")
    for disease, score in sorted_results[1:]:
        st.write(f"{disease}: {score}%")

    st.subheader("Recommended Action")

    if shortness_breath or top_score >= 70:
        st.error("Medical attention is recommended, especially if symptoms are severe or worsening.")
    elif fever or muscle_pain or fatigue:
        st.warning("Rest, hydration, and symptom monitoring are recommended.")
    else:
        st.info("Symptoms appear mild. Continue monitoring your condition.")

    st.caption("This result is not a medical diagnosis. Please consult a healthcare professional for accurate diagnosis and treatment.")

st.markdown("---")

if st.button("New Patient"):
    st.rerun()