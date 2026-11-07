import streamlit as st
import requests

# page configuration
st.set_page_config(
    page_title="FoodTech Copilot",
    page_icon="🍔",
    layout="centered"
)

st.title("🍔 FoodTech Partner Copilot")
st.caption("RAG-powered support assistant for marketplace partners. Powered by Gpt & ChromaDB.")

# session state initialization (memory for chat UI)
if "messages" not in st.session_state:
    st.session_state.messages = []

# render previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input capture
if user_input := st.chat_input("Ask a question about the platform rules... (e.g., repasse financeiro)"):
    
    # display user query in UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # API Request and Response Handling
    with st.chat_message("assistant"):
        try:
            # send payload to your local FastAPI backend
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/ask",
                json={"user_query": user_input}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer")
                source_context = data.get("source_context")
                
                # display LLM answer
                st.markdown(answer)
                
                # display transparent debug/source context in a dropdown
                with st.expander("🔍 View Retrieved Source Context"):
                    st.info(source_context)
                    
                # save assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            elif response.status_code == 404:
                error_msg = "I couldn't find an answer to that in the platform documentation."
                st.warning(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
            else:
                st.error(f"API Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Is the FastAPI backend running on port 8000?")