FROM node:18-alpine

WORKDIR /usr/src/app

# Копируем описание зависимостей и устанавливаем их
COPY package*.json ./
RUN npm install --only=production

# Копируем исходный код приложения
COPY app.js .

EXPOSE 3000

CMD [ "node", "app.js" ]