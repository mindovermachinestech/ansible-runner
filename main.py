from flask import Flask, request, jsonify
import ansible_runner

app = Flask(__name__)

# API to trigger Ansible playbook
@app.route('/api/upgrade', methods=['POST'])
def upgrade_app():
    print("Invoking API")
    try:
        # Get request parameters
        data = request.json
        app_name = data.get('app_name', 'rule-engine')
        container_name = data.get('container_name', 'rule-engine')
        image_url = data.get('image_url', 'quay.io/mindovermachinestech/rule-engine:0.0.2-SNAPSHOT')
        project_name = data.get('project_name', 'mindovermachinestech-dev')
        oc_token = data.get('oc_token', 'sha256~CpFs208GyQ89xtD6_TNyeduDZrQxowx5Wp7feQ7QniQ')
        oc_server = data.get('oc_server', 'https://api.rm2.thpm.p1.openshiftapps.com:6443')

        # Define extra variables for playbook
        extra_vars = {
            "app_name": app_name,
            "container_name": container_name,
            "image_url": image_url,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }

        # Run Ansible playbook using ansible-runner
        runner = ansible_runner.run(
            private_data_dir="ansible/",
            playbook="tasks/upgrade.yml",
            inventory="ansible/hosts.ini",
            extravars=extra_vars
        )

        # Check playbook status
        if runner.rc == 0:
            return jsonify({"status": "success", "message": "Playbook executed successfully", "output": runner.stdout.read()}), 200
        else:
            return jsonify({"status": "error", "message": "Playbook execution failed", "error": runner.stderr.read()}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# API to trigger Ansible playbook
@app.route('/api/scale', methods=['POST'])
def scale_app():
    print("Invoking Scaling API")
    try:
        # Get request parameters
        data = request.json
        app_name = data.get('app_name', 'rule-engine')
        replicas = data.get('replicas', '1')
        project_name = data.get('project_name', 'mindovermachinestech-dev')
        oc_token = data.get('oc_token', 'sha256~CpFs208GyQ89xtD6_TNyeduDZrQxowx5Wp7feQ7QniQ')
        oc_server = data.get('oc_server', 'https://api.rm2.thpm.p1.openshiftapps.com:6443')

        # Define extra variables for playbook
        extra_vars = {
            "app_name": app_name,
            "replicas": replicas,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }

        # Run Ansible playbook using ansible-runner
        runner = ansible_runner.run(
            private_data_dir="ansible/",
            playbook="tasks/scale.yml",
            inventory="ansible/hosts.ini",
            extravars=extra_vars
        )

        # Check playbook status
        if runner.rc == 0:
            return jsonify({"status": "success", "message": "Playbook executed successfully", "output": runner.stdout.read()}), 200
        else:
            return jsonify({"status": "error", "message": "Playbook execution failed", "error": runner.stderr.read()}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# API to trigger Ansible playbook
@app.route('/api/restart', methods=['POST'])
def restart_app():
    print("Invoking Restart API")
    try:
        # Get request parameters
        data = request.json
        app_name = data.get('app_name', 'rule-engine')
        project_name = data.get('project_name', 'mindovermachinestech-dev')
        oc_token = data.get('oc_token', 'sha256~CpFs208GyQ89xtD6_TNyeduDZrQxowx5Wp7feQ7QniQ')
        oc_server = data.get('oc_server', 'https://api.rm2.thpm.p1.openshiftapps.com:6443')

        # Define extra variables for playbook
        extra_vars = {
            "app_name": app_name,
            "project_name": project_name,
            "oc_token": oc_token,
            "oc_server": oc_server
        }

        # Run Ansible playbook using ansible-runner
        runner = ansible_runner.run(
            private_data_dir="ansible/",
            playbook="tasks/restart.yml",
            inventory="ansible/hosts.ini",
            extravars=extra_vars
        )

        # Check playbook status
        if runner.rc == 0:
            return jsonify({"status": "success", "message": "Playbook executed successfully", "output": runner.stdout.read()}), 200
        else:
            return jsonify({"status": "error", "message": "Playbook execution failed", "error": runner.stderr.read()}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# API to trigger application deployment
@app.route('/api/deploy', methods=['POST'])
def deploy_app():
    print("Invoking Deployment API...")
    try:
        # Get request parameters
        data = request.json
        app_name = data.get('app_name', 'rule-engine')
        container_name = data.get('container_name', 'rule-engine')
        image_url = data.get('image_url', 'quay.io/mindovermachinestech/rule-engine:0.0.2-SNAPSHOT')
        project_name = data.get('project_name', 'mindovermachinestech-dev')
        oc_token = data.get('oc_token', 'sha256~CpFs208GyQ89xtD6_TNyeduDZrQxowx5Wp7feQ7QniQ')
        oc_server = data.get('oc_server', 'https://api.rm2.thpm.p1.openshiftapps.com:6443')
        replicas = data.get('replicas', 1)
        port = data.get('port', 8080)

        # Validate required parameters
        if not oc_token or not oc_server:
            return jsonify({"status": "error", "message": "OpenShift token and server URL are required"}), 400

        # Run Ansible playbook with variables
        result = ansible_runner.run(
            private_data_dir="ansible/",
            playbook='tasks/deploy.yml',
            extravars={
                "app_name": app_name,
                "container_name": container_name,
                "image_url": image_url,
                "project_name": project_name,
                "oc_token": oc_token,
                "oc_server": oc_server,
                "replicas": replicas,
                "port": port,
            }
        )

        # Check playbook result
        if result.rc == 0:
            return jsonify({"status": "success", "message": "Application deployed successfully", "output": result.stdout}), 200
        else:
            return jsonify({"status": "error", "message": "Deployment failed", "error": result.stderr}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# API to trigger application undeployment
@app.route('/api/undeploy', methods=['POST'])
def undeploy_app():
    print("Invoking Undeployment API...")
    try:
        # Get request parameters
        data = request.json
        app_name = data.get('app_name', 'myapp')
        project_name = data.get('project_name', 'myproject')
        oc_token = data.get('oc_token', '')
        oc_server = data.get('oc_server', '')

        # Validate required parameters
        if not oc_token or not oc_server:
            return jsonify({"status": "error", "message": "OpenShift token and server URL are required"}), 400

        # Run Ansible playbook with variables
        result = ansible_runner.run(
            private_data_dir="ansible/",
            playbook='tasks/undeploy.yml',
            extravars={
                "app_name": app_name,
                "project_name": project_name,
                "oc_token": oc_token,
                "oc_server": oc_server,
            }
        )

        # Check playbook result
        if result.rc == 0:
            return jsonify({"status": "success", "message": "Application undeployed successfully", "output": result.stdout}), 200
        else:
            return jsonify({"status": "error", "message": "Undeployment failed", "error": result.stderr}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Run Flask app
if __name__ == '__main__':
    print("Starting Application")
    app.run(host='0.0.0.0', port=5000)
