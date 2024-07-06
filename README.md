
# Expense Tracker API

The API consists of connections to MongoDB and Redis, where the user can register, log in, and verify their data. The login process has a timeout due to JWT authentication. Once logged in, the user can perform CRUD operations.

###Note: You 
## Tech


<div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

</div>

## API Reference

### Login

```http
  POST /login
```
Request Body

{
  "email": "string",
  "password": "string"
}

### Sign Up

```http
  POST /signup
```
Request Body

{
  "email": "string",
  "password": "string"
}

### Me

```http
  GET /me
```
Response

{
  "access_token": "string",
  "token_type": "string"
}

### Get Expenses
```http
  GET /expenses
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `mode` | `string -> past_week, last_month, last_3_months, custom` | Allows filtering by a time period. |
| `category` | `string -> e.g Leisure, Groceries, Clothing, Electronics` | Allows filtering by category |
| `start_date` | `YYYY-mm-dd` | Allows filtering by a custom date, for this mode must be custom, e.g expenses/?mode=custom&start_date=YYYY-mm-ddd |
| `end_date` | `YYYY-mm-dd` | Allows filtering by a custom date, for this mode must be custom, e.g expenses/?mode=custom&end_date=YYYY-mm-ddd |
