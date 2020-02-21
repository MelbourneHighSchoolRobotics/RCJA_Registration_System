FROM python:3.7
EXPOSE 8000
ENV PORT=8000
ENV PATH="${PATH}:/app"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY rcjaRegistration /app
WORKDIR /app
CMD ["/bin/sh", "-c", "/app/manage.py runserver 0.0.0.0:${PORT}"]
