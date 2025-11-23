# 🌍 GeoEvent Backend API

A high-performance, location-based event management and ticketing API built with **Python**, **FastAPI**, and **MongoDB**.

This project demonstrates advanced NoSQL patterns including **Geospatial Queries**, **Full-Text Search**, **Aggregation Pipelines**, and **ACID Transactions**.

---

## 🚀 Features

- **📍 Geospatial Indexing (`2dsphere`):** Find events within a specific radius using MongoDB's `$near` operator.
- **🔍 Full-Text Search:** Advanced search functionality on event titles with Turkish language support using Text Indexes.
- **📊 Analytics & Reporting:** Aggregation pipelines (`$group`, `$sum`, `$avg`) to calculate category statistics.
- **🏦 ACID Transactions:** Secure ticket purchasing process ensuring data consistency between `Events` and `Tickets` collections (preventing overbooking).
- **⚡ Asynchronous Architecture:** Built on top of **Motor** and **Beanie** for non-blocking I/O operations.
- **🛠 CRUD Operations:** comprehensive management of events and tickets.
- **✅ Data Validation:** Robust schema validation using **Pydantic**.

---

## 🛠 Tech Stack

- **Language:** Python 3.x
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** [MongoDB Atlas](https://www.mongodb.com/atlas) (Cloud)
- **ODM (Object Document Mapper):** [Beanie](https://beanie-odm.dev/)
- **Driver:** [Motor](https://motor.readthedocs.io/) (Async Python Driver for MongoDB)
- **Authentication:** (Planned for future release)

---

## 📂 Project Structure

```bash
geoevent-backend/
├── models/             # Database Schemas (ODM)
│   ├── events.py       # Event model with Embedded Location
│   └── ticket.py       # Ticket model
├── routes/             # API Endpoints (Controllers)
│   ├── events.py       # Event logic (CRUD, Geo, Search, Stats)
│   └── tickets.py      # Ticket logic (Transactions)
├── main.py             # Application Entry Point & DB Connection
├── requirements.txt    # Project Dependencies
└── .env                # Environment Variables (Ignored by Git)
```

---

## ⚡ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/habipokc/geoevent-backend.git
cd geoevent-backend
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory and add your MongoDB connection string:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
DB_NAME=geoevent_db
```

### 5. Run the Application
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## 📖 API Documentation

FastAPI provides automatic interactive documentation. Once the server is running, access:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Key Endpoints

#### 🌍 Geospatial
- `GET /events/nearby/`: List events near a coordinate (Lat/Lon) within a specific radius.

#### 🔎 Search
- `GET /events/search/`: Text search implementation (Case insensitive).

#### 📊 Analytics
- `GET /events/stats/categories`: Returns event counts and average prices per category using MongoDB Aggregation.

#### 🎫 Ticketing (Transactions)
- `POST /tickets/buy`: Atomically creates a ticket and decrements event capacity.

---

## 💡 Learning Outcomes

This project was built to master **MongoDB** patterns in a backend environment:
- Moving from SQL Relational thinking to NoSQL **Document Modeling** (Embedding vs Referencing).
- Implementing **ACID Transactions** in MongoDB using Sessions.
- Utilizing **Indexes** for performance optimization.

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).