# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN apt-get update \
    && apt-get install -y libyaml-dev

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the container
COPY . /app/

# Set the PYTHONPATH environment variable to include the Django project directory
ENV PYTHONPATH=/app

# Expose the port on which the Django development server will run
EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
