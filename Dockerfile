#use python 3.7 image
FROM python:3.7-slim

RUN apt-get update && apt-get install -y netcat && apt-get install dos2unix

#set the working directory
WORKDIR /opt/qualichain_mcdss

#create uploads folder
RUN mkdir -p ./MCDSS/uploads

#install Project requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#copy contents to container automatic-forensic-tool
ADD . .

#start app
RUN dos2unix run.sh
CMD bash run.sh
