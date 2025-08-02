# Use official Python 3.10 image
FROM python:3.10-slim

# Set work directory inside the container
WORKDIR /app

# Copy the script and config file into the container
COPY autodocgen.py .
COPY default_configuration.json .

# Set default command (overridden if you pass args to docker run)
ENTRYPOINT ["python", "autoDocGen.py"]
