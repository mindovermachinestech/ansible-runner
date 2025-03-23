import streamlit as st
import requests

# API base URL
API_URL = "http://localhost:5000/api"
oc_token = "sha256~CpFs208GyQ89xtD6_TNyeduDZrQxowx5Wp7feQ7QniQ"
oc_server = "https://api.rm2.thpm.p1.openshiftapps.com:6443"


# Common Input Fields
def get_common_inputs(prefix):
    app_name = st.text_input("Application Name", "rule-engine", key=f"{prefix}_app_name")
    project_name = st.text_input("Project Name", "mindovermachinestech-dev", key=f"{prefix}_project_name")
    return app_name, project_name


# Upgrade Application
def upgrade_app():
    st.header("Upgrade Application")
    app_name, project_name = get_common_inputs("upgrade")
    container_name = st.text_input("Container Name", "rule-engine", key="upgrade_container_name")
    image_url = st.text_input("Image URL", "quay.io/mindovermachinestech/rule-engine:0.0.2-SNAPSHOT", key="upgrade_image_url")

    if st.button("Upgrade"):
        payload = {
            "app_name": app_name,
            "container_name": container_name,
            "image_url": image_url,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }
        response = requests.post(f"{API_URL}/upgrade", json=payload)
        st.write(response)


# Scale Application
def scale_app():
    st.header("Scale Application")
    app_name, project_name = get_common_inputs("scale")
    replicas = st.number_input("Number of Replicas", min_value=1, value=1, key="scale_replicas")

    if st.button("Scale"):
        payload = {
            "app_name": app_name,
            "replicas": replicas,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }
        response = requests.post(f"{API_URL}/scale", json=payload)
        st.write(response)


# Restart Application
def restart_app():
    st.header("Restart Application")
    app_name, project_name = get_common_inputs("restart")

    if st.button("Restart"):
        payload = {
            "app_name": app_name,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }
        response = requests.post(f"{API_URL}/restart", json=payload)
        st.write(response)


# Deploy Application
def deploy_app():
    st.header("Deploy Application")
    app_name, project_name = get_common_inputs("deploy")
    container_name = st.text_input("Container Name", "rule-engine", key="deploy_container_name")
    image_url = st.text_input("Image URL", "quay.io/mindovermachinestech/rule-engine:0.0.2-SNAPSHOT", key="deploy_image_url")
    replicas = st.number_input("Number of Replicas", min_value=1, value=1, key="deploy_replicas")
    port = st.number_input("Port", min_value=1, value=8080, key="deploy_port")

    if st.button("Deploy"):
        payload = {
            "app_name": app_name,
            "container_name": container_name,
            "image_url": image_url,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server,
            "replicas": replicas,
            "port": port
        }
        response = requests.post(f"{API_URL}/deploy", json=payload)
        st.write(response)


# Undeploy Application
def undeploy_app():
    st.header("Undeploy Application")
    app_name, project_name = get_common_inputs("undeploy")

    if st.button("Undeploy"):
        payload = {
            "app_name": app_name,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }
        response = requests.post(f"{API_URL}/undeploy", json=payload)
        st.write(response)


# Main Application
st.title("OpenShift Application Manager")

# Tabs for different actions
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Deploy", "Scale", "Restart", "Upgrade", "Undeploy"])

with tab1:
    deploy_app()
with tab2:
    scale_app()
with tab3:
    restart_app()
with tab4:
    upgrade_app()
with tab5:
    undeploy_app()
