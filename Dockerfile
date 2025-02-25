FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libffi-dev gcc pkg-config build-essential libssl-dev python3-dev

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of your app files
COPY . /app/

# Command to run the app
CMD ["python", "manage.py", "runserver"]

