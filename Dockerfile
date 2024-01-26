# Use the Python 3.11 image as the base
FROM python:3.11

# Set the working directory
WORKDIR /racer

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy all files from the current directory to the working directory
COPY . .

# Expose port 5000
# EXPOSE 5000

# Install Redis
# RUN apt-get update && apt-get install -y sudo lsb-release curl
# RUN chmod +x redis.sh && ./redis.sh
# RUN service redis-server --full-restart

# Run the racer_socket.py file
CMD ["python", "racer_socket.py"]
