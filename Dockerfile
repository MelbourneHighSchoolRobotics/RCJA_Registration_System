FROM tiangolo/meinheld-gunicorn:python3.7
ENV PATH="${PATH}:/app"
ENV APP_MODULE="rcjaRegistration.wsgi:application"
ENV PORT=8000

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY app.json /app
COPY rcjaRegistration /app

CMD ["/start.sh"]
ENTRYPOINT ["/entrypoint.sh"]
