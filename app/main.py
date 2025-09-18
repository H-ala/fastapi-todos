from fastapi import FastAPI
from app.routers.todo_router import todo_router
from app.routers.user_router import user_router
from app.routers.auth_router import auth_router
from app.errors.handlers import register_all_errors


version = "v1"
app = FastAPI(
    title='Todos',
    description='A rest API for a todo- list web service',
    version=version,
    # terms_of_service=, # this gets url for the terms of service
    # docs_url=f"/api/{version}/docs",
    # redoc_url=f"/api/{version}/docs",
    contact={"email": "hos.ala81@gmail.com"},
    )

@app.get("/")
def health_check():
    return {"message": "Hello World"}



register_all_errors(app)

app.include_router(todo_router, prefix=f"/api/{version}", tags=["todos"])
app.include_router(user_router, prefix=f"/api/{version}", tags=["users"])
app.include_router(auth_router, prefix=f"/api/{version}", tags=["auth"])











    

