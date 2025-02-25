FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libffi-dev gcc pkg-config build-essential libssl-dev python3-dev

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install gunicorn directly in the Dockerfile
# RUN pip install gunicorn
RUN pip install daphne

# Copy the rest of your app files
COPY . /app/

# Command to run the app
# CMD ["python", "manage.py", "runserver"]

# Run collectstatic to collect all static files into the STATIC_ROOT
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# Set the default port to 8000
ENV PORT=8000

# Define the DJANGO_SETTINGS_MODULE environment variable
ENV DJANGO_SETTINGS_MODULE=tic_tac_toe.settings

# Expose the port that the app will run on
EXPOSE 8000

# Set the entry point to run Gunicorn with Django's wsgi.py
# CMD ["gunicorn", "tic_tac_toe.wsgi:application", "--bind", "0.0.0.0:$PORT"]

# CMD gunicorn tic_tac_toe.wsgi:application --bind 0.0.0.0:$PORT
CMD daphne tic_tac_toe.asgi:application --bind 0.0.0.0:$PORT

