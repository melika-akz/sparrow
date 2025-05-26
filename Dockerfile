# Base image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (if needed)
RUN mkdir -p /app/static

# Default command
CMD ["gunicorn", "sparrow.wsgi:application", "--bind", "0.0.0.0:8000"]
