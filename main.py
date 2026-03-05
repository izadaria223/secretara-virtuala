from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitem acces de la frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pentru test, poți restricționa mai târziu
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mesaj": "Bun venit la secretara AI!"}

@app.post("/recomanda_pachet")
def recomanda_pachet():
    # Aici va veni logica ta
    return {"pachet": "Premium", "pret": "1999 RON"}