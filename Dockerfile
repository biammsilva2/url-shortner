FROM python:3.9

WORKDIR /code

COPY . /code

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
