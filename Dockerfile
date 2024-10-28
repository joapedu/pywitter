FROM python:3.11-slim

LABEL João Eduardo Braga <joaoeduardobraga2@gmail.com>

ENV MY_USER="pywitter" \
    MY_GROUP="pywitter" \
    PYTHONUNBUFFERED=1 \
    TZ="America/Fortaleza"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /src

COPY requirements.txt /src/
RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
