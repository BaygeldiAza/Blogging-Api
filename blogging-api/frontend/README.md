# Blogging Frontend (React + Vite)

This is a ready-to-use frontend for your FastAPI Blogging API.

## 1) Install
```bash
npm install
```

## 2) Configure API base URL
Create a `.env` file in the project root (or copy `.env.example`):
```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 3) Run
```bash
npm run dev
```

Open: http://localhost:5173

## Notes about endpoints
Backends differ slightly between tutorials, so all API paths are centralized in:

- `src/api/endpoints.js`

If one endpoint path is different in your backend, edit it there once.

Default assumptions:
- Register: `POST /users/register` (JSON body)
- Login: `POST /users/login` (OAuth2PasswordRequestForm: `application/x-www-form-urlencoded`)
- Posts: `GET /posts/`, `POST /posts/`, `GET /posts/{id}`
- Comments: `GET /posts/{id}/comments` (fallback to `GET /comments/?post_id={id}`), `POST /comments/`
- Likes (post likes only): `POST /likes/` (body: `{ post_id }`) and `DELETE /likes/{post_id}`
  - If your backend uses different paths (like toggle), update in `src/api/likes.js`.

