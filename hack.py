import io
import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Study Hub",
    layout="wide",
    page_icon="🎓"
)

# ----------------- MODERN LIGHT THEME STYLING -----------------
st.markdown(
    """
    <style>
    /* 1. App background and default text */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    /* 2. COMPLETE FIX FOR TAB VISIBILITY */
    /* Target the tab list container */
    [data-testid="stTabs"] button {
        background-color: transparent !important;
        opacity: 1 !important;
    }
    
    /* Force ALL text and labels inside all tabs (unselected) to dark slate */
    [data-testid="stTabs"] button * {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        fill: #1e293b !important;
        opacity: 1 !important;
    }

    /* Active selected tab highlighted in vivid royal blue */
    [data-testid="stTabs"] button[aria-selected="true"] * {
        color: #2563eb !important;
        font-weight: 700 !important;
    }

    /* 3. Upload button clearly styled with a subtle border and visible text */
    [data-testid="stFileUploader"] button {
        background-color: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
        padding: 4px 12px !important;
    }
    [data-testid="stFileUploader"] button * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #e2e8f0 !important;
    }

    /* 4. Expander header and border */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* 5. Main action buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR CONFIGURATION -----------------
st.sidebar.header("⚙️ Configuration")
default_key = st.secrets.get("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input(
    "Gemini API Key:",
    value=default_key,
    type="password",
    help="Loaded automatically if configured in .streamlit/secrets.toml",
)

st.sidebar.divider()
st.sidebar.markdown(
    "**Solo Hackathon Project**  \n"
    "Stack: Streamlit + Gemini 3.5 Flash Lite"
)

# ----------------- HEADER & SHARED INPUT -----------------
st.title("🎓 Smart Study & Revision Assistant")
st.write("Upload a document or paste lecture notes below, then choose any revision tool from the tabs above.")

# Shared Document & Note Input Section
with st.expander("📂 **Input Source: Upload File or Paste Notes**", expanded=True):
    uploaded_file = st.file_uploader("Upload Study Document (TXT or PDF):", type=["txt", "pdf"])
    extracted_text = ""

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".txt"):
            extracted_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        st.success(f"Loaded '{uploaded_file.name}' successfully!")

    notes = st.text_area(
        "Lecture Notes / Topic Content:",
        value=extracted_text,
        height=180,
        placeholder="Type or paste your notes here, or upload a document above..."
    )

# ----------------- HELPER FUNCTION FOR GEMINI -----------------
def generate_ai_response(prompt_text):
    if not notes.strip():
        st.warning("⚠️ Please provide some notes or upload a file first!")
        return None
    if not api_key.strip():
        st.error("⚠️ Please provide a valid Gemini API key in the sidebar!")
        return None

    try:
        with st.spinner("AI is thinking..."):
            client = genai.Client(api_key=api_key.strip())
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt_text
            )
            return response.text
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# ----------------- MULTI-TAB NAVIGATION -----------------
tab_summary, tab_quiz, tab_eli5, tab_stats = st.tabs([
    "📝 Note Summarizer", 
    "❓ Practice Quiz", 
    "💡 Explain Like I'm 5", 
    "📊 Document Stats"
])

# --- TAB 1: SUMMARIZER ---
with tab_summary:
    st.subheader("Executive Study Summary")
    st.caption("Extracts key ideas and actionable takeaways for quick revision.")
    if st.button("Generate Summary", key="btn_summary"):
        prompt = (
            "Provide a clean, well-formatted bullet-point summary of these notes, "
            "followed by a separate section for 'Action Items / Takeaways':\n\n"
            f"{notes}"
        )
        result = generate_ai_response(prompt)
        if result:
            st.markdown(result)
            st.download_button("📥 Download Summary (.txt)", data=result, file_name="study_summary.txt")

# --- TAB 2: PRACTICE QUIZ ---
with tab_quiz:
    st.subheader("Interactive Revision Quiz")
    st.caption("Generates multiple-choice test questions directly from your materials.")
    if st.button("Generate 3 Quiz Questions", key="btn_quiz"):
        prompt = (
            "Generate 3 multiple-choice questions based on these notes.\n"
            "Format each question cleanly using standard Markdown like this:\n\n"
            "### Question 1: [Question text here]\n"
            "- A) Option 1\n"
            "- B) Option 2\n"
            "- C) Option 3\n"
            "- D) Option 4\n\n"
            "**Correct Answer:** [Letter]\n\n"
            "**Explanation:** [Brief reason]\n\n---\n\n"
            f"Notes:\n{notes}"
        )
        result = generate_ai_response(prompt)
        if result:
            st.markdown(result)
            st.download_button("📥 Download Quiz (.txt)", data=result, file_name="revision_quiz.txt")

# --- TAB 3: ELI5 EXPLAINER ---
with tab_eli5:
    st.subheader("Simple Analogy Breakdown (ELI5)")
    st.caption("Breaks down complex technical topics using relatable, everyday concepts.")
    if st.button("Explain Simply", key="btn_eli5"):
        prompt = (
            "Explain the main concepts in these notes in very simple terms using a real-world analogy "
            f"and zero technical jargon:\n\n{notes}"
        )
        result = generate_ai_response(prompt)
        if result:
            st.markdown(result)
            st.download_button("📥 Download Analogy (.txt)", data=result, file_name="eli5_explanation.txt")

# --- TAB 4: DOCUMENT STATS ---
with tab_stats:
    st.subheader("Text & Content Analytics")
    if notes.strip():
        words = len(notes.split())
        chars = len(notes)
        lines = len(notes.splitlines())
        reading_time_mins = round(words / 200, 1)  # Avg 200 wpm

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Word Count", words)
        col2.metric("Character Count", chars)
        col3.metric("Line Count", lines)
        col4.metric("Est. Reading Time", f"~{reading_time_mins} min")
    else:
        st.info("Paste some text or upload a document to view analytics.")