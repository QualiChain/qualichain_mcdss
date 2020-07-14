#use python 3.7 image
FROM python:3.7-slim

#set the working directory
WORKDIR /opt/qualichain_mcdss
RUN mkdir -p ./MCDSS/uploads

#install Project requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#copy contents to container automatic-forensic-tool
ADD . .

#start app
CMD python MCDSS/app.py
