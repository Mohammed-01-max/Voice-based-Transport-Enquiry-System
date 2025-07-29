# 🚌 Voice-Based Transport Enquiry System

This project is a **Flask-based web application** that provides transport information such as bus names, timings, fare, type, and stops based on **natural language queries** like:

> "Find bus from Hyderabad to Vijayawada"

---

## 🚀 Features

- 🔎 Search buses by voice/text query
- 🧠 Regex-based query parsing
- 🗄️ Backend powered by **MySQL**
- 🖥️ User interface via `index.html` (to be created/added)
- 🔐 Secure DB connection handling and error messages

---

## 🧠 How It Works

- The app listens to POST `/search` requests with a query like:
```json
{ "query": "Find bus from Hyderabad to Vijayawada" }
