FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . .
# executa a aplicação dentro do container
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

