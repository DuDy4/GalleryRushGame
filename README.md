🖼️ Gallery Rush
Gallery Rush is a simulation-style game. The grid represents a network of art galleries — evolving over time according to predefined logic and user actions.

Built as a Fullstack web app using FastAPI, React (Typescript) & Docker.

You can see deployment here: 'https://gallery-rush-game.vercel.app/'
(might need to wait 15 seconds for backend to warm-up here: 'https://galleryrushgame.onrender.com/')

🛠️ Getting Started
1. Clone the repository
git clone git@github.com:DanShevel/GalleryRushGame.git
cd GalleryRushGame

3. Run docker:
There is a script for bash or powershell.
Bash: ./start.sh
Powershell: .\start.sp1

This should:
I. Run the pytest on the backend.
II. Dockerize the images of the backend & frontend.
III. Run the two images.

🟢 Frontend: http://localhost

🔵 Backend: http://localhost:8000


📦 Project Structure
GalleryRushGame/
├── backend/         # FastAPI app
│   └── tests/       # Unit + E2E tests
├── frontend/        # React + Vite
│   └── src/         # Grid UI and controls
├── docker-compose.yml
└── README.md (You are here :P )


🧪 API Endpoints (visit http://localhost:8000 for swagger)

✍️ Author
Dan Shevel
