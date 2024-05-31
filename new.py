import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GAKey"))
model_text = genai.GenerativeModel("gemini-pro")

past_prompts = {}


def get_gemini_response(prompt):
    if prompt not in past_prompts:
        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            past_prompts[prompt] = "".join([chunk.text for chunk in response])
            return past_prompts[prompt]
        except Exception as e:
            return f"Error during Text Chat: {str(e)}"
    else:
        return past_prompts[prompt]


def display_chat_history(chat_history):
    previous_role = None
    for message in chat_history:
        role = message["role"]
        content = message["content"]
        if role != previous_role:
            with st.chat_message(role):
                st.markdown(content)
        previous_role = role


def main():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "old_chat_history" not in st.session_state:
        st.session_state.old_chat_history = []

    st.sidebar.title("Settings")
    css="""
            <style>
                .st-emotion-cache-1629p8f h1 {
                    scroll-margin-top: 2rem;
                    margin-top: -10%;
                }
            </style>
            """
    st.markdown(css,unsafe_allow_html=True)
    temperature_value = st.sidebar.slider(
        "Temperature", min_value=0.0, max_value=1.0, step=0.1, value=0.30
    )
    top_p_value = st.sidebar.slider("Top-p", min_value=0.0, max_value=1.0, step=0.1, value=0.53)
    top_k_value = st.sidebar.number_input("Top-k", min_value=1, value=20)
    if top_k_value < 1:
        st.warning("Top-k must be a positive integer greater than or equal to 1. Setting to default (40).")
        top_k_value = 40

    st.title("Chat Bot Using GEMINI_PRO.")

    if st.button("New Session") and st.session_state.chat_history:
        if "old_chat_history" not in st.session_state:
            st.session_state.old_chat_history = []
        session_id = len(st.session_state.old_chat_history) + 1
        st.session_state.old_chat_history.append({f"Old Session {session_id}": st.session_state.chat_history})

        st.session_state.chat_history = []
        
        past_prompts.clear()
    css="""
            <style>
                .st-emotion-cache-7ym5gk {
                    display: inline-flex;
                    -webkit-box-align: center;
                    align-items: center;
                    -webkit-box-pack: center;
                    justify-content: center;
                    font-weight: 400;
                    padding: 0.25rem 0.75rem;
                    border-radius: 0.5rem;
                    min-height: 38.4px;
                    margin: 0px;
                    line-height: 1.6;
                    color: inherit;
                    width: auto;
                    user-select: none;
                    background-color: rgb(255, 255, 255);
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    margin-left: 80%;
                }
            </style>
            """
    st.markdown(css,unsafe_allow_html=True)
    
    if "old_chat_history" in st.session_state:
        for idx, session in enumerate(st.session_state.old_chat_history):
            session_key = f"Old Session {idx+1}"
            if st.sidebar.button(session_key):
                st.session_state.chat_history = session[session_key]


    if prompt := st.chat_input("Enter a prompt here"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        response = get_gemini_response(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    if st.session_state.chat_history:
        display_chat_history(st.session_state.chat_history)


if __name__ == "__main__":
    main()
