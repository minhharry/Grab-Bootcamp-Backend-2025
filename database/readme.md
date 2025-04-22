### B1 Tạo file .env
tạo file .env như sau:
```sh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
POSTGRES_DB=restaurants
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

### B2 Khởi động postgres
```sh
docker compose up db
```

### B3 Khởi động cái client để xem dữ liệu trong database cho nhanh
```sh
docker compose up adminer
```
### B4 Nạp data từ jsonl vào database
```sh
docker compose up app
```

### B5
vô http://localhost:8080/ để xem dữ liệu

Để xóa hết mọi thứ để chạy lại: 
```sh
docker compose down -v
```
Để chạy lại: 
```sh
docker compose up --build
```

