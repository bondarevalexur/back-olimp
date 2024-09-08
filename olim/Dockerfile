# Use an official Python runtime as a parent image
FROM python:3.9


# Add the current directory files (on your machine) to the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port server is running on
EXPOSE 8000

# Start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "olim.wsgi:application"]