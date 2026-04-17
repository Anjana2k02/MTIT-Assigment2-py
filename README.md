# Restaurant Management System — Microservices

A microservices-based restaurant management backend built with **FastAPI**, **MongoDB Atlas** (Motor + Beanie), and a centralized **API Gateway** with JWT authentication.

---

## Architecture Overview

```
Client
  │
  ▼
API Gateway  :8080  ──► JWT Auth (all routes except /auth/login)
  │
  ├──► Menu Service      :8002   MongoDB › restaurant.menu_items / menus
  ├──► Billing Service   :8003   MongoDB › restaurant.pos_orders / discounts
  ├──► Table Service     :8004   MongoDB › restaurant.tables / locations / table_statuses
  ├──► Store Service     :8005   MongoDB › restaurant.store_items
  ├──► Delivery Service  :8006   MongoDB › restaurant.deliveries
  └──► User Service      :8007   SQLite  › users / roles
```

All inter-service communication passes through the gateway. Each service is independently deployable and exposes a `/health` endpoint.

---

## Services

### API Gateway — `localhost:8080`

Central entry point. Proxies requests to downstream services and enforces JWT Bearer token authentication on all routes except `/auth/login`.

| Method | Path | Proxies to |
|--------|------|------------|
| POST | `/auth/login` | User Service (auth) |
| ANY | `/api/v1/menus/**` | Menu Service |
| ANY | `/api/v1/items/**` | Menu Service |
| ANY | `/api/v1/menu-items/**` | Menu Service |
| ANY | `/api/v1/billing/**` | Billing Service |
| ANY | `/api/v1/tables/**` | Table Service |
| ANY | `/api/v1/store/**` | Store Service |
| ANY | `/api/v1/deliveries/**` | Delivery Service |
| GET | `/health` | Gateway health |

---

### Menu Service — `localhost:8002`

Manages menu items, menus, and the many-to-many link between them.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/items/` | List all items |
| GET | `/api/v1/items/{item_id}` | Get item by ID |
| POST | `/api/v1/items/` | Create item |
| PUT | `/api/v1/items/{item_id}` | Update item |
| DELETE | `/api/v1/items/{item_id}` | Delete item |
| GET | `/api/v1/menus/` | List all menus |
| GET | `/api/v1/menus/{menu_id}` | Get menu by ID |
| POST | `/api/v1/menus/` | Create menu |
| PUT | `/api/v1/menus/{menu_id}` | Update menu |
| DELETE | `/api/v1/menus/{menu_id}` | Delete menu |
| GET | `/api/v1/menu-items/` | List all menu-item links |
| GET | `/api/v1/menu-items/{id}` | Get menu-item link by ID |
| POST | `/api/v1/menu-items/` | Link item to menu |
| PUT | `/api/v1/menu-items/{id}` | Update link |
| DELETE | `/api/v1/menu-items/{id}` | Remove link |
| GET | `/api/v1/menus/{menu_id}/items` | List items in a menu |

---

### Billing Service — `localhost:8003`

POS order management with discount application and itemised bill generation. Fetches live prices from Menu Service.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/pos/` | List all POS orders |
| GET | `/api/v1/pos/delivery` | List delivery-type orders |
| GET | `/api/v1/pos/{order_id}` | Get POS order by ID |
| POST | `/api/v1/pos/` | Create POS order |
| PUT | `/api/v1/pos/{order_id}` | Update POS order |
| DELETE | `/api/v1/pos/{order_id}` | Delete POS order |
| GET | `/api/v1/discounts/` | List all discounts |
| GET | `/api/v1/discounts/{id}` | Get discount by ID |
| POST | `/api/v1/discounts/` | Create discount |
| PUT | `/api/v1/discounts/{id}` | Update discount |
| DELETE | `/api/v1/discounts/{id}` | Delete discount |
| GET | `/api/v1/bill/{order_id}` | Get full bill breakdown |

---

### Table Service — `localhost:8004`

Manages restaurant floor layout — locations, tables, and real-time table status.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/locations/` | List all locations |
| GET | `/api/v1/locations/{id}` | Get location by ID |
| POST | `/api/v1/locations/` | Create location |
| PUT | `/api/v1/locations/{id}` | Update location |
| DELETE | `/api/v1/locations/{id}` | Delete location |
| GET | `/api/v1/locations/{id}/tables` | List tables in a location |
| GET | `/api/v1/tables/` | List all tables |
| GET | `/api/v1/tables/{id}` | Get table by ID |
| POST | `/api/v1/tables/` | Create table |
| PUT | `/api/v1/tables/{id}` | Update table |
| DELETE | `/api/v1/tables/{id}` | Delete table |
| GET | `/api/v1/table-statuses/` | List all table statuses |
| GET | `/api/v1/table-statuses/{id}` | Get table status by ID |
| POST | `/api/v1/table-statuses/` | Set table status |
| PUT | `/api/v1/table-statuses/{id}` | Update table status |
| DELETE | `/api/v1/table-statuses/{id}` | Delete table status |

---

### Store Service — `localhost:8005`

Tracks ingredient and supply inventory — quantities, units, and low-stock thresholds.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/store/` | List all store items |
| GET | `/api/v1/store/{item_id}` | Get store item by ID |
| POST | `/api/v1/store/` | Create store item |
| PUT | `/api/v1/store/{item_id}` | Update store item |
| DELETE | `/api/v1/store/{item_id}` | Delete store item |

---

### Delivery Service — `localhost:8006`

Manages delivery orders — address, status tracking, and assignment.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/deliveries/` | List all deliveries |
| GET | `/api/v1/deliveries/{id}` | Get delivery by ID |
| POST | `/api/v1/deliveries/` | Create delivery |
| PUT | `/api/v1/deliveries/{id}` | Update delivery |
| DELETE | `/api/v1/deliveries/{id}` | Delete delivery |

---

### User Service — `localhost:8007`

User and role management. Uses SQLite + SQLAlchemy (not MongoDB). Authentication tokens are issued via the gateway's `/auth/login` endpoint.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/users/` | List all users |
| GET | `/users/{user_id}` | Get user by ID |
| POST | `/users/` | Create user |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |
| GET | `/roles/` | List all roles |
| GET | `/roles/{role_id}` | Get role by ID |
| POST | `/roles/` | Create role |
| PUT | `/roles/{role_id}` | Update role |
| DELETE | `/roles/{role_id}` | Delete role |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ODM (MongoDB) | Beanie + Motor (async) |
| ORM (SQLite) | SQLAlchemy (User Service) |
| Database | MongoDB Atlas (`restaurant` DB) + SQLite |
| Auth | JWT Bearer tokens (via API Gateway) |
| Runtime | Python 3.14, Uvicorn |

---

## Project Structure

```
.
├── start.py                  # Starts all services concurrently
├── .env.example              # Template for environment variables
│
├── api-gateway/
├── menu-service/
├── billing-service/
├── table-service/
├── store-service/
├── delivery-service/
└── user-service/

# Each service follows this layout:
service-name/
├── app/
│   ├── main.py               # FastAPI app, lifespan, router registration
│   ├── config.py             # Settings (pydantic-settings, reads .env)
│   ├── database.py           # Motor + Beanie init
│   ├── models/               # Beanie Document subclasses
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Business logic / CRUD
│   └── routes/               # FastAPI routers
├── .env                      # Local env (gitignored)
└── requirements.txt
```

---

## Running the Project

### 1. Set up environment variables

Each service directory needs a `.env` file. Use `.env.example` as the template:

```
MONGODB_URL=mongodb+srv://<user>:<password>@mtit.9eco5id.mongodb.net/restaurant?appName=mtit
MONGO_DB_NAME=restaurant
```

### 2. Start all services

```bash
python start.py
```

`start.py` will:
1. Install missing dependencies automatically
2. Start all backend services concurrently
3. Wait for each service to pass its `/health` check
4. Start the API Gateway once all backends are healthy

### 3. Access the docs

| Service | Swagger UI |
|---------|-----------|
| API Gateway | http://localhost:8080/docs |
| Menu Service | http://localhost:8002/docs |
| Billing Service | http://localhost:8003/docs |
| Table Service | http://localhost:8004/docs |
| Store Service | http://localhost:8005/docs |
| Delivery Service | http://localhost:8006/docs |
| User Service | http://localhost:8007/docs |
