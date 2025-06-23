import streamlit as st
import sqlite3

# DB connection
conn = sqlite3.connect("finwise_users.db", check_same_thread=False)
cursor = conn.cursor()

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0

def next_step():
    st.session_state.step += 1

st.title("💸 FinWise360: Financial Literacy & Fraud Awareness")

if st.session_state.step == 0:
    st.subheader("Step 1: User Details")
    name = st.text_input("Name")
    age = st.number_input("Age", 10, 100, 25)
    income = st.number_input("Monthly Income", 1000, 100000, 30000)
    goal = st.selectbox("Main Financial Goal", ["Savings", "Investing", "Retirement"])
    if st.button("Next"):
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.income = income
        st.session_state.goal = goal
        next_step()

elif st.session_state.step == 1:
    st.subheader("Step 2: Fraud Awareness Scenario")
    q = st.radio("You get an email from your bank asking to click a link and enter your OTP. What will you do?",
                 ["Click the link and enter OTP", "Ignore and delete the email", "Report it as phishing"])
    if st.button("Submit Answer"):
        if q == "Report it as phishing":
            st.success("Correct! This is the safest response.")
            st.session_state.score = 1
        else:
            st.warning("Wrong choice. Always verify with your bank first.")
        next_step()

elif st.session_state.step == 2:
    st.subheader("Step 3: Personalized Tip")
    goal = st.session_state.goal
    if goal == "Savings":
        st.info("Tip: Save at least 20% of income monthly.")
    elif goal == "Investing":
        st.info("Tip: Start SIPs in diversified mutual funds.")
    else:
        st.info("Tip: Consider long-term options like NPS and PPF.")
    if st.button("Finish"):
        cursor.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            income INTEGER,
            goal TEXT,
            score INTEGER
        )
        \"\"\")
        cursor.execute(\"\"\"
            INSERT INTO users (name, age, income, goal, score)
            VALUES (?, ?, ?, ?, ?)
        \"\"\", (st.session_state.name, st.session_state.age,
               st.session_state.income, st.session_state.goal,
               st.session_state.score))
        conn.commit()
        next_step()

elif st.session_state.step == 3:
    st.success("✅ All done! Your result is saved.")
    st.write(f"Thank you, {st.session_state.name}!")
    st.write(f"Your score: {st.session_state.score}/1")
    if st.button("Start Over"):
        st.session_state.step = 0
        st.session_state.score = 0
