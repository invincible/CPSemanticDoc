
FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade -r /app/requirements.txt

# 
COPY ./ /app

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]