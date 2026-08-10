import random
import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(page_title="Number Caller App", page_icon="🔢", layout="centered")

st.title("🔢 Number Caller App")

# Sidebar Configuration
st.sidebar.header("Settings")
min_num = st.sidebar.number_input("Minimum Number", value=1, step=1)
max_num = st.sidebar.number_input("Maximum Number", value=75, step=1)
enable_tts = st.sidebar.checkbox("Enable Voice Announcements", value=True)

# Initialize Session State
if "called_numbers" not in st.session_state:
    st.session_state.called_numbers = []

# Calculations
all_numbers = list(range(int(min_num), int(max_num) + 1))
remaining_numbers = [num for num in all_numbers if num not in st.session_state.called_numbers]

# Main Interface Actions
col1, col2 = st.columns(2)

with col1:
    if st.button("📢 Call Next Number", use_container_width=True, type="primary"):
        if remaining_numbers:
            next_number = random.choice(remaining_numbers)
            st.session_state.called_numbers.append(next_number)
        else:
            st.warning("All numbers in the range have been called!")

with col2:
    if st.button("🔄 Reset / Start Over", use_container_width=True):
        st.session_state.called_numbers = []
        st.rerun()

st.divider()

# Display Current Call
if st.session_state.called_numbers:
    current = st.session_state.called_numbers[-1]
    
    # Large Display Metric
    st.markdown(
        f"""
        <div style="text-align: center; background-color: #1f2937; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
            <p style="color: #9ca3af; font-size: 18px; margin: 0;">CURRENT NUMBER</p>
            <h1 style="color: #3b82f6; font-size: 96px; margin: 0;">{current}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Text-To-Speech Script Execution
    if enable_tts:
        components.html(
            f"""
            <script>
                window.speechSynthesis.cancel();
                const msg = new SpeechSynthesisUtterance('Number {current}');
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
            """,
            height=0,
            width=0,
        )
else:
    st.info("Click **'Call Next Number'** to start calling.")

# Stats Dashboard
st.write("---")
stat1, stat2, stat3 = st.columns(3)
stat1.metric("Total Range", len(all_numbers))
stat2.metric("Called", len(st.session_state.called_numbers))
stat3.metric("Remaining", len(remaining_numbers))

# History Display
st.subheader("📋 Called Numbers History")
if st.session_state.called_numbers:
    # Display recent numbers as badges
    history_rev = list(reversed(st.session_state.called_numbers))
    st.write(" **Latest sequence:** " + ", ".join([f"`{n}`" for n in history_rev]))
else:
    st.caption("No numbers called yet.")
