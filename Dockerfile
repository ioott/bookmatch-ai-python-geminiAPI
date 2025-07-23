FROM python:3.10-slim
EXPOSE 7860
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
