FROM kavolorn/opencv
MAINTAINER vic3jo@gmail.com

RUN mkdir -p /app 
WORKDIR /app

COPY ./server ./
COPY ./requirements.txt ./

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN pip3 install -r requirements.txt
RUN export PYTHONIOENCODING=UTF-8

EXPOSE 3005

CMD ["python3", "./server/start.py"]
