FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY . /app


RUN pip install --no-cache-dir elasticsearch python-dotenv

CMD ["python", "elastic-backend/cv-index.py"]