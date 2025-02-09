import streamlit as st
from chatbot import Chatbot

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "urls" not in st.session_state:
        st.session_state.urls = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = Chatbot()

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    st.title("InsightURL Chatbot")
    initialize_session_state()
    with st.sidebar:
        st.header("URL Configuration")
        urls = st.text_area(
            "Enter URLs (one per line)", 
            placeholder="Paste URLs here",
            height=150,
            key="url_input"
        )
        if st.button("Load URLs"):
            url_list = urls.splitlines()
            if not url_list:
                st.error("Please enter at least one URL")
                return

            with st.spinner("Validating and loading URLs..."):
                result = st.session_state.chatbot.get_vectorstore(url_list)
                
                if "error" in result:
                    st.error(result["error"])
                    return
                
                if result.get("invalid_urls"):
                    st.warning(f"The following URLs could not be accessed: \n" + 
                             "\n".join(result["invalid_urls"]))
                
                if result.get("success"):
                    valid_urls = [url for url in url_list if url not in result.get("invalid_urls", [])]
                    if valid_urls:
                        st.session_state.urls = valid_urls
                        st.session_state.messages = [] 
                        st.success(f"Successfully loaded {len(valid_urls)} URLs!")
                    else:
                        st.error("No valid URLs were loaded. Please check your URLs and try again.")

    display_chat_messages()

    if prompt := st.chat_input("What's your question about the content?"):
        if not st.session_state.urls:
            st.error("Please load valid URLs first using the sidebar!")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in st.session_state.chatbot.generate_response(prompt, st.session_state.urls):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()