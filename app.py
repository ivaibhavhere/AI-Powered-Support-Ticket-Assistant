import streamlit as st
import requests
import json
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Support Ticket AI Assistant", layout="wide")

st.title("🎫 AI-Powered Support Ticket Assistant")
st.markdown("Ask natural language questions about your support tickets or check for anomalies.")

tab1, tab2 = st.tabs(["💬 NL Query", "🚨 Anomaly Detection"])

with tab1:
    st.subheader("Query your Support Data")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question (e.g. 'How many tickets are currently open?')"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Fetch response from FastAPI
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/query", json={"question": prompt})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer received.")
                else:
                    answer = f"Error: {response.text}"
            except Exception as e:
                answer = f"Could not connect to API: {e}"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})

with tab2:
    st.subheader("Detected Anomalies")
    
    if st.button("Run Anomaly Detection"):
        with st.spinner("Analyzing dataset..."):
            try:
                response = requests.get(f"{API_URL}/anomalies")
                if response.status_code == 200:
                    data = response.json()
                    
                    st.markdown("### 🔴 Rule-based Anomalies")
                    st.caption("Unresolved High/Critical tickets older than 24 hours")
                    if data.get("rule_based"):
                        df_rule = pd.DataFrame(data["rule_based"])
                        st.dataframe(df_rule, use_container_width=True)
                    else:
                        st.success("No rule-based anomalies detected.")
                        
                    st.markdown("### 📊 Statistical Anomalies")
                    st.caption("Tickets with abnormally long resolution times (Z-score > 2.5)")
                    if data.get("statistical"):
                        df_stat = pd.DataFrame(data["statistical"])
                        st.dataframe(df_stat, use_container_width=True)
                    else:
                        st.success("No statistical anomalies detected.")
                        
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
