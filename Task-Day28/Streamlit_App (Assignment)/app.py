"""AI Text Assistant - a Streamlit web app powered by a Hugging Face model."""

import re
from datetime import datetime

import requests
import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
APP_TITLE = "AI Text Assistant"
APP_DESCRIPTION = (
    "Ask a question below and get an instant AI-generated response, "
    "powered by the lightweight `google/flan-t5-base` model from Hugging Face, "
    "grounded with live Wikipedia lookups to cut down on made-up answers."
)
MODEL_NAME = "google/flan-t5-base"
DEVELOPER_NAME = "Abhishek Venkatraman"
APP_VERSION = "1.0.0"
MAX_INPUT_CHARS = 500
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_CONTEXT_CHAR_LIMIT = 1000
WIKIPEDIA_HEADERS = {
    "User-Agent": f"{APP_TITLE}/{APP_VERSION} (Streamlit educational assignment)"
}


# --------------------------------------------------------------------------
# Model loading (cached so it only loads once per session)
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    """Load and cache the Hugging Face tokenizer and seq2seq model."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model


QUESTION_PREFIX_PATTERN = re.compile(
    r"^\s*(what|who|whom|whose|where|when|why|how)\s+(is|are|was|were|does|do|did)\s+"
    r"(the\s+)?|^\s*(tell me about|explain)\s+",
    re.IGNORECASE,
)
MATH_EXPRESSION_PATTERN = re.compile(r"^[\d\s+\-*/^%().]+\??$")


def simplify_search_query(question: str) -> str:
    """Strip common question wrappers so Wikipedia search matches the actual topic."""
    simplified = QUESTION_PREFIX_PATTERN.sub("", question).strip().rstrip("?").strip()
    return simplified or question


def fetch_wikipedia_context(query: str) -> str | None:
    """Look up a Wikipedia summary for the query to ground the model in real facts."""
    search_query = simplify_search_query(query)
    if MATH_EXPRESSION_PATTERN.match(search_query):
        return None
    try:
        search_resp = requests.get(
            WIKIPEDIA_API_URL,
            params={
                "action": "query",
                "list": "search",
                "srsearch": search_query,
                "format": "json",
                "srlimit": 1,
            },
            headers=WIKIPEDIA_HEADERS,
            timeout=5,
        )
        search_resp.raise_for_status()
        results = search_resp.json().get("query", {}).get("search", [])
        if not results:
            return None
        title = results[0]["title"]

        extract_resp = requests.get(
            WIKIPEDIA_API_URL,
            params={
                "action": "query",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "titles": title,
                "format": "json",
            },
            headers=WIKIPEDIA_HEADERS,
            timeout=5,
        )
        extract_resp.raise_for_status()
        pages = extract_resp.json().get("query", {}).get("pages", {})
        extract = next(iter(pages.values()), {}).get("extract", "").strip()
        return extract[:WIKIPEDIA_CONTEXT_CHAR_LIMIT] if extract else None
    except requests.RequestException:
        return None


def build_prompt(question: str, context: str | None) -> str:
    """Build the model prompt, grounding it in Wikipedia context when available."""
    if not context:
        return question
    return (
        "Answer the question using only the context below. "
        "If the context does not contain the answer, say you don't know.\n\n"
        f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    )


def generate_response(question: str, max_length: int, temperature: float) -> tuple[str, bool]:
    """Generate an AI response for the given question.

    Returns (response_text, was_grounded_in_wikipedia).
    """
    tokenizer, model = load_model()
    context = fetch_wikipedia_context(question)
    prompt = build_prompt(question, context)

    do_sample = temperature > 0.0
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    generate_kwargs = {
        "max_new_tokens": max_length,
        "do_sample": do_sample,
        "repetition_penalty": 1.3,
        "no_repeat_ngram_size": 3,
    }
    if do_sample:
        generate_kwargs["temperature"] = temperature
    output_ids = model.generate(**inputs, **generate_kwargs)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    return response, context is not None


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
def init_session_state():
    """Initialize chat history and confirmation flag in session state."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear = False


def add_to_history(question: str, response: str):
    """Append a question/response pair with a timestamp to chat history."""
    st.session_state.chat_history.append(
        {
            "question": question,
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def build_history_text() -> str:
    """Build a plain-text export of the chat history."""
    lines = []
    for entry in st.session_state.chat_history:
        lines.append(f"[{entry['timestamp']}]")
        lines.append(f"Q: {entry['question']}")
        lines.append(f"A: {entry['response']}")
        lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# UI sections
# --------------------------------------------------------------------------
def apply_theme():
    """Apply consistent custom theming across the app."""
    st.markdown(
        """
        <style>
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #4B8BBE;
        }
        .chat-box {
            max-height: 400px;
            overflow-y: auto;
            padding: 0.5rem;
            border: 1px solid #4B8BBE33;
            border-radius: 8px;
            background-color: rgba(75, 139, 190, 0.05);
        }
        .response-box {
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 300px;
            overflow-y: auto;
            padding: 0.75rem;
            border-radius: 8px;
            border: 1px solid #4B8BBE55;
            background-color: rgba(75, 139, 190, 0.08);
        }
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render the app title and description."""
    st.title(f"🤖 {APP_TITLE}")
    st.write(APP_DESCRIPTION)
    st.divider()


def render_sidebar() -> dict:
    """Render the sidebar with model settings and app info; return settings."""
    with st.sidebar:
        st.header("⚙️ Model Settings")
        max_length = st.slider(
            "Max output length",
            min_value=16,
            max_value=256,
            value=64,
            step=8,
            help="Maximum number of tokens the model may generate.",
        )
        temperature = st.slider(
            "Temperature (creativity)",
            min_value=0.0,
            max_value=1.5,
            value=0.7,
            step=0.1,
            help="Higher values produce more creative/random responses.",
        )

        st.divider()
        st.header("ℹ️ About this App")
        st.markdown(
            f"""
            This app is an **AI Text Assistant** built with Streamlit.

            - **Model:** `{MODEL_NAME}`
            - **Framework:** Hugging Face Transformers
            - **Purpose:** Ask questions, get AI-generated answers,
              and keep track of your conversation history.
            """
        )

    return {"max_length": max_length, "temperature": temperature}


def render_input_section() -> str:
    """Render the question input text area and return its value."""
    st.subheader("💬 Ask a Question")
    question = st.text_area(
        "Enter your question here:",
        height=120,
        max_chars=MAX_INPUT_CHARS,
        placeholder="e.g. What is the capital of France?",
    )
    st.caption(f"{len(question)}/{MAX_INPUT_CHARS} characters")
    return question


def render_chat_history():
    """Display previous questions and responses in a scrollable container."""
    st.subheader("🕑 Chat History")

    if not st.session_state.chat_history:
        st.info("No conversation yet. Ask a question above to get started.")
        return

    history_html = "<div class='chat-box'>"
    for entry in reversed(st.session_state.chat_history):
        history_html += (
            f"<p><b>🧑 [{entry['timestamp']}] You:</b><br>{entry['question']}</p>"
            f"<p><b>🤖 Assistant:</b><br>{entry['response']}</p><hr>"
        )
    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Download Chat History",
            data=build_history_text(),
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        render_clear_history_control()


def render_clear_history_control():
    """Render the clear-history button with a confirmation prompt."""
    if not st.session_state.confirm_clear:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.confirm_clear = True
            st.rerun()
    else:
        st.warning("Are you sure you want to clear the chat history?")
        yes_col, no_col = st.columns(2)
        with yes_col:
            if st.button("✅ Yes, clear it", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.confirm_clear = False
                st.rerun()
        with no_col:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()


def render_footer():
    """Render a footer with developer name and app version."""
    st.divider()
    st.markdown(
        f"<div style='text-align: center; color: gray;'>"
        f"Developed by <b>{DEVELOPER_NAME}</b> &nbsp;|&nbsp; Version {APP_VERSION}"
        f"</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Main app
# --------------------------------------------------------------------------
def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🤖", layout="centered")
    apply_theme()
    init_session_state()

    render_header()
    settings = render_sidebar()

    main_col, = st.columns(1)
    with main_col:
        question = render_input_section()
        generate_clicked = st.button("🚀 Generate Response", type="primary")

        if generate_clicked:
            if not question or not question.strip():
                st.error("⚠️ Please enter a question before generating a response.")
            elif len(question) > MAX_INPUT_CHARS:
                st.warning(
                    f"⚠️ Your input exceeds the {MAX_INPUT_CHARS}-character limit. "
                    "Please shorten it."
                )
            else:
                with st.spinner("Looking up facts and generating response..."):
                    response, grounded = generate_response(
                        question,
                        max_length=settings["max_length"],
                        temperature=settings["temperature"],
                    )
                add_to_history(question, response)
                st.subheader("✅ Response")
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)
                if grounded:
                    st.caption("📚 Grounded in a live Wikipedia lookup.")
                else:
                    st.caption(
                        "⚠️ No matching Wikipedia article found — this answer is "
                        "AI-generated only and may be inaccurate."
                    )

        st.divider()
        render_chat_history()

    render_footer()


if __name__ == "__main__":
    main()
