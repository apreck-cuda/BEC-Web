FROM kalilinux/kali-rolling
#FROM python:3.10-slim


RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install kali-linux-headless
RUN apt-get -y install python3 python3-pip build-essential


# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir flask flask-socketio 
RUN pip install --no-cache-dir paramiko 
RUN pip install --no-cache-dir eventlet



WORKDIR /app

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
