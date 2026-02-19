# api/Dockerfile
FROM python:3.11-slim

ARG MODEL_TAG="latest"
LABEL org.opencontainers.image.version=$MODEL_TAG

WORKDIR /app
ENV PYTHONPATH=/app

# Install runtime requirements (adjust path if you keep requirements elsewhere)
COPY api/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY api/src src

# Copy model_repo (must exist in build context before docker build)
# We copy the whole directory to /app/model so the model and VERSION are present
COPY model_repo model

EXPOSE 8000

# Start uvicorn; the app will load the model from /app/model/model.joblib
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]