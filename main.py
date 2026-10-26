import streamlit as st

from input_module import collect_profile
from profile_module import analyze_profile
from prompt_module import build_prompt
from recommendation_module import generate_recommendations
from ranking_module import rank_recommendations
from feedback_module import refine_recommendations
from explanation_module import explain_recommendation
from intent_module import detect_intent
from save_module import save_recommendations, format_recommendations
from utils import check_ollama

st.set_page_config(
    page_title="Personalized Recommendation System",
    page_icon="🎯",
    layout="wide"
)

st.title("Personalized Recommendation System")
st.caption("Powered by Ollama and Qwen3:4b")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model = st.text_input("Ollama model", value="qwen3:4b")

    if st.button("Check Ollama connection"):
        ok, message = check_ollama(model)
        if ok:
            st.success(message)
        else:
            st.error(message)

# Profile collection
st.header("1. Build your user profile")
profile = collect_profile()

# Use stored profile after form submission
if profile:
    st.session_state["profile"] = profile

profile = st.session_state.get("profile")

if profile:
    st.success("Profile submitted successfully.")

    with st.expander("View your profile"):
        st.json(profile)

    # Recommendation generation
    if st.button(
        "Analyze profile and generate recommendations",
        type="primary",
        use_container_width=True
    ):
        st.write("Button clicked. Starting recommendation process...")

        try:
            with st.spinner("Step 1/2: Analyzing preferences..."):
                analysis = analyze_profile(profile, model)

            st.session_state["analysis"] = analysis
            st.success("Preference analysis completed.")

            prompt = build_prompt(profile, analysis)
            st.session_state["prompt"] = prompt

            with st.spinner("Step 2/2: Generating recommendations..."):
                results = generate_recommendations(prompt, model)

            if not results:
                st.error("No recommendations returned. Please try again.")
            else:
                st.session_state["recommendations"] = (
                    rank_recommendations(results)
                )
                st.success("Recommendations generated successfully!")

        except Exception as e:
            st.error(f"Generation failed: {e}")
            st.info(
                "Check that Ollama is running and the selected model "
                "is installed. See the VS Code terminal for more details."
            )

# Display analysis
if "analysis" in st.session_state:
    st.header("2. Preference analysis")
    st.write(st.session_state["analysis"])

if "prompt" in st.session_state:
    with st.expander("View constructed prompt"):
        st.code(st.session_state["prompt"])

# Display recommendations
if "recommendations" in st.session_state:
    recommendations = st.session_state["recommendations"]

    st.header("3. Personalized recommendations")

    for index, rec in enumerate(recommendations, start=1):
        with st.container(border=True):
            st.subheader(f"{index}. {rec.get('name', 'Recommendation')}")
            st.metric(
                "Suitability score",
                f"{rec.get('score', 0)}%"
            )
            st.write("**Reason:**", rec.get("reason", "Not provided."))

            if rec.get("details"):
                st.write("**Details:**", rec["details"])

    # Recommendation ranking
    st.header("4. Recommendation ranking")

    ranking_rows = [
        {
            "Rank": i,
            "Recommendation": rec.get("name", ""),
            "Score": f"{rec.get('score', 0)}%"
        }
        for i, rec in enumerate(recommendations, start=1)
    ]

    st.dataframe(ranking_rows, use_container_width=True)

    # Explanation
    st.header("5. Explain a recommendation")

    selected = st.selectbox(
        "Choose recommendation",
        range(len(recommendations)),
        format_func=lambda i: recommendations[i].get(
            "name", f"Recommendation {i + 1}"
        )
    )

    if st.button("Generate explanation"):
        try:
            with st.spinner("Generating explanation..."):
                explanation = explain_recommendation(
                    st.session_state["profile"],
                    recommendations[selected],
                    model
                )
            st.write(explanation)
        except Exception as e:
            st.error(f"Explanation failed: {e}")

    # Feedback and refinement
    st.header("6. Refine recommendations")

    feedback = st.text_area(
        "Enter your feedback",
        placeholder=(
            "I prefer hands-on AI projects and beginner-friendly "
            "resources. Avoid web development."
        )
    )

    if st.button("Refine recommendations"):
        if not feedback.strip():
            st.warning("Please enter your feedback.")
        else:
            try:
                with st.spinner("Refining recommendations..."):
                    refined = refine_recommendations(
                        st.session_state["profile"],
                        recommendations,
                        feedback,
                        model
                    )

                st.session_state["recommendations"] = (
                    rank_recommendations(refined)
                )
                st.session_state["last_feedback"] = feedback
                st.success("Recommendations refined.")
                st.rerun()

            except Exception as e:
                st.error(f"Refinement failed: {e}")

    # Intent detection
    st.header("7. Intent detection")

    request = st.text_input(
        "What would you like to do?",
        placeholder="Show my profile or explain recommendation 1"
    )

    if st.button("Detect intent"):
        if not request.strip():
            st.warning("Enter a request first.")
        else:
            try:
                with st.spinner("Detecting intent..."):
                    intent = detect_intent(request, model)
                st.info(f"Detected intent: {intent}")

                if intent == "SHOW_PROFILE":
                    st.json(st.session_state["profile"])
                elif intent == "EXIT":
                    st.session_state.clear()
                    st.rerun()
                elif intent == "SAVE_RECOMMENDATION":
                    path = save_recommendations(
                        st.session_state["profile"],
                        st.session_state["recommendations"],
                        st.session_state.get("last_feedback", "")
                    )
                    st.success(f"Saved to {path}")
                elif intent == "EXPLAIN_RECOMMENDATION":
                    with st.spinner("Generating explanation..."):
                        explanation = explain_recommendation(
                            st.session_state["profile"],
                            recommendations[0],
                            model
                        )
                    st.write(explanation)

            except Exception as e:
                st.error(f"Intent detection failed: {e}")

    # Save and download
    st.header("8. Save recommendations")

    if st.button("Save recommendations to file"):
        try:
            path = save_recommendations(
                st.session_state["profile"],
                st.session_state["recommendations"],
                st.session_state.get("last_feedback", "")
            )
            st.success(f"Saved successfully: {path}")
        except Exception as e:
            st.error(f"Saving failed: {e}")

    st.download_button(
        "Download recommendations",
        data=format_recommendations(
            st.session_state["profile"],
            st.session_state["recommendations"]
        ),
        file_name="recommendations.txt",
        mime="text/plain"
    )

st.divider()
st.caption(
    "Suitability scores are AI-generated estimates. "
    "Review recommendations before relying on them."
)
