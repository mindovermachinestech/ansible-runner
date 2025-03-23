import streamlit as st
import requests

# API base URL
API_URL = "http://localhost:5000/api"
oc_token = "sha256~CpFs208GyQ89xtD6_TNyeduDZrQxowx5Wp7feQ7QniQ"
oc_server = "https://api.rm2.thpm.p1.openshiftapps.com:6443"

# Chatbot Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {"intent": None, "data": {}}


# Function to detect user intent based on input
def detect_intent(user_input):
    user_input = user_input.lower()
    if "deploy" in user_input:
        return "deploy"
    elif "scale" in user_input or "scale up" in user_input or "scale down" in user_input:
        return "scale"
    elif "restart" in user_input:
        return "restart"
    elif "upgrade" in user_input:
        return "upgrade"
    elif "undeploy" in user_input or "remove" in user_input:
        return "undeploy"
    else:
        return "unknown"


# Function to handle API requests based on intent
def handle_api_request(intent, data):
    url = f"{API_URL}/{intent}"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return f"✅ Successfully performed {intent} action!"
    else:
        return f"❌ Failed to perform {intent}. Error: {response.text}"


# Main chatbot logic
# Main chatbot logic
def chatbot():
    st.header("🤖 OpenShift Chatbot")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    user_input = st.chat_input("Ask me something...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        conversation_state = st.session_state.conversation_state
        intent = conversation_state["intent"]

        # Check if intent is already detected
        if not intent:
            intent = detect_intent(user_input)
            conversation_state["intent"] = intent

            if intent == "unknown":
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": "❓ I didn't understand that. Please specify if you want to deploy, scale, restart, upgrade, or undeploy."}
                )
            else:
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"👍 Got it! You want to {intent} an application. Let's get some details."}
                )

        # If intent is valid, start gathering data
        if intent in ["deploy", "scale", "restart", "upgrade", "undeploy"]:
            data = conversation_state["data"]

            # Collect app_name
            if "app_name" not in data:
                data["app_name"] = user_input
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": "✅ Application name saved. What's the project name?"}
                )
            elif "project_name" not in data:
                data["project_name"] = user_input
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": "✅ Project name saved."}
                )

            # Handle intent-specific fields
            elif intent == "scale" and "replicas" not in data:
                try:
                    data["replicas"] = int(user_input)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": "✅ Number of replicas saved. Scaling now..."}
                    )
                except ValueError:
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": "❗ Please provide a valid number of replicas."}
                    )

            elif intent == "deploy":
                if "container_name" not in data:
                    data["container_name"] = user_input
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": "✅ Container name saved. What's the image URL?"}
                    )
                elif "image_url" not in data:
                    data["image_url"] = user_input
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": "✅ Image URL saved. How many replicas should be deployed?"}
                    )
                elif "replicas" not in data:
                    try:
                        data["replicas"] = int(user_input)
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": "✅ Number of replicas saved. Which port should be exposed?"}
                        )
                    except ValueError:
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": "❗ Please provide a valid number for replicas."}
                        )
                elif "port" not in data:
                    try:
                        data["port"] = int(user_input)
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": "✅ Port saved. Deploying now..."}
                        )
                    except ValueError:
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": "❗ Please provide a valid port number."}
                        )

            # For restart, upgrade, and undeploy — no extra details needed after project_name
            if intent in ["restart", "upgrade", "undeploy"] and "app_name" in data and "project_name" in data:
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"✅ All required details collected for {intent}. Performing the task now..."}
                )

            # Check if all required data is collected
            if intent == "deploy" and {"app_name", "project_name", "container_name", "image_url", "replicas", "port"}.issubset(
                data.keys()
            ):
                result = handle_api_request(intent, data)
                st.session_state.chat_history.append({"role": "assistant", "content": result})
                st.session_state.conversation_state = {"intent": None, "data": {}}

            elif intent == "scale" and {"app_name", "project_name", "replicas"}.issubset(data.keys()):
                result = handle_api_request(intent, data)
                st.session_state.chat_history.append({"role": "assistant", "content": result})
                st.session_state.conversation_state = {"intent": None, "data": {}}

            elif intent in ["restart", "upgrade", "undeploy"] and {"app_name", "project_name"}.issubset(data.keys()):
                result = handle_api_request(intent, data)
                st.session_state.chat_history.append({"role": "assistant", "content": result})
                st.session_state.conversation_state = {"intent": None, "data": {}}

        st.rerun()

# Run chatbot
chatbot()
