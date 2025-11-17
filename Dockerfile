# ================================
# 1. Base image
# ================================
FROM python:3.11-slim

# ================================
# 2. Prevent Python buffering
# ================================
ENV PYTHONUNBUFFERED=1

# ================================
# 3. Create app directory
# ================================
WORKDIR /app

# ================================
# 4. Install system dependencies
# ================================
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ================================
# 5. Copy project
# ================================
COPY . /app

# ================================
# 6. Install dependencies
# ================================
RUN pip install --no-cache-dir -r requirements.txt

# ================================
# 7. Streamlit config (production mode)
# ================================
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_SERVER_HEADLESS=true

# ================================
# 8. Expose port
# ================================
EXPOSE 8080

# ================================
# 9. Run Streamlit
# ================================
CMD ["streamlit", "run", "app/web_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
