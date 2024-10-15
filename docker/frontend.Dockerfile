FROM python:3.11.7-slim-bookworm

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-tk tk-dev && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY ./app/requirements.txt /usr/local/src/myscripts/requirements.txt 
WORKDIR /usr/local/src/myscripts
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY ./app /usr/local/src/myscripts/app
WORKDIR /usr/local/src/myscripts/app

# Set environment variable for base directory
ENV BASE_DIR="${PYTHONPATH}:/usr/local/src/myscripts/assets/scripts"
ENV RUNNING_IN_DOCKER=true

# Expose port for Streamlit
EXPOSE 80

# Command to run Streamlit
CMD ["streamlit", "run", "AOAI_Chatbot.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]
