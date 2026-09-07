# 🚀 FastAPI - Dynamic Routes & Request Handling

A beginner-friendly FastAPI project demonstrating **dynamic routing**, **query parameters**, **request body handling** (dictionaries & Pydantic models), and file uploads. Built for learning and rapid prototyping.

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Setup & Installation](#setup--installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for building APIs.
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server for running FastAPI.
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and settings management using Python type hints.
- **Python 3.10+**

---

## ✨ Features

- **Query Parameters** - Handle optional and required query params (e.g., `/items?name=Apple&price=100`).
- **Request Body (Dict)** - Accept raw JSON dictionaries.
- **Request Body (Pydantic)** - Validate incoming JSON using Pydantic `BaseModel`.
- **Dynamic Routes** - Modular routing structure for scalability.
- **File Uploads** - Ready for static and uploaded file handling (via `uploads/` folder).

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Riteshkumarsingh1/fastapi.git
cd fastapi
