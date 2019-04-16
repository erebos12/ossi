FROM python:latest
LABEL maintainer "Alexander Sahm <sahm.alexander@pwc.com>"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

env FLASK_APP app.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
