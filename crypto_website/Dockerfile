# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
# Install pipenv or any other package manager if you're using it. Otherwise, we will use requirements.txt
COPY requirements.txt /app/
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


# Install the python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8000

# Run the Django app when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
