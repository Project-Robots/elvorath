from fastapi import FastAPI

from elvorath.api.v1 import ca

def create_app() -> FastAPI:
    app = FastAPI(title="Elvorath FastAPI Application for Orbit server")
    
    # Include /api/v1/ca router
    app.include_router(ca.router)

    return app

app = create_app()
