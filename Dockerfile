FROM python:3.9

WORKDIR /app

COPY ./flask-server/requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", ".flask-server/app.py"]