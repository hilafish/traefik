FROM python:3.7-alpine
WORKDIR ./post_app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8081
COPY . . 
CMD ["python3", "web_server.py"]
