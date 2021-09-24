FROM python:3.9

RUN pip install --upgrade pip


# RUN adduser -D myuser
# USER myuser
# WORKDIR /home/myuser

WORKDIR /src/fasteyes_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./fasteyes_backend/requirements.txt  /src/fasteyes_backend/requirements.txt 
# COPY ./fasteyes_backend/requirements.txt  /home/myuser

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install -r requirements.txt

RUN pip install opencv-python-headless


# COPY ./fasteyes_backend/app/Pipfile ./fasteyes_backend/app/Pipfile.lock /usr/src/fasteyes_backend/

# RUN pipenv install --system --ignore-pipfile --deploy

COPY ./fasteyes_backend/  /src/fasteyes_backend

# COPY ./fasteyes_backend/app/  /src/fasteyes_backend/app
# COPY ./fasteyes_backend/.env  /src/fasteyes_backend/.env
# COPY ./fasteyes_backend/templates/  /src/fasteyes_backend/templates
# COPY ./fasteyes_backend/templates/  /src/fasteyes_backend/templates
RUN pytest

CMD ["uvicorn", "app.main:app", "--host", "192.168.45.63", "--port", "8000"]