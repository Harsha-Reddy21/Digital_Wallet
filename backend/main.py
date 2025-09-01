from fastapi import FastAPI,HTTPException
import uvicorn
from routers import users,transactions, transactions,wallet
from database import get_db, create_tables



app=FastAPI(
    title="Digital Wallet API",
    description='API for managing digital wallet transactions and user accounts'
)


app.include_router(users.router)
# app.include_router(transactions.router)
app.include_router(wallet.router)

@app.on_event("startup")
async def on_startup():
    # Create database tables
    await create_tables()


if __name__=="__main__":
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)