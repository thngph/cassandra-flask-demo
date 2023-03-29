FROM python:3.9

WORKDIR /app

COPY ./flask/requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", ".flask/app.py"]