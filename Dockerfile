FROM python:3.7
# show the stdout and stderr streams right in the command line instead of getting buffered.
ENV PYTHONUNBUFFERED 1
RUN mkdir /django-kube
WORKDIR /django-kube
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .



EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]