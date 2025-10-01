import streamlit as st
from ai_researcher_2 import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄")
st.title("📄 Research AI Agent")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# Chat interface
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Log and display user input
    logger.info(f"User input: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Prepare input for the agent
    chat_input = {"messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history}
    logger.info("Starting agent processing...")

    # Placeholder for assistant response
    assistant_msg = st.chat_message("assistant")
    placeholder = assistant_msg.empty()
    full_response = ""

    # Stream agent response
    for s in graph.stream(chat_input, config, stream_mode="values"):
        message = s["messages"][-1]

        # Handle tool calls (log only)
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                logger.info(f"Tool call: {tool_call['name']}")

        # Stream assistant content progressively
        if isinstance(message, AIMessage) and message.content:
            text_content = str(message.content)
            full_response += text_content
            placeholder.markdown(full_response)  # update without overwriting chat history

    # Add final response to history
    if full_response:
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# PDF download button
if st.session_state.pdf_path:
    pdf_file = Path(st.session_state.pdf_path)
    if pdf_file.exists():
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download Research Paper PDF",
                data=f,
                file_name=pdf_file.name,
                mime="application/pdf"
            )
        logger.info("PDF download button displayed")
