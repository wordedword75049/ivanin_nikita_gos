FROM node:14

COPY / /frontend

WORKDIR /frontend

RUN npm install

COPY /run-container.sh .
ENTRYPOINT [ "./run-container.sh" ]