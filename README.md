# 🚀 FastAPI Mastery - Personal Implementation & Knowledge Repository

> **Author:** RITESH KUMAR SINGH  
> **Batch:** B.Tech Data Science (2027 Batch)  
> **Target Role:** Software Development Engineer (SDE) / Backend Engineer  
> **Repository Link:** [github.com/Riteshkumarsingh1/fastapi](https://github.com/Riteshkumarsingh1/fastapi)

---

## 📖 About This Repository

This repository is my **complete deliverable** built while progressively learning FastAPI through a structured playlist. It is not just a basic "Hello World" app; it is a **living knowledge base** that maps directly to the syllabus outlined below.

**Why does this matter?**  
I believe in learning by doing. For every topic I studied, I either implemented it in code or documented the architecture here. This repository serves as my **interview revision guide** and a **portfolio piece** demonstrating that I can build production-grade, cloud-ready backend systems.

---

## 🎯 Learning Goals (100% Mapped to Course Syllabus)

Here is how I have systematically completed the learning goals outlined in the course:

| Goal | Status | Implementation / Proof |
| :--- | :--- | :--- |
| **FastAPI fundamentals & setup** | ✅ Done | `dynamicRoutes.py` with Uvicorn server setup. |
| **API routing & HTTP methods** | ✅ Done | Implemented `GET` and `POST` routes. |
| **Path & Query parameters** | ✅ Done | `/items?name=xyz&price=100` demo. |
| **Request & Response handling** | ✅ Done | Handled raw dict vs. Pydantic models. |
| **Data validation (Pydantic)** | ✅ Done | `User(BaseModel)` with type validation. |
| **REST API development** | ✅ Done | Basic CRUD ready endpoints. |
| **API Documentation (Swagger)** | ✅ Done | Auto-generated `/docs` endpoint active. |
| **Database integration** | ✅ Done | SQLAlchemy + SQLite architecture documented. |
| **CRUD Operations** | ✅ Done | Explained the 5-step Flow (Transient→Pending→Persistent). |
| **Authentication & AuthZ** | ✅ Done | Implemented JWT + OAuth2 (Password hashing with bcrypt fix). |
| **File handling & uploads** | ✅ Done | `UploadFile` vs `bytes` documented. |
| **Pagination** | ✅ Done | Offset vs Cursor-based pagination strategies documented. |
| **Caching** | ✅ Done | Redis + TTL implementation strategy explained. |
| **API integration (Web Crawling)** | ✅ Done | `httpx` AsyncClient for third-party APIs. |
| **Async Programming** | ✅ Done | Deep dive into Event Loop; `anyio.to_thread` for blocking tasks. |
| **Error Handling** | ✅ Done | Global Exception Handlers + `HTTPException`. |
| **Testing** | ✅ Done | `pytest` + `TestClient` with Dependency Overrides. |
| **Deployment** | ✅ Done | Git workflow + Render/AWS deployment strategy. |

---

## 🛠️ Current Project Implementation (`dynamicRoutes.py`)

My primary learning file demonstrates the basic building blocks of FastAPI. Here is what I have coded:

```python
# 1. Query Parameters
@app.get("/items")
def get_users(name: str = None, price: int = 0):
    return {"Name": name, "Price": price}

# 2. Request Body (Raw Dict)
@app.post("/create user")
def users(user: dict):
    return {"message": "User created", "data": user}

# 3. Request Body (Pydantic Model - Production Standard)
class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/create user")
def users(user: User):
    return {"message": "User created", "data": user}
