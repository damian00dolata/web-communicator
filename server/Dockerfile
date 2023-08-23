# FROM python:3.9
FROM python:3.9.17-bookworm

COPY . .

# RUN apt-get install build-essential libffi-dev python-dev
RUN apt-get update
RUN apt-get install sqlite3
RUN pip install --upgrade pip
RUN pip install 'uvicorn[standard]'
RUN apt-get -y install build-essential cargo
RUN pip install bcrypt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:mainApp.restApi.app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000