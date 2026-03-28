# -------------------------------
# BASE IMAGE
# -------------------------------
FROM python:3.10-slim

# -------------------------------
# WORKDIR
# -------------------------------
WORKDIR /app

# -------------------------------
# INSTALL SYSTEM DEPENDENCIES
# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# COPY FILES
# -------------------------------
COPY . .

# -------------------------------
# INSTALL PYTHON DEPENDENCIES
# -------------------------------
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# ENV
# -------------------------------
ENV PORT=10000

# -------------------------------
# EXPOSE
# -------------------------------
EXPOSE 10000

# -------------------------------
# RUN APP (IMPORTANT 🔥)
# -------------------------------
CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT"]