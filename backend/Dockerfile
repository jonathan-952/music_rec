FROM python:3.11-slim

WORKDIR /code

# Copy dependency file
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY /code ./code

EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "8000"]