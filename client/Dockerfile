FROM node:current-bullseye AS build

COPY package.json .
COPY package-lock.json .
COPY tsconfig.json .
COPY svelte.config.js .
COPY vite.config.ts .

COPY . .

RUN npm install -g npm@9.8.1
RUN npm i --force
RUN npm run build

ENTRYPOINT ["node", "build"]
EXPOSE 3000

# FROM nginx:1.19-alpine
# COPY --from=build /public /usr/share/nginx/html