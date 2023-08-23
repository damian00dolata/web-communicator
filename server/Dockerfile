FROM python:3.9

COPY ./requirements.txt requirements.txt

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:mainApp.restApi.app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
