FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY server.py .

# Expose port 8081 (Smithery default)
EXPOSE 8081

# Run the server
CMD ["python", "server.py"]