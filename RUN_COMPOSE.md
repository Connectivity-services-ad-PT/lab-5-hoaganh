# RUN_COMPOSE.md — Hướng dẫn chạy Lab 05

## Yêu cầu
- Docker Desktop đang chạy
- Docker Compose v2 (`docker compose version`)

## Bước 1 — Clone repo

```bash
git clone https://github.com/Connectivity-services-ad-PT/lab-5-hoaganh.git
cd lab-5-hoaganh
```

## Bước 2 — Tạo file .env

```bash
cp .env.example .env
# Chỉnh AUTH_TOKEN và POSTGRES_PASSWORD nếu cần
```

## Bước 3 — Chạy toàn bộ stack

```bash
make compose-up
# hoặc
docker compose up -d --build
```

## Bước 4 — Kiểm tra sức khoẻ từng service

```bash
# API
curl http://localhost:8000/health

# AI service
curl http://localhost:9000/health

# DB
docker exec fit4110-db-lab05 pg_isready -U core_user -d core_db
```

## Bước 5 — Dừng stack

```bash
make compose-down
# hoặc
docker compose down
```

## Docker image đã push

```
docker pull hoanganh2k5/core-business:v0.1.0-team-core
```
