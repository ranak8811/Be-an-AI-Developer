# 1. Use an official Python base image
FROM python:3.10-slim

# 2. Set the directory inside the container where our code will live
WORKDIR /app

# 3. Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install system dependencies for PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only the requirements first (to use Docker's cache)
COPY requirements.txt .

# 6. Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of your application code
COPY . .

# 8. Tell Docker which port the app runs on
EXPOSE 8000

# 9. The command to start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
