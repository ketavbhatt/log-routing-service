# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the entrypoint command
CMD ["python", "app.py"]
