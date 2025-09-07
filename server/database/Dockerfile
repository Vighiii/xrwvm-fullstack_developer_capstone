FROM node:18.12.1-bullseye-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN npm install -g npm@9.1.3

# Copy package.json first for better caching
COPY package.json ./

# Install dependencies
RUN npm install --production

# Copy application code
COPY . .

EXPOSE 3030

CMD [ "node", "app.js" ]
