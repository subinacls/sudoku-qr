# ─── Builder Stage ────────────────────────────────────────────────────────────
FROM node:18-alpine AS builder
WORKDIR /app

# 1. Copy package.json only (no package-lock.json assumed)
COPY package.json ./

# 2. Install dependencies + autoprefixer so PostCSS can find it
RUN npm install --legacy-peer-deps \
    && npm install --no-save autoprefixer

# 3. Copy entire source, then build
COPY . .
RUN npm run build

# ─── Production Stage ─────────────────────────────────────────────────────────
FROM nginx:stable-alpine

# 4. Remove default static assets and copy in ours
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html

# 5. Expose port (Railway maps $PORT→80 by default) and start Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


