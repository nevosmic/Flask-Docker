FROM node:16.13.0-slim

WORKDIR /app

COPY package.json /app/package.json

RUN npm install && npm install -g @angular/cli

COPY . .

EXPOSE 4200

CMD ng serve --host 0.0.0.0
