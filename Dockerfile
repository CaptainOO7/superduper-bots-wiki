FROM node:24.20.0-alpine AS build
WORKDIR /wiki
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN corepack pnpm install --frozen-lockfile
COPY docs docs
RUN corepack pnpm build

FROM nginx:1.28.3-alpine
COPY --from=build /wiki/docs/.vitepress/dist/ /usr/share/nginx/html/
