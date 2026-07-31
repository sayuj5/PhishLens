# BlackFalcon Local Setup Guide

This guide will walk you through the complete process of setting up and running the BlackFalcon Enterprise Vulnerability Management Platform (both Backend and Frontend) on your local machine from scratch.

---

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Git** (for cloning the repository)
- **Python 3.12+** (for the backend)
- **Node.js 20+** (for the frontend)

---

## 2. Clone the Repository

First, clone the repository to your local machine and navigate into the project directory.

```bash
# Clone the repository
git clone https://github.com/sayuj5/PhishLens-.git

# Navigate into the project folder
cd "PhishLens-/BCT Day-6_and_7"
```

> **Note:** If you already have the repository cloned, just navigate to the `BCT Day-6_and_7` folder inside it.

---

## 3. Backend Setup

The backend is built with FastAPI and Python. 

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```
   *You should see `(venv)` appear at the start of your terminal prompt.*

3. **Install the required Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Seed the database (Optional but recommended):**
   This will populate the local SQLite database with initial demo data.
   ```bash
   python seed_demo.py
   ```

5. **Start the API Server:**
   ```bash
   uvicorn main:app --reload
   ```
   *The backend is now running at `http://localhost:8000`.*
   *You can view the interactive API docs at `http://localhost:8000/docs`.*

---

## 4. Frontend Setup

The frontend has been recently migrated from Next.js to **Vite + React + TypeScript**. If you are pulling this repository and have older Next.js caches, follow these steps strictly.

Open a **new terminal window** (leave the backend running in the first one).

1. **Navigate to the frontend directory:**
   ```bash
   # Assuming you are in the root 'BCT Day-6_and_7' folder
   cd frontend
   ```

2. **Clean up old Next.js caches (Crucial Step):**
   If you have previously run this project when it was using Next.js, you **must** delete the old `node_modules` and `.next` folders to prevent conflicts.
   
   **Windows (Command Prompt):**
   ```cmd
   rmdir /s /q node_modules .next
   del package-lock.json
   ```
   **macOS / Linux / Git Bash:**
   ```bash
   rm -rf node_modules .next package-lock.json
   ```

3. **Install the Vite dependencies:**
   ```bash
   npm install --legacy-peer-deps
   ```

4. **Start the Frontend Development Server:**
   ```bash
   npm run dev
   ```
   *The frontend is now running at `http://localhost:3000`.*

---

## 5. Accessing the Platform

1. Open your browser and go to `http://localhost:3000`.
2. You should see the BlackFalcon Login Screen.
3. If you ran the `seed_demo.py` script, you can log in using:
   - **Email:** `admin@blackfalcon.local`
   - **Password:** `Str0ngP@ss!`
4. If you didn't run the seed script, you can create a user via the backend API at `http://localhost:8000/docs` using the `/users/register` endpoint.

---

## Troubleshooting

- **Frontend shows a blank screen or errors about 'next':** You forgot to delete the old `node_modules` folder. Stop the server, delete `node_modules`, run `npm install`, and try again.
- **Backend says 'Address already in use':** Something else is running on port 8000. Find and stop that process, or change the Uvicorn port (`uvicorn main:app --port 8080`).
- **Cannot log in / Network Error:** Ensure the backend terminal is actively running and that `VITE_API_URL` in `frontend/.env` is pointing to `http://localhost:8000`.
