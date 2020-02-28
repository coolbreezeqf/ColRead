FROM python:3.7-alpine

WORKDIR /usr/share/app
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
COPY . .
RUN pip3 install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
