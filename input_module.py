import streamlit as st

def collect_profile():
    with st.form("profile_form"):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("Name", placeholder="Arun")
            age = st.number_input("Age", min_value=1, max_value=120, value=20)
            background = st.text_input("Educational / professional background")
            interests = st.text_area("Interests (comma-separated)")

        with c2:
            skill = st.selectbox(
                "Skill level", ["Beginner", "Intermediate", "Advanced"]
            )
            category = st.selectbox(
                "Preferred category",
                ["Practical learning", "Courses", "Books", "Projects",
                 "Career", "Tools", "General"]
            )
            goal = st.text_input("Goal", placeholder="Learn AI")
            count = st.slider("Number of recommendations", 1, 10, 5)

        submitted = st.form_submit_button("Submit profile")

    if submitted:
        if not name.strip() or not interests.strip() or not goal.strip():
            st.error("Please enter your name, interests, and goal.")
        else:
            st.session_state["submitted_profile"] = {
                "name": name.strip(),
                "age": int(age),
                "background": background.strip(),
                "interests": interests.strip(),
                "skill_level": skill,
                "preferred_category": category,
                "goal": goal.strip(),
                "number_of_recommendations": int(count),
            }

    return st.session_state.get("submitted_profile")