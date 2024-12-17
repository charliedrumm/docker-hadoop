FROM python:3.9-slim

# Use OpenJDK 17 (or fallback to OpenJDK 11 via the correct package name)
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jdk curl && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for PySpark and Java
ENV PYSPARK_PYTHON=python3
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:/usr/lib/jvm/java-17-openjdk-amd64/bin

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app into the container
WORKDIR /app
COPY app.py /app

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
