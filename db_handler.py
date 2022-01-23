from typing import Tuple
from jikanpy import Jikan

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from db_tools import *

engine = create_engine('sqlite:///anime_list.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class AnimeList(Base):
    __tablename__ = "AnimeList"

    id = Column(Integer, primary_key=True)
    anime_code = Column(Integer, unique=True)
    anime_type = Column(String)  # movies|series|ovas|specials
    anime_title = Column(String)  # anime_title
    description = Column(String)  # persian text
    themes = Column(String)  # theme1 theme2 theme3
    genres = Column(String)  # genre1 genre2 genre3
    score = Column(String)  # 8.18
    year = Column(Integer)  # 2000
    en = Column(String)  # {"01": "url", "02": "url"}
    jp = Column(String)  # {"01": "url", "02": "url"}
    de = Column(String)  # {"01": "url", "02": "url"}
    subtitle = Column(String)  # url


def load_all(all: bool = False, base: str = None):
    if all: 
        if base=='series': return [f"sr{anime.anime_code}" for anime in session.query(AnimeList)]
        if base=='movies': return [f"mv{anime.anime_code}" for anime in session.query(AnimeList)]


    animes = session.query(AnimeList).order_by(AnimeList.year).filter(AnimeList.anime_type == base)
    return [anime.anime_code for anime in animes]


def load_preview(anime_code: int) -> Tuple[bytes, str, str]:
    jikan = Jikan()
    anime = jikan.anime(anime_code)

    image_url = anime['image_url']
    title = anime['title']
    episodes = anime['episodes']
    aired = anime['aired']['prop']['from']['year']
    # description = session.query(AnimeList).filter(AnimeList.anime_code == anime_code)[0].description
    description = load_description(AnimeList, session, anime_code)

    title = f"( {aired} ) ( {episodes} Ep ) {title}"

    new_score = str(anime['score'])
    update_score(AnimeList, session, anime_code, new_score)

    return image_url, title, description


if __name__ == '__main__':
    print(load_all(False, 'series'))
    # Base.metadata.create_all(engine)
    # add_anime(
    #     db=AnimeList,
    #     session=session,
    #     anime_code=11757,
    #     anime_type='series',
    #     anime_title='Sword art online S1 (SAO)',
    #     description="\u062f\u0631 \u0633\u0627\u0644 \u06f2\u06f0\u06f2\u06f2\u060c \u06cc\u06a9 \u0628\u0627\u0632\u06cc \u0648\u0627\u0642\u0639\u06cc\u062a \u0645\u062c\u0627\u0632\u06cc \u0628\u0627 \u0646\u0627\u0645 \u0647\u0646\u0631 \u0634\u0645\u0634\u06cc\u0631\u0632\u0646\u06cc \u0622\u0646\u0644\u0627\u06cc\u0646 \u0631\u0648\u0646\u0645\u0627\u06cc\u06cc \u0645\u06cc\u200c\u0634\u0648\u062f \u06a9\u0647 \u0628\u0627\u0632\u06cc\u06a9\u0646\u0627\u0646 \u0622\u0646 \u0628\u0627 \u06af\u0630\u0627\u0634\u062a\u0646 \u06a9\u0644\u0627\u0647\u06cc \u0628\u0631 \u0633\u0631 \u06a9\u0647 \u0628\u0627 \u0639\u0635\u0628\u200c\u0647\u0627\u06cc \u06af\u0631\u062f\u0646 \u0627\u0631\u062a\u0628\u0627\u0637 \u0628\u0631\u0642\u0631\u0627\u0631 \u0645\u06cc\u200c\u06a9\u0646\u062f \u0645\u06cc\u200c\u062a\u0648\u0627\u0646\u0646\u062f \u0628\u0647 \u062f\u0646\u06cc\u0627\u06cc \u0645\u062c\u0627\u0632\u06cc \u0628\u0627\u0632\u06cc \u06a9\u0647 \u0622\u06cc\u0646\u06a9\u0631\u062f \u0646\u0627\u0645\u06cc\u062f\u0647 \u0645\u06cc\u200c\u0634\u0648\u062f \u0645\u0646\u062a\u0642\u0644 \u0634\u0648\u0646\u062f",
    #     themes='Game',
    #     genres='Action Adventure Fantasy Romance',
    #     score='7.20',
    #     year=2012,
    #     de={
    #         "01": "https://xip.li/q7Lmtw",
    #         "02": "https://xip.li/wak7hJ",
    #         "03": "https://xip.li/4tfi58",
    #         "04": "https://xip.li/GOL4cF",
    #         "05": "https://xip.li/adgJlk",
    #         "06": "https://xip.li/MDNqYk",
    #         "07": "https://xip.li/huSK5z",
    #         "08": "https://xip.li/PvWF27",
    #         "09": "https://xip.li/4y7LB3",
    #         "10": "https://xip.li/5DhlZT",
    #         "11": "https://xip.li/SiQ4wu",
    #         "12": "https://xip.li/kCEfOt",
    #         "13": "https://xip.li/RsOZ37",
    #         "14": "https://xip.li/pBVwoO",
    #         "15": "https://xip.li/Fog2AH",
    #         "16": "https://xip.li/RApELf",
    #         "17": "https://xip.li/sTgZtN",
    #         "18": "https://xip.li/OaNgx1",
    #         "19": "https://xip.li/6EJ4QX",
    #         "20": "https://xip.li/mhKRu4",
    #         "21": "https://xip.li/E2R4km",
    #         "22": "https://xip.li/3ATJ71",
    #         "23": "https://xip.li/nLlXOF",
    #         "24": "https://xip.li/2gxwEj",
    #         "25": "https://xip.li/jDFagr"
    #     },
    #     en='',
    #     jp='',
    #     subtitle="https://subs.anidlencodes.xyz/B/Burn%20the%20Witch.rar"
    # )
