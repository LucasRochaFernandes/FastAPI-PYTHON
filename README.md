# FastApi API

FastAPI is a Python web framework designed for fast API development. It stands out for high performance, static typing, and automatic generation of interactive documentation. Leveraging modern concepts like Type Hints and supporting standards like OpenAPI, it simplifies API development efficiently and securely.

## Using Tools like 
  - FastApi
  - Sqlalchemy
  - Pydantic

## How to use

 
After git clone, run:
```bash
docker-compose up -d
```

> **Important->** It is recommended to create a **venv** to install the dependencies

To install the dependencies:

```bash
pip install -r requirements.txt
```

> **Important->** Rename **.env.example** file to **.env**

To run the project:

```bash
uvicorn main:app --reload
```