from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/friends")
def get_friends():
    return [
        {"name": "Ramesh", "language": "Telugu"},
        {"name": "Arjun", "language": "Hindi"},
        {"name": "Karthik", "language": "Tamil"}
    ]
