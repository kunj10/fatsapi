# FastAPI Project

This project demonstrates the development of a backend application using **FastAPI**, a modern, high-performance web framework for building APIs with Python.

## 🚀 Features

* **FastAPI Framework**: Leverages type hints for automatic validation and documentation.
* **RESTful API Endpoints**: Well-structured endpoints for efficient data handling.
* **Async Support**: Asynchronous request handling for better performance.
* **Data Validation**: Automatic request body validation using Pydantic models.
* **Interactive Documentation**: Auto-generated Swagger UI and ReDoc.

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Framework**: FastAPI
* **Data Models**: Pydantic
* **Server**: Uvicorn

## 📂 Project Structure

```
.
├── app.py              # Main FastAPI application
├── models/             # Data models (Pydantic)
├── routes/             # API endpoint definitions
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## ⚙️ Installation & Usage

1. **Clone the Repository**

```bash
git clone https://github.com/kunj10/fatsapi.git
cd fatsapi
```

2. **Create and Activate Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Application**

```bash
uvicorn app:app --reload
```

5. **Access API Docs**

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## 📌 Example Endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.post("/items/")
async def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}
```


---

**👤 Author:** [Kunj Patel](https://www.linkedin.com/in/kunjpatel101/)
