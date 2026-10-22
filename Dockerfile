FROM python:3.11-slim
WORKDIR /app
COPY REQUIREMENT.txt .
RUN pip install --no-cache-dir -r REQUIREMENT.txt
COPY API ./API
COPY MODEL ./MODEL
COPY STREAMLIT ./STREAMLIT
EXPOSE 8000
EXPOSE 8501
CMD ["python", "-m", "uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "8000"]