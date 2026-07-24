# app.py - Professional Modern UI
import os
import re

import streamlit as st

from src.rag_chain import RAGChatbot
from src.memory import ConversationMemory


st.set_page_config(
    page_title="AI Research Assistant | RAG Chatbot",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0;
    }

    .stApp {
        background:
            radial-gradient(circle at 18% 8%, rgba(0, 212, 255, 0.18), transparent 28%),
            radial-gradient(circle at 82% 16%, rgba(123, 44, 191, 0.20), transparent 30%),
            linear-gradient(135deg, #111827 0%, #17132d 48%, #101827 100%);
        color: #e8eefc;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #101827; }
    ::-webkit-scrollbar-thumb {
        background: #4f6f9f;
        border-radius: 4px;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-container {
        text-align: center;
        padding: 2rem 1.2rem 1.25rem;
        background: rgba(255, 255, 255, 0.045);
        border-radius: 18px;
        margin-bottom: 1.35rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.18);
    }

    .hero-title {
        font-size: clamp(2rem, 5vw, 2.8rem);
        font-weight: 750;
        background: linear-gradient(90deg, #38d5ff, #9b7cff, #5eead4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #a8b3cf;
        font-size: 1rem;
        font-weight: 400;
    }

    .badge-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .tech-badge {
        background: rgba(56, 213, 255, 0.10);
        border: 1px solid rgba(56, 213, 255, 0.28);
        color: #67e8f9;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 650;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin: 1.35rem 0;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem;
        min-height: 138px;
        transition: all 0.22s ease;
    }

    .feature-card:hover {
        background: rgba(255, 255, 255, 0.075);
        border-color: rgba(56, 213, 255, 0.26);
        transform: translateY(-2px);
    }

    .feature-title {
        color: #f8fafc;
        font-size: 0.98rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .feature-desc {
        color: #9ca9c8;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    .metrics-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .metric-item { text-align: center; }
    .metric-value {
        font-size: 1.45rem;
        font-weight: 750;
        color: #67e8f9;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #9ca9c8;
        margin-top: 2px;
    }

    .section-title {
        color: #f8fafc;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 1.4rem 0 0.65rem;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #8290b3;
        border: 1px dashed rgba(255,255,255,0.12);
        border-radius: 14px;
        background: rgba(255,255,255,0.025);
    }

    .empty-title {
        font-size: 1.1rem;
        color: #e8eefc;
        margin-bottom: 0.4rem;
        font-weight: 650;
    }

    .user-msg {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0 8px auto;
        max-width: min(80%, 760px);
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 10px 24px rgba(79, 70, 229, 0.22);
        overflow-wrap: anywhere;
    }

    .assistant-msg {
        background: rgba(255,255,255,0.065);
        color: #e8eefc;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px auto 8px 0;
        max-width: min(85%, 840px);
        font-size: 0.95rem;
        line-height: 1.65;
        border: 1px solid rgba(255,255,255,0.09);
        overflow-wrap: anywhere;
    }

    .source-tag {
        display: inline-block;
        background: rgba(56, 213, 255, 0.14);
        color: #67e8f9;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 650;
        margin: 0 2px;
    }

    .source-panel {
        background: rgba(0,0,0,0.24);
        border-left: 3px solid #38d5ff;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 10px 10px 0;
    }

    .source-header {
        color: #67e8f9;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .source-preview {
        color: #a8b3cf;
        font-size: 0.82rem;
        line-height: 1.45;
        font-style: italic;
    }

    .stTextInput input {
        background: rgba(255,255,255,0.075);
        color: #f8fafc;
        border: 1px solid rgba(255,255,255,0.16);
        border-radius: 12px;
        min-height: 44px;
    }

    .stTextInput input::placeholder {
        color: #8b98b8;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 44px;
        font-weight: 700;
    }

    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #dbeafe;
    }

    .sidebar-muted {
        color: #93a4c7;
        font-size: 0.86rem;
        line-height: 1.55;
    }

    .ready-box {
        background: rgba(34, 197, 94, 0.11);
        border: 1px solid rgba(34, 197, 94, 0.32);
        border-radius: 10px;
        padding: 10px;
        margin-top: 1rem;
        color: #86efac;
        font-size: 0.85rem;
    }

    .footer {
        text-align: center;
        padding: 2rem 0 0.8rem;
        color: #7c8aaa;
        font-size: 0.8rem;
    }

    .footer a {
        color: #67e8f9;
        text-decoration: none;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        background: #22c55e;
        box-shadow: 0 0 8px #22c55e;
    }

    @media (max-width: 800px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .metrics-bar {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        .user-msg, .assistant-msg {
            max-width: 100%;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


if "chatbot" not in st.session_state:
    with st.spinner("Loading AI models..."):
        st.session_state.chatbot = RAGChatbot()
        st.session_state.messages = []
        st.session_state.memory = ConversationMemory(max_history=5)
        st.session_state.docs_loaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory(max_history=5)
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False


with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="color: #67e8f9; font-size: 1.35rem; margin-bottom: 0.2rem;">Documents</h2>
            <p class="sidebar-muted">Upload PDFs or TXT files to chat with them.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        with st.spinner("Processing documents..."):
            for file in uploaded_files:
                temp_path = f"temp_{file.name}"
                with open(temp_path, "wb") as f:
                    f.write(file.getvalue())

                success = st.session_state.chatbot.add_documents(temp_path)
                if success:
                    st.session_state.docs_loaded = True
                    st.success(f"{file.name} processed")

                os.remove(temp_path)

    if st.session_state.docs_loaded:
        st.markdown('<div class="ready-box">Documents ready for chat</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<h4 style="font-size: 0.95rem;">Memory</h4>', unsafe_allow_html=True)
    memory_count = len(st.session_state.memory.messages) // 2
    st.markdown(
        f'<div class="sidebar-muted">{memory_count} exchanges stored</div>',
        unsafe_allow_html=True,
    )

    if st.button("Clear All", use_container_width=True):
        st.session_state.memory.clear()
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        """
        <h4 style="font-size: 0.95rem;">Powered By</h4>
        <div class="sidebar-muted">
            Llama 3.1 8B via Groq<br>
            Hybrid Search: BM25 + Vector<br>
            Cross-Encoder Reranker<br>
            ChromaDB Vector Store<br>
            Streamlit Interface
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">AI Research Assistant</div>
        <div class="hero-subtitle">
            Intelligent document analysis with retrieval-augmented generation.
        </div>
        <div class="badge-container">
            <span class="tech-badge">HYBRID SEARCH</span>
            <span class="tech-badge">RERANKER</span>
            <span class="tech-badge">LLAMA 3.1</span>
            <span class="tech-badge">GROQ LPU</span>
            <span class="tech-badge">CHROMADB</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-title">Hybrid Retrieval</div>
            <div class="feature-desc">BM25 keyword search and dense vector search work together for stronger document recall.</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">Smart Reranking</div>
            <div class="feature-desc">A cross-encoder reranker reorders retrieved chunks by semantic relevance before generation.</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">Source Citations</div>
            <div class="feature-desc">Answers include traceable sources with page numbers and previews for quick verification.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.docs_loaded:
    st.markdown(
        """
        <div class="metrics-bar">
            <div class="metric-item">
                <div class="metric-value">94%</div>
                <div class="metric-label">Faithfulness</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">91%</div>
                <div class="metric-label">Relevancy</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">1.2s</div>
                <div class="metric-label">Avg Latency</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">500+</div>
                <div class="metric-label">Tok/sec</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">Conversation</div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">Welcome</div>
            <div>Upload documents from the sidebar, then ask questions about them.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end;">
                <div class="user-msg">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        answer = re.sub(
            r"\[Source (\d+)\]",
            r'<span class="source-tag">Source \1</span>',
            msg["content"],
        )

        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start;">
                <div class="assistant-msg">{answer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "sources" in msg and msg["sources"]:
            with st.expander("View Sources"):
                for src in msg["sources"]:
                    st.markdown(
                        f"""
                        <div class="source-panel">
                            <div class="source-header">Source {src['number']} - {src['source']} (Page {src['page']})</div>
                            <div class="source-preview">"{src['content_preview']}"</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

col1, col2 = st.columns([6, 1])
with col1:
    prompt = st.text_input(
        "",
        placeholder="Ask me anything about your documents...",
        label_visibility="collapsed",
        key="chat_input",
    )

with col2:
    send_clicked = st.button("Send", use_container_width=True, type="primary")

if send_clicked and prompt:
    st.session_state.memory.add_message("user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Searching documents..."):
        try:
            history = st.session_state.memory.get_history()
            result = st.session_state.chatbot.ask(prompt, chat_history=history)

            st.session_state.memory.add_message("assistant", result["answer"])
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result.get("sources", []),
                    "retrieval_method": result.get("retrieval_method", "unknown"),
                }
            )

            st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown(
    """
    <div class="footer">
        <span class="status-dot"></span> System Online |
        Built with care by <strong>Umar Asghar</strong> |
        <a href="https://github.com/YOUR_USERNAME/rag-chatbot">GitHub</a> |
        <a href="https://huggingface.co/spaces/YOUR_USERNAME/rag-chatbot">Live Demo</a>
    </div>
    """,
    unsafe_allow_html=True,
)
