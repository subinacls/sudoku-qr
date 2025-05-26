# ─── Builder Stage ──────────────────────────────────────────────────────────
FROM node:18-alpine AS builder
WORKDIR /app

# Copy manifests & install everything (including devDependencies)
COPY package.json package-lock.json ./
RUN npm ci

# Ensure PostCSS plugins exist
# (only needed if you haven’t already added them to package.json)
RUN npm install --save-dev autoprefixer postcss

# Copy source & build
COPY . .
RUN npm run build

# ─── Production Stage ───────────────────────────────────────────────────────
FROM nginx:stable-alpine
# Remove default site
RUN rm -rf /usr/share/nginx/html/*
# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port (Railway will map $PORT → 80 by default)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
