# Use official Node.js image for build
FROM node:20 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Use official Nginx image for serving static files
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=build /app/build .
EXPOSE 8001

# Replace default nginx config to listen on port 8001
RUN sed -i 's/listen       80;/listen       8001;/g' /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]
