FROM python:3.9-alpine
WORKDIR /app
COPY . ./
RUN pip install -r ./requirements/requirements.txt
CMD ["python", "./api/main.py"]
#docker build -t python-imagename .
#sudo docker run -d -p 8080:8080 python-imagename