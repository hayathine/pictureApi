from fastapi import FastAPI

app = FastAPI()

@app.get("/user")
async def get_user():
    pass

@app.post("/user")
async def create_user():
    pass

@app.put("/user")
async def update_user():
    pass

@app.delete("/user")
async def delete_user():
    pass

@app.get("/user/{user_id}")
async def get_user_by_id(user_id: int):
    pass

@app.get("/picture/")
async def get_picture():
    pass

@app.post("/picture/")
async def create_picture():
    pass

@app.get("/picture/{picture_id}")
async def get_picture_by_id(picture_id: int):
    pass

