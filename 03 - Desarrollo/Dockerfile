FROM node:22-alpine AS frontend
WORKDIR /web
RUN npm install -g pnpm@10
COPY package.json pnpm-lock.yaml ./
COPY index.html vite.config.js ./
COPY src ./src
COPY public ./public
ENV VITE_API_URL=
RUN pnpm install --frozen-lockfile && pnpm build

FROM python:3.12-slim
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    STATIC_DIR=/app/static
WORKDIR $HOME/app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt
COPY backend/app ./app
COPY --from=frontend --chown=user /web/dist ./static
EXPOSE 7860
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
