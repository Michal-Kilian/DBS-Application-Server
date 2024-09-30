from fastapi import FastAPI
from dbs_assignment.router import router
import dbs_assignment.db_setup


app = FastAPI(title="DBS")
app.include_router(router)
