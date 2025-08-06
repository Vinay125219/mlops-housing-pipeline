# Use the official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Create log directory inside container

#if you want to run models on iris dataset
# RUN mkdir -p irislogs

#if you want to run models on housing dataset
RUN mkdir -p housinglogs

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "api.housing_api:app", "--host", "0.0.0.0", "--port", "8000"]

# for the iris dataset use
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
