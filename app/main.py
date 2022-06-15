from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import orders, products
from app.tags import tags_metadata

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(products.router, prefix='/api')
app.include_router(orders.router, prefix='/api')
add_pagination(app)
