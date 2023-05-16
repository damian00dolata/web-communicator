#################################
#   uvicorn main:app --reload   #
#################################

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sockio import sio_app

app = FastAPI()
app.mount('/', app=sio_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)