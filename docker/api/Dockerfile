FROM python:3.9

RUN pip install --upgrade pip


# RUN adduser -D myuser
# USER myuser
# WORKDIR /home/myuser

WORKDIR /src/fasteyes_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./fasteyes_backend/  /src/fasteyes_backend

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install -r requirements.txt

RUN pip install opencv-python-headless


# COPY ./fasteyes_backend/app/Pipfile ./fasteyes_backend/app/Pipfile.lock /usr/src/fasteyes_backend/

# RUN pipenv install --system --ignore-pipfile --deploy
RUN pytest

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]