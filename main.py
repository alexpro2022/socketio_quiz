import uvicorn

from src.web.app import app

if __name__ == "__main__":
    uvicorn.run(app)
