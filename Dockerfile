FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install sudo
RUN pip install -r requirements.txt
CMD /bin/bash
