FROM python:3.11-slim

# Create a user
RUN useradd -m ws

# Set working directory
WORKDIR /home/ws

# Install Streamlit
RUN pip install --no-cache-dir streamlit wg-meshconf

# Copy the app
COPY app.py .

# Set ownership
RUN chown ws:ws app.py

# Use non-root user
USER ws

# Expose Streamlit's default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
