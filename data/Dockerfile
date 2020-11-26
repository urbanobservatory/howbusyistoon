FROM python:3.8-alpine

WORKDIR /usr/src/app

#RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
#RUN apk --no-cache --update-cache add gcc gfortran g++ linux-headers musl-dev build-base wget
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN apk add --update --no-cache py3-numpy
ENV PYTHONPATH=/usr/lib/python3.8/site-packages

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "python", "update.py" ]
