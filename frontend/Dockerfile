FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

# Copy application code
COPY . .

EXPOSE 3000

# Development mode with hot reload
CMD ["npm", "run", "dev"]

