from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from platimarket.main import app as platiApp
from steambuy.main import app as steamBuyApp
from steam_account.main import app as steamAccountApp
from funpay.main import app as funPayApp


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(platiApp)
app.include_router(steamBuyApp)
app.include_router(steamAccountApp)
app.include_router(funPayApp)

