# [file name]: main.py
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from utils.agent import ResearchAgent
from utils.audio import text_to_audio
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Research Agent Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .persona-badge {
        background-color: #ff6b6b;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .status-update {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "👋 Hello! I'm your AI Research Assistant. I can help you research companies and generate comprehensive account plans. Please enter your API key in the sidebar to begin!"}]
if "account_plan" not in st.session_state:
    st.session_state.account_plan = "## Account Plan\n\n*No plan generated yet. Start by asking me to research a company!*"
if "agent" not in st.session_state:
    st.session_state.agent = None
if "plan_sections" not in st.session_state:
    st.session_state.plan_sections = {}
if "auto_play_audio" not in st.session_state:
    st.session_state.auto_play_audio = True

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.markdown('<div class="main-header">🔬</div>', unsafe_allow_html=True)
    st.header("⚙️ Configuration")

    # 1. API KEY INPUT
    api_key = st.text_input(
        "🔑 Google Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key to enable the AI agent",
        placeholder="Enter your API key here..."
    )

    if api_key and not st.session_state.agent:
        try:
            with st.spinner("🔄 Initializing AI Agent..."):
                st.session_state.agent = ResearchAgent(api_key)
                st.success("✅ Agent Activated!")
                # Add welcome message
                if len(st.session_state.messages) == 1:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "✅ Agent ready! I can now help you research companies and create account plans. What company would you like to explore?"
                    })
        except Exception as e:
            st.error(f"❌ Invalid API Key: {e}")

    st.markdown("---")

    # 2. PERSONA SELECTOR
    st.subheader("🎭 Agent Persona")
    persona = st.selectbox(
        "Choose Interaction Style:",
        ["Standard Professional", "The Efficient User (Brief)", "The Deep Researcher (Detailed)",
         "The Creative Strategist", "The Clarifying Assistant (Asks Questions)"],
        help="Select how you want the AI to interact with you"
    )

    # Enhanced persona prompts
    persona_prompts = {
        "Standard Professional": "Be professional, balanced, and corporate. Provide comprehensive but concise analysis.",
        "The Efficient User (Brief)": "Be extremely concise. Use bullet points. No fluff. Focus on key insights and speed.",
        "The Deep Researcher (Detailed)": "Be exhaustive and analytical. Dig deep into data. Provide lengthy, nuanced explanations with multiple perspectives.",
        "The Creative Strategist": "Think outside the box. Use metaphors and creative analogies. Suggest bold, unconventional strategies and opportunities.",
        "The Clarifying Assistant (Asks Questions)": "Ask clarifying questions before proceeding. Confirm understanding. Excellent for ambiguous or complex requests."
    }

    if st.session_state.agent:
        st.session_state.agent.update_persona(persona_prompts[persona], persona)
        st.markdown(f'<div class="persona-badge">Active: {persona}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 3. AUDIO SETTINGS
    st.subheader("🔊 Audio Settings")
    st.session_state.auto_play_audio = st.checkbox(
        "Auto-play responses",
        value=True,
        help="Automatically speak AI responses"
    )

    st.markdown("---")

    # 4. LIVE ACCOUNT PLAN VIEW & EDITOR
    st.subheader("📄 Account Plan Builder")

    # Plan sections editor
    if st.session_state.plan_sections:
        st.write("**Edit Plan Sections:**")
        for section, content in st.session_state.plan_sections.items():
            with st.expander(f"✏️ {section}"):
                new_content = st.text_area(
                    f"Content for {section}",
                    value=content,
                    key=f"editor_{section}",
                    height=150
                )
                if new_content != content:
                    st.session_state.plan_sections[section] = new_content
                    st.success(f"✅ {section} updated!")

        # Reconstruct plan from sections
        full_plan = "# Account Plan\n\n"
        for section, content in st.session_state.plan_sections.items():
            full_plan += f"## {section}\n{content}\n\n"
        st.session_state.account_plan = full_plan

    st.markdown("---")
    st.download_button(
        "📥 Download Complete Plan",
        st.session_state.account_plan,
        file_name="account_plan.md",
        mime="text/markdown"
    )

# --- MAIN INTERFACE ---
st.markdown('<div class="main-header">AI Research Agent Pro</div>', unsafe_allow_html=True)
st.caption("🚀 Multimodal Research Assistant • Voice & Text • Live Data • Strategic Planning")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Play audio if available
        if "audio" in msg and msg["audio"]:
            st.audio(msg["audio"], format="audio/mp3")

# --- INPUT AREA (VOICE + TEXT) ---
st.markdown("---")
st.subheader("💬 Start Conversation")

col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    text_input = st.chat_input("💡 Ask me to research a company or update the account plan...")

with col2:
    # Voice input
    voice_text = speech_to_text(
        language='en',
        start_prompt="🎤 Speak",
        stop_prompt="⏹️ Stop",
        just_once=True,
        use_container_width=True,
        key='voice_input'
    )

with col3:
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! How can I help you research companies today?"}
        ]
        st.rerun()

# Determine final input
user_query = None
if text_input:
    user_query = text_input
elif voice_text:
    user_query = voice_text
    # Show voice input confirmation
    st.toast(f"🎤 Voice captured: {voice_text[:50]}...")

# --- PROCESSING LOGIC ---
if user_query:
    if not st.session_state.agent:
        st.error("🔑 Please enter your Google Gemini API Key in the sidebar first!")
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
    else:
        # 1. Append User Message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # 2. Generate Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            status_container = st.empty()

            # Initialize response components
            audio_bytes = None
            response_text = ""
            final_status_updates = []

            with st.status("🤖 AI Agent Working...", expanded=True) as status:
                # Show persona being used
                status.write(f"🎭 Applying **{persona}** persona...")
                time.sleep(0.5)

                try:
                    # Get AI response
                    response_text, status_updates, search_context, plan_updates = st.session_state.agent.get_response(
                        user_query,
                        st.session_state.account_plan
                    )

                    # Display status updates
                    for update in status_updates:
                        status.write(update)
                        time.sleep(0.3)

                    # Update account plan sections if provided
                    if plan_updates:
                        st.session_state.plan_sections.update(plan_updates)
                        status.write("📝 Updating account plan sections...")

                    status.update(label="✅ Response Ready", state="complete", expanded=False)
                    final_status_updates = status_updates

                except Exception as e:
                    response_text = f"❌ I encountered an error: {str(e)}\n\nPlease try again or rephrase your question."
                    status.write("Error in response generation")
                    status.update(label="❌ Error", state="error")
                    final_status_updates = ["Error occurred"]

            # 3. Display Status Updates
            if final_status_updates:
                with status_container:
                    for update in final_status_updates:
                        st.markdown(f'<div class="status-update">{update}</div>', unsafe_allow_html=True)

            # 4. Display Final Response
            message_placeholder.markdown(response_text)

            # In your main.py, replace the audio section with this:

            # 5. Generate and Auto-Play Audio (with debugging)
            if st.session_state.auto_play_audio and response_text:
                try:
                    with st.spinner("🔊 Generating audio..."):
                        # Debug: Check what's being passed to audio
                        print(f"Audio debug - Text length: {len(response_text)}")
                        print(f"Audio debug - First 100 chars: {response_text[:100]}")

                        audio_bytes = text_to_audio(response_text, auto_play=True)

                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                        st.success("✅ Audio ready!")
                        print("✅ Audio generated successfully")
                    else:
                        st.info("🔇 Audio generation skipped")
                        print("❌ Audio bytes are None - checking why...")

                except Exception as e:
                    print(f"❌ Audio generation failed: {e}")
                    st.info("🔇 Audio temporarily unavailable")
                    audio_bytes = None

            # 6. Save to History
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "audio": audio_bytes
            })

            # 7. Update account plan in sidebar if needed
            if plan_updates and st.session_state.plan_sections:
                st.rerun()