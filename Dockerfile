# Use official Python slim image for smaller size
FROM python:3.11-slim

# Set working directory in container
WORKDIR /APL-Ai-Request

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

ENV OPENAI_API_URL=https://api.deepseek.com
ENV OPENAI_API_KEY=sk-31b5d01210e6448f8397b91b8c328c23
ENV KAFKA_TOPIC=cooking-tips-response
ENV KAFKA_RESPONSE_TOPIC=cooking-tips-requests

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port FastAPI will run on
EXPOSE 8001

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
