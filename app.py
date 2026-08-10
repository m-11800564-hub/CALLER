import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Group Number Caller", page_icon="📢", layout="wide")

st.title("📢 Group Number Caller Panel")

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Controls
st.sidebar.header("⚙️ Calling Controls")

# Group Selection / Custom Typing
group_type = st.sidebar.radio("Group Input Method", ["Preset Groups", "Type Custom Group"])

if group_type == "Preset Groups":
    selected_group = st.sidebar.selectbox("Select Group", ["Group A", "Group B", "Group C", "VIPs", "Table / Counter"])
else:
    selected_group = st.sidebar.text_input("Enter Group Name", value="Group A")

call_number = st.sidebar.number_input("Number to Call", min_value=1, value=1, step=1)
enable_tts = st.sidebar.checkbox("Enable Voice Announcement", value=True)

# Calling Actions
st.sidebar.divider()
if st.sidebar.button("📢 Call Group & Number", type="primary", use_container_width=True):
    call_entry = {"group": selected_group, "number": int(call_number)}
    st.session_state.history.append(call_entry)

if st.sidebar.button("🔄 Reset Queue", use_container_width=True):
    st.session_state.history = []
    st.rerun()

# Main Display Area
col_main, col_hist = st.columns([2, 1])

with col_main:
    st.subheader("📺 Now Serving")
    if st.session_state.history:
        current = st.session_state.history[-1]
        group_text = current["group"]
        num_text = current["number"]
        
        # Display Card
        st.markdown(
            f"""
            <div style="text-align: center; background-color: #1e293b; border: 2px solid #3b82f6; border-radius: 16px; padding: 40px; margin-bottom: 20px;">
                <p style="color: #94a3b8; font-size: 28px; margin: 0; font-weight: 600;">{group_text.upper()}</p>
                <h1 style="color: #38bdf8; font-size: 110px; margin: 10px 0;">#{num_text}</h1>
                <p style="color: #22c55e; font-size: 22px; margin: 0;">Please Proceed Forward</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Text-To-Speech Script
        if enable_tts:
            speech_phrase = f"{group_text}, Number {num_text}"
            components.html(
                f"""
                <script>
                    window.speechSynthesis.cancel();
                    const msg = new SpeechSynthesisUtterance('{speech_phrase}');
                    msg.rate = 0.85;
                    window.speechSynthesis.speak(msg);
                </script>
                """,
                height=0,
                width=0,
            )
    else:
        st.info("No group called yet. Use the sidebar to send a call.")

with col_hist:
    st.subheader("📋 Recent Calls")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            if idx == 0:
                st.success(f"**NOW:** {item['group']} - #{item['number']}")
            else:
                st.write(f"**{item['group']}** - #{item['number']}")
    else:
        st.caption("History will appear here.")
