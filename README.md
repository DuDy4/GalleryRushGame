# 🖼️ Gallery Rush

**Gallery Rush** is a simulation-style game. The grid represents a network of art galleries — evolving over time according to predefined logic and user actions.

Built as a Fullstack web app using **FastAPI**, **React (TypeScript)**, and **Docker**.

📍 **Live deployment**:
- 🟢 Frontend: [https://gallery-rush-game.vercel.app/](https://gallery-rush-game.vercel.app/)
- 🔵 Backend: [https://galleryrushgame.onrender.com/](https://galleryrushgame.onrender.com/) (may take ~15s to wake up)

---

## 🛠️ Getting Started

### 1. Clone the repository

git clone git@github.com:DanShevel/GalleryRushGame.git
cd GalleryRushGame

2. Run Docker:
There is a script for bash or powershell.
Bash: ./start.sh
Powershell: .\start.ps1

This should:
I. Run the pytest on the backend.
II. Dockerize the images of the backend & frontend.
III. Run the two images.

🟢 Frontend: http://localhost

🔵 Backend: http://localhost:8000

3. Without Docker?
Run in separate terminals:

    cd ./backend
    pip i -f requirements.txt
    python ./start_api.py

    &

    cd ./frontend
    npm i
    npm run build
    npm run dev

🟢 Frontend: http://localhost:5173

🔵 Backend: http://localhost:8000

📦 Project Structure
GalleryRushGame/
├── backend/         # FastAPI app
│   └── tests/       # Unit + E2E tests
├── frontend/        # React + Vite
│   └── src/         # Grid UI and controls
├── docker-compose.yml
└── README.md (<- You are here :P )


🧪 API Endpoints (visit http://localhost:8000 for swagger)

✍️ Author
Dan Shevel
