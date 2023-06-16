# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the entry point for the container
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]