run:
	sudo docker build -t sber-api-v1 .
	sudo docker run -d -p 8080:8080 sber-api-v1
