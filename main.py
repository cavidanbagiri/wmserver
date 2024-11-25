
from fastapi import FastAPI
from routes import common_router, user_router, warehouse_router, stock_router
from fastapi.middleware.cors import CORSMiddleware

# Import .env
from dotenv import load_dotenv
load_dotenv()

origins = [
    'http://localhost:5173'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common_router.router, prefix='/api/common')
app.include_router(user_router.router,  prefix='/api/users')
app.include_router(warehouse_router.router, prefix='/api/warehouse')
app.include_router(stock_router.router, prefix='/api/stock')


