# Pagination Showcase

This project demonstrates g using FastAPI, SQLAlchemy, and Pydantic. It includes offset-based pagination for posts and time-based pagination with lower and upper bounds for comments.

## Features

- **Authors Pagination**: Offset-based pagination.
- **Posts Pagination**: Page-based pagination.
- **Comments Pagination**: Time-based pagination with support for lower and upper bounds.

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/your-username/pagination-showcase.git
    cd pagination-showcase
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies using Poetry**:

    ```sh
    poetry install
    ```

4. **Set up the database**:

    Create a PostgreSQL database and update the `DATABASE_URL` in the `.env` file:

    ```sh
    DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
    ```

5. **Run database migrations**:

    ```sh
    alembic upgrade head
    ```

6. **Run the FastAPI application**:

    ```sh
    uvicorn main:app --reload
    ```

## Endpoints and Usage

### Posts Pagination (Page-Based)

#### Fetch posts with pagination

- **Endpoint**: `/posts/`
- **Method**: GET

**Curl Example**:

```sh
curl -X GET "http://localhost:8000/posts/?page=1&page_size=10" -H "accept: application/json"
```

### Comments Pagination (Time-Based)
#### Fetch comments with pagination
- **Endpoint**: `/comments/`
- **Method**: GET

**Curl Examples**:
- Basic Usage (Default Pagination)

```sh
curl -X GET "http://localhost:8000/comments/" -H "accept: application/json"
```

- Pagination with Limit

```sh
curl -X GET "http://localhost:8000/comments/?limit=5" -H "accept: application/json"
```

- Pagination with Cursor

```sh
curl -X GET "http://localhost:8000/comments/?limit=5&cursor=2024-06-25T00:00:00" -H "accept: application/json"
```

- Pagination with Start Date

```sh
curl -X GET "http://localhost:8000/comments/?limit=5&start_date=2024-06-20T00:00:00" -H "accept: application/json"
```

- Pagination with End Date

```sh
curl -X GET "http://localhost:8000/comments/?limit=5&end_date=2024-06-30T00:00:00" -H "accept: application/json"
```

- Pagination with Start Date and End Date

```sh
curl -X GET "http://localhost:8000/comments/?limit=5&start_date=2024-06-20T00:00:00&end_date=2024-06-30T00:00:00" -H "accept: application/json"
```

- Pagination with Cursor, Start Date, and End Date

```sh
curl -X GET "http://localhost:8000/comments/?limit=5&cursor=2024-06-25T00:00:00&start_date=2024-06-20T00:00:00&end_date=2024-06-30T00:00:00" -H "accept: application/json"
```

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
If you have any questions, feel free to contact me at [jan.nctu@gmail.com].