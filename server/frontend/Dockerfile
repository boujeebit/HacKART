FROM node:14 as builder
WORKDIR '/app'
COPY . .
RUN yarn install
RUN yarn build

FROM nginx:latest
COPY ./config/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist/ /usr/share/nginx/html