FROM python:3.10-slim

WORKDIR /code 

COPY ./requirements.txt /code
ENV TZ=Time/zone
RUN echo "Time/zone" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN mkdir /code/graphs

COPY . /code

CMD [ "python", "-u", "telegram_bot.py" ]
