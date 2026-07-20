# INSTRACUTION.md

## Purpose
This file explains how to read the **server-side JavaScript project** in this repository and how to debug bugs quickly.

Repository: `Kuldip1211/xrwvm-fullstack_developer_capstone`

---

## What to read first (order)
Read the backend in this order so the flow is easy to understand:

1. `server/database/app.js`  
   - Main Express app  
   - MongoDB connection  
   - API routes  
   - Review insert logic

2. `server/database/review.js`  
   - Mongoose schema for reviews

3. `server/database/dealership.js`  
   - Mongoose schema for dealerships

4. `server/database/Dockerfile`  
   - Runtime environment for backend service

5. Django bridge files (to understand integration):
   - `server/djangoapp/urls.py`
   - `server/djangoapp/views.py` (if present / continue there)
   - `server/djangoproj/settings.py`

6. Frontend entry (for request flow):
   - `server/frontend/src/App.js`

---

## Backend request flow (important)
Most API calls follow this path:

1. Client/Frontend calls endpoint (example: `/fetchReviews`)  
2. Express route in `server/database/app.js` handles request  
3. Mongoose model runs query on MongoDB  
4. Response returned as JSON

For inserts:

1. POST `/insert_review`  
2. raw body parsed using `JSON.parse(req.body)`  
3. new id created from max id + 1  
4. `review.save()` to MongoDB  
5. saved document returned

---

## Current bug-prone points you should check
These are likely error spots from current code:

1. **Unfinished routes in `app.js`**
   - `/fetchDealers`
   - `/fetchDealers/:state`
   - `/fetchDealer/:id`
   These currently contain `//Write your code here` and will break expected functionality.

2. **Error handler uses `res` in top-level try/catch**
   - In startup seed block, catch uses `res.status(...)`, but `res` is not defined outside route handlers.

3. **`JSON.parse(req.body)` risk**
   - `req.body` may already be object/string depending middleware.

4. **No validation before insert**
   - Missing required fields can throw schema validation errors.

5. **Potential empty DB issue when calculating new id**
   - If no documents exist, `documents[0]` can fail.

6. **Mongo container dependency**
   - App expects `mongodb://mongo_db:27017/`.
   - If service/container name differs, DB connection fails.

---

## Quick local debugging checklist
Use this checklist when bug appears:

1. Start services and confirm DB is reachable.  
2. Open backend logs and verify server starts on `3030`.  
3. Test each route using Postman/curl:
   - `GET /`
   - `GET /fetchReviews`
   - `GET /fetchReviews/dealer/:id`
   - `POST /insert_review`
4. For failed request, check:
   - route path
   - request payload format
   - Mongo query
   - stack trace line number
5. Add temporary logs in `app.js`:
   - log `req.params`
   - log `req.body`
   - log query output length
6. Validate schema field types in `review.js`/`dealership.js`.

---

## Suggested logging points
Add logs in these locations:

- after Mongo connection
- before each query
- after query result
- inside each catch block with full error object

Example style:

```js
console.log("[fetchReviews] start");
console.log("[fetchReviews] count:", documents.length);
console.error("[fetchReviews] error:", error);
```

---

## How to read and fix a bug fast (method)
When a bug is reported, follow this method:

1. Reproduce the bug with exact endpoint and payload.
2. Identify failing file and line from log/stack trace.
3. Trace data from request -> route -> model -> DB response.
4. Confirm assumptions (types, null values, required fields).
5. Implement smallest fix possible.
6. Re-test the same failing request.
7. Re-test nearby routes to avoid regressions.

---

## Priority fixes to implement first
1. Complete the 3 unfinished dealer routes in `server/database/app.js`.
2. Replace top-level `res.status` usage with proper startup error logging.
3. Add input validation for `/insert_review`.
4. Guard id generation for empty collection case.

---

## Minimal API reference (from current code)
- `GET /` -> welcome text
- `GET /fetchReviews` -> all reviews
- `GET /fetchReviews/dealer/:id` -> reviews by dealer
- `POST /insert_review` -> insert one review

Dealer APIs are expected but currently incomplete.

---

## Note
This instruction file is intentionally focused on **server JavaScript backend debugging** so contributors can quickly read, understand, and solve bugs.
