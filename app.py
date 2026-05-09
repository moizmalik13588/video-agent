import streamlit as st
from main import run_pipeline
from core.rag_engine import ask_question

st.set_page_config(page_title="AI Meeting Assistant", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

    .stApp {
        background: #050a05 !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(16,185,80,0.13), transparent),
            radial-gradient(ellipse 50% 40% at 80% 90%, rgba(0,255,100,0.04), transparent) !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1300px !important;
    }

    /* ── Hero ── */
    .hero-wrap {
        position: relative;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(16,185,80,0.2);
        border-radius: 20px;
        overflow: hidden;
        background: rgba(16,185,80,0.03);
        text-align: center;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(16,185,80,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #10b950;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        border: 1px solid rgba(16,185,80,0.35);
        padding: 4px 12px;
        border-radius: 100px;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: clamp(2rem, 5vw, 6rem) !important;
        font-weight: 400 !important;
        color: #f0fdf0 !important;
        line-height: 1.05 !important;
        margin: 0 0 1rem !important;
        letter-spacing: 0.02em;
    }
    .hero-title span { color: #10b950; }
    .hero-sub {
        font-family: 'Barlow', sans-serif;
        font-size: clamp(0.85rem, 2vw, 1rem);
        font-weight: 300;
        color: rgba(240,253,240,0.45);
        margin: 0 auto 1.5rem;
        max-width: 480px;
        line-height: 1.7;
    }
    .hero-pills {
        display: flex;
        gap: 0.6rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    .hero-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: rgba(16,185,80,0.65);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: 1px solid rgba(16,185,80,0.18);
        padding: 4px 10px;
        border-radius: 100px;
        background: rgba(16,185,80,0.03);
    }

    /* ── Input form card ── */
    .input-section {
        background: rgba(16,185,80,0.03);
        border: 1px solid rgba(16,185,80,0.15);
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: rgba(16,185,80,0.05) !important;
        border: 1px solid rgba(16,185,80,0.22) !important;
        border-radius: 10px !important;
        color: #e2ffe8 !important;
        font-family: 'Barlow', sans-serif !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(16,185,80,0.6) !important;
        box-shadow: 0 0 0 3px rgba(16,185,80,0.08) !important;
    }
    input::placeholder { color: rgba(200,255,210,0.3) !important; }
    .stTextInput label, .stSelectbox label {
        color: rgba(200,255,210,0.55) !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 600 !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: #10b950 !important;
        color: #021a07 !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        white-space: nowrap !important;
        padding: 0.7rem 1.5rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #0dda5e !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(16,185,80,0.35) !important;
    }

    /* ── Result card ── */
    .res-card {
        background: rgba(16,185,80,0.04);
        border: 1px solid rgba(16,185,80,0.18);
        border-radius: 18px;
        padding: 1.75rem 2rem;
        margin-bottom: 2rem;
        animation: slideUp 0.5s ease forwards;
    }
    .res-card h2 {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: clamp(1.3rem, 3vw, 1.8rem) !important;
        font-weight: 600 !important;
        color: #10b950 !important;
        margin-bottom: 0.75rem !important;
    }
    .res-card p {
        color: rgba(240,253,240,0.72);
        line-height: 1.75;
        font-size: clamp(0.9rem, 2vw, 1.05rem);
        font-weight: 300;
        margin: 0;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 3px;
        background: rgba(16,185,80,0.04);
        padding: 5px;
        border-radius: 12px;
        border: 1px solid rgba(16,185,80,0.12);
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Barlow Condensed', sans-serif !important;
        color: rgba(200,255,210,0.45) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: clamp(0.72rem, 2vw, 0.88rem) !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.4rem 0.75rem !important;
        transition: all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(16,185,80,0.15) !important;
        color: #10b950 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(16,185,80,0.025);
        border: 1px solid rgba(16,185,80,0.1);
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 1.5rem !important;
        color: rgba(200,255,210,0.75) !important;
        line-height: 1.85;
        font-family: 'Barlow', sans-serif;
        font-weight: 300;
        font-size: clamp(0.88rem, 2vw, 1rem);
    }

    /* ── Chat ── */
    .chat-answer {
        background: rgba(16,185,80,0.07);
        border: 1px solid rgba(16,185,80,0.15);
        border-left: 3px solid #10b950;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        color: #e2ffe8;
        margin-bottom: 1rem;
        font-size: 0.95rem;
        line-height: 1.7;
        animation: slideUp 0.3s ease forwards;
    }
    .chat-q {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #10b950;
        margin-bottom: 0.25rem;
        font-weight: 600;
    }
    .chat-a { color: rgba(200,255,210,0.8); margin: 0; }

    div[data-testid="stForm"] {
        border: 1px solid rgba(16,185,80,0.18) !important;
        border-radius: 12px !important;
        background: rgba(16,185,80,0.03) !important;
        padding: 0.75rem !important;
    }

    .stAlert, div[data-baseweb="notification"] {
        background: rgba(16,185,80,0.06) !important;
        border: 1px solid rgba(16,185,80,0.25) !important;
        border-radius: 12px !important;
        color: rgba(200,255,210,0.8) !important;
        font-family: 'Barlow', sans-serif !important;
    }
    .stAlert svg { color: #10b950 !important; fill: #10b950 !important; }
    .stAlert strong { color: #10b950 !important; }

    .stSpinner > div { border-top-color: #10b950 !important; }
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #050a05; }
    ::-webkit-scrollbar-thumb { background: rgba(16,185,80,0.25); border-radius: 3px; }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# ── Session state ──
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ── Hero ──
st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">&nbsp;:: AI · MEETING · ASSISTANT&nbsp;</div>
    <h1 class="hero-title">Transform meetings into <span>insights.</span></h1>
    <p class="hero-sub">Paste a YouTube link or local file — get summary, action items, decisions, and an AI you can question.</p>
    <div class="hero-pills">
        <span class="hero-pill">✦ Transcription</span>
        <span class="hero-pill">✦ Summarization</span>
        <span class="hero-pill">✦ Action Items</span>
        <span class="hero-pill">✦ RAG Chat</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input — stacked layout (no columns) ──
source = st.text_input("YouTube URL or Local Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")
language = st.selectbox("Meeting Language", ["english", "hinglish"])
process_btn = st.button("🚀 Process Meeting", use_container_width=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Pipeline ──
if process_btn:
    if not source:
        st.warning("⚠️ Please enter a YouTube URL or file path first.")
    else:
        st.session_state.messages = []
        with st.spinner("✨ Transcribing & analysing your meeting…"):
            result = run_pipeline(source, language)
            st.session_state['result'] = result
        st.balloons()

# ── Results ──
if 'result' in st.session_state:
    res = st.session_state['result']

    st.markdown(
        f"<div class='res-card'><h2>📌 {res['title']}</h2><p>{res['summary']}</p></div>",
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs(["✅ Action Items", "🔑 Decisions", "❓ Questions", "💬 Chat"])

    with tab1: st.markdown(res['action_items'])
    with tab2: st.markdown(res['key_decisions'])
    with tab3: st.markdown(res['open_questions'])

    with tab4:
        st.markdown(
            "<p style='font-family:Barlow Condensed,sans-serif;font-size:0.78rem;letter-spacing:0.12em;text-transform:uppercase;color:#10b950;font-weight:600;margin-bottom:1rem;'>💬 Meeting Assistant</p>",
            unsafe_allow_html=True
        )
        for msg in st.session_state.messages:
            st.markdown(f"""
                <div class="chat-answer">
                    <div class="chat-q">You →</div>
                    <p class="chat-a" style="margin-bottom:0.5rem">{msg['question']}</p>
                    <div class="chat-q" style="color:rgba(16,185,80,0.6);margin-top:0.5rem">🤖 AI →</div>
                    <p class="chat-a">{msg['answer']}</p>
                </div>
            """, unsafe_allow_html=True)

        with st.form(key='chat_form', clear_on_submit=True):
            user_q = st.text_input("Ask about the meeting:", placeholder="What was decided about the budget?")
            submit_q = st.form_submit_button("Send ➤")
            if submit_q and user_q:
                with st.spinner("Thinking…"):
                    answer = ask_question(res['rag_chain'], user_q)
                st.session_state.messages.append({"question": user_q, "answer": answer})
                st.rerun()

else:
    st.info("👆 Enter a URL or file path above and hit **Process Meeting** to get started.")