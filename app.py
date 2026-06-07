import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Root tokens ─── */
:root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --border:    #1e2230;
    --accent:    #4f9cf9;
    --accent2:   #a78bfa;
    --warn:      #f59e0b;
    --success:   #34d399;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --font-head: 'DM Serif Display', Georgia, serif;
    --font-body: 'DM Sans', sans-serif;
    --font-mono: 'DM Mono', monospace;
}

/* ─── Global reset ─── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ─── Hide Streamlit chrome ─── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem !important; max-width: 1100px; }

/* ─── Hero ─── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: var(--font-head) !important;
    font-size: clamp(2.4rem, 5vw, 3.8rem) !important;
    font-weight: 400 !important;
    line-height: 1.1 !important;
    margin: 0 0 0.6rem !important;
    color: var(--text) !important;
    letter-spacing: -0.01em;
}
.hero h1 em {
    font-style: italic;
    color: var(--accent);
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}
.hero-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    margin: 1.8rem auto 0;
    border-radius: 2px;
}

/* ─── Search bar ─── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,156,249,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ─── Button ─── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ─── Pipeline stepper ─── */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    padding: 1.5rem 0 2rem;
    flex-wrap: wrap;
    row-gap: 1rem;
}
.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    min-width: 110px;
}
.step-dot {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    font-weight: 700;
    border: 2px solid var(--border);
    background: var(--surface);
    color: var(--muted);
    transition: all 0.4s;
    position: relative;
}
.step-dot.active  { border-color: var(--accent);  color: var(--accent);  box-shadow: 0 0 12px rgba(79,156,249,0.35); }
.step-dot.done    { border-color: var(--success); background: var(--success); color: #0a0c10; }
.step-dot.error   { border-color: #f87171; color: #f87171; }
.step-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
}
.step-label.active { color: var(--accent); }
.step-label.done   { color: var(--success); }
.connector {
    width: 48px; height: 2px;
    background: var(--border);
    margin-bottom: 18px;
    flex-shrink: 0;
}
.connector.done { background: linear-gradient(90deg, var(--success), var(--success)); }

/* ─── Result cards ─── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 14px 0 0 14px;
}
.card-search::before  { background: var(--accent); }
.card-reader::before  { background: var(--accent2); }
.card-writer::before  { background: var(--success); }
.card-critic::before  { background: var(--warn); }

.card-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1rem;
}
.card-icon {
    font-size: 1.15rem;
    width: 34px; height: 34px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(255,255,255,0.04);
}
.card-title {
    font-family: var(--font-head) !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    color: var(--text) !important;
    margin: 0 !important;
}
.card-badge {
    margin-left: auto;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid;
}
.badge-done  { color: var(--success); border-color: var(--success); background: rgba(52,211,153,0.08); }
.badge-run   { color: var(--accent);  border-color: var(--accent);  background: rgba(79,156,249,0.08); }
.badge-wait  { color: var(--muted);   border-color: var(--border);  background: transparent; }

/* ─── Expander override ─── */
.stExpander {
    background: transparent !important;
    border: none !important;
}
.stExpander > div > div {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.8rem 1rem !important;
}
.stExpander summary {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.05em;
}

/* ─── Text area (report display) ─── */
.report-body {
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.75;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ─── Metric row ─── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.metric-box {
    flex: 1; min-width: 130px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-value {
    font-family: var(--font-head);
    font-size: 1.6rem;
    color: var(--accent);
    display: block;
}
.metric-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.2rem;
    display: block;
}

/* ─── Status bar ─── */
.status-bar {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: var(--accent);
    letter-spacing: 0.08em;
    padding: 0.5rem 0.8rem;
    background: rgba(79,156,249,0.07);
    border: 1px solid rgba(79,156,249,0.18);
    border-radius: 6px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.pulse {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.3; transform: scale(0.7); }
}

/* ─── Download button ─── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1.5px solid var(--success) !important;
    color: var(--success) !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em;
    padding: 0.5rem 1.2rem !important;
}
.stDownloadButton > button:hover {
    background: rgba(52,211,153,0.1) !important;
}

/* ─── Divider ─── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ─── Spinner ─── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def render_pipeline_stepper(current_step: int, error: bool = False):
    steps = [
        ("🔍", "Search"),
        ("📄", "Reader"),
        ("✍️", "Writer"),
        ("🧐", "Critic"),
    ]
    html = '<div class="pipeline">'
    for i, (icon, label) in enumerate(steps):
        if i > 0:
            done_class = "done" if i < current_step else ""
            html += f'<div class="connector {done_class}"></div>'
        if i < current_step:
            dot_cls = "done"; lbl_cls = "done"; icon = "✓"
        elif i == current_step:
            dot_cls = "error" if error else "active"
            lbl_cls = "active"
        else:
            dot_cls = ""; lbl_cls = ""
        html += f"""
        <div class="step">
            <div class="step-dot {dot_cls}">{icon}</div>
            <div class="step-label {lbl_cls}">{label}</div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def card(title: str, icon: str, color_cls: str, badge: str, badge_cls: str, body):
    st.markdown(f"""
    <div class="result-card {color_cls}">
        <div class="card-header">
            <div class="card-icon">{icon}</div>
            <span class="card-title">{title}</span>
            <span class="card-badge {badge_cls}">{badge}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    with st.expander("View output", expanded=True):
        st.markdown(f'<div class="report-body">{body}</div>', unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "step", "error", "elapsed"):
    if key not in st.session_state:
        st.session_state[key] = None if key not in ("running", "error") else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent Pipeline</div>
    <h1>Research <em>Intelligence</em></h1>
    <p class="hero-sub">Four agents working in concert — searching, reading, writing, and critiquing — to produce a polished research brief in seconds.</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([5, 1.3], gap="small")
with col_in:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="Enter a research topic  e.g.  'Advances in quantum error correction 2024'",
        key="topic_input",
    )
with col_btn:
    run = st.button("Run Research ▶", use_container_width=True)

st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)


# ── Pipeline execution ────────────────────────────────────────────────────────
if run and topic.strip():
    st.session_state.running = True
    st.session_state.results = None
    st.session_state.error = False

    state = {}
    t_start = time.time()

    # ── Step 0: Search ──
    st.session_state.step = 0
    render_pipeline_stepper(0)
    st.markdown('<div class="status-bar"><span class="pulse"></span> Search agent querying the web…</div>', unsafe_allow_html=True)

    with st.spinner(""):
        try:
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content
        except Exception as e:
            st.error(f"Search agent failed: {e}")
            render_pipeline_stepper(0, error=True)
            st.stop()

    # ── Step 1: Reader ──
    st.session_state.step = 1
    render_pipeline_stepper(1)
    st.markdown('<div class="status-bar"><span class="pulse"></span> Reader agent scraping top resources…</div>', unsafe_allow_html=True)

    with st.spinner(""):
        try:
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
        except Exception as e:
            st.error(f"Reader agent failed: {e}")
            render_pipeline_stepper(1, error=True)
            st.stop()

    # ── Step 2: Writer ──
    st.session_state.step = 2
    render_pipeline_stepper(2)
    st.markdown('<div class="status-bar"><span class="pulse"></span> Writer drafting the report…</div>', unsafe_allow_html=True)

    with st.spinner(""):
        try:
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined,
            })
        except Exception as e:
            st.error(f"Writer chain failed: {e}")
            render_pipeline_stepper(2, error=True)
            st.stop()

    # ── Step 3: Critic ──
    st.session_state.step = 3
    render_pipeline_stepper(3)
    st.markdown('<div class="status-bar"><span class="pulse"></span> Critic reviewing the report…</div>', unsafe_allow_html=True)

    with st.spinner(""):
        try:
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
        except Exception as e:
            st.error(f"Critic chain failed: {e}")
            render_pipeline_stepper(3, error=True)
            st.stop()

    state["elapsed"] = round(time.time() - t_start, 1)
    st.session_state.results = state
    st.session_state.running = False
    st.rerun()

elif run and not topic.strip():
    st.warning("Please enter a research topic first.")


# ── Results display ───────────────────────────────────────────────────────────
if st.session_state.results:
    s = st.session_state.results

    render_pipeline_stepper(4)  # all done

    # Metrics
    word_count = len(s.get("report", "").split())
    src_count = s["search_results"].count("http")
    elapsed = s.get("elapsed", "—")
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box">
            <span class="metric-value">{word_count:,}</span>
            <span class="metric-label">Report Words</span>
        </div>
        <div class="metric-box">
            <span class="metric-value">{src_count}</span>
            <span class="metric-label">Sources Found</span>
        </div>
        <div class="metric-box">
            <span class="metric-value">{elapsed}s</span>
            <span class="metric-label">Total Time</span>
        </div>
        <div class="metric-box">
            <span class="metric-value">4</span>
            <span class="metric-label">Agents Run</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Four result cards ──
    tab_report, tab_feedback, tab_raw = st.tabs(["📋  Final Report", "🧐  Critic Feedback", "🔩  Raw Agent Outputs"])

    with tab_report:
        report_text = s.get("report", "")
        if hasattr(report_text, "content"):
            report_text = report_text.content
        st.markdown(f'<div class="result-card card-writer"><div class="card-header"><div class="card-icon">✍️</div><span class="card-title">Research Report</span><span class="card-badge badge-done">Complete</span></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-body">{report_text}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download Report (.txt)",
            data=report_text,
            file_name=f"research_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

    with tab_feedback:
        feedback_text = s.get("feedback", "")
        if hasattr(feedback_text, "content"):
            feedback_text = feedback_text.content
        st.markdown(f'<div class="result-card card-critic"><div class="card-header"><div class="card-icon">🧐</div><span class="card-title">Critic Assessment</span><span class="card-badge badge-done">Complete</span></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-body">{feedback_text}</div>', unsafe_allow_html=True)

    with tab_raw:
        with st.expander("🔍 Search Agent Output"):
            st.text(s.get("search_results", ""))
        with st.expander("📄 Reader Agent Output"):
            st.text(s.get("scraped_content", ""))

elif not st.session_state.running:
    # Empty state illustration
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0; color: #334155;">
        <div style="font-size: 3.5rem; margin-bottom: 1rem; opacity: 0.25;">⬡</div>
        <p style="font-family: 'DM Mono', monospace; font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; color: #334155;">
            Enter a topic above to start the pipeline
        </p>
    </div>
    """, unsafe_allow_html=True)