FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Cloud Run automatically sets the PORT environment variable, we default to 8080 if not set.
ENV PORT 8080

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port
EXPOSE $PORT

# Start FastAPI server
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
