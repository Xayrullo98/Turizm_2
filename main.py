from fastapi import FastAPI

from routes import auth,about,users,pictures,hotels,news,texts,gids

from db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shablon",
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'])
app.include_router(
    users.user_router,
    prefix='/user',
    tags=['User section'])
app.include_router(
    about.about_router,
    prefix='/about',
    tags=['About section'])
app.include_router(
    news.news_router,
    prefix='/news',
    tags=['News section'])
app.include_router(
    hotels.hotels_router,
    prefix='/hotels',
    tags=['Hotels section'])

app.include_router(
    gids.gid_router,
    prefix='/gids',
    tags=['Gids section'])
app.include_router(
    texts.text_router,
    prefix='/text',
    tags=['Text section'])
app.include_router(
    pictures.picture_router,
    prefix='/picture',
    tags=['Picture section'])