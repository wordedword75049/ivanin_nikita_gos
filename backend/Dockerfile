FROM python:3.8

COPY /requirements.txt /backend/
RUN pip3 install -r /backend/requirements.txt --no-cache-dir

COPY / /backend/

#EXPOSE 8080

ENV PYTHONPATH=/:/backend/
COPY /run-container.sh .
ENTRYPOINT [ "./run-container.sh" ]
