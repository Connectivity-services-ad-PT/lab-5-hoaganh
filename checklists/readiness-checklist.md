# Readiness Checklist — Lab 05

## Checklist 6 điểm

- [x] **DB sẵn sàng**: `pg_isready` trả OK, container `fit4110-db-lab05` healthy
- [x] **AI service sẵn sàng**: `/health` trả 200, container `fit4110-ai-lab05` healthy
- [x] **API kết nối được DB và AI**: `POST /policy/access-check` trả ALLOW thành công
- [x] **Biến môi trường đúng**: `.env.example` đầy đủ, không commit secret thật
- [x] **Network `team-internal` hoạt động**: các service gọi nội bộ qua tên container
- [x] **Version/tag đúng quy ước**: `v0.1.0-team-core`, push lên Docker Hub

## Ghi chú

| Service | Image | Port | Health |
|---|---|---|---|
| api | fit4110/core-business:lab04 | 8000 | GET /health → 200 |
| ai-service | Dockerfile.ai | 9000 | GET /health → 200 |
| db | postgres:16-alpine | 5432 | pg_isready |

## Sign-off

- Provider: Nhóm A6 — Core Business
- Ngày: 2026-06-10
