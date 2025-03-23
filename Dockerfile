# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install system dependencies and Ansible runtime
RUN apt-get update && \
    apt-get install -y ansible curl && \
    curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/oc.tar.gz && \
    tar -xvf oc.tar.gz -C /usr/local/bin/ && \
    rm -f oc.tar.gz

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run Flask application
CMD ["python", "main.py"]
