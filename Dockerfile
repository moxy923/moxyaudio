FROM ubuntu:18.04

# install deps
RUN apt-get update
RUN apt-get -y install python-all-dev
RUN apt-get -y install python-pip
RUN apt-get -y install portaudio19-dev
RUN python -m pip install pyaudio

CMD /app/run_recorder.sh
