FROM python:3.12
RUN apt-get update && apt-get install -y ffmpeg --no-install-recommends

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# En desarrollo
# CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "80"]

# En producción
CMD ["fastapi", "run", "app/main.py", "--port", "80"]