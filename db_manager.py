from json import loads, dumps

from os import makedirs
from os.path import exists
from typing import Dict, List

from jikanpy import Jikan

class DBManager:
    def __init__(
        self, 
        base_folder: str = 'db', 
        db_name: str = 'anime_list',
        genre_base: str = "genre_base",
        theme_base: str = "theme_base",
        title_base: str = "title_base",
        year_base: str = "year_base",
        anime_type: str = "anime_type"
        ):

        self._db_name = db_name
        self._genre_base = genre_base
        self._theme_base = theme_base
        self._title_base = title_base
        self._year_base = year_base
        self._anime_type = anime_type

        self._db_path = f"{base_folder if base_folder[-1] == '/' else base_folder + '/'}"

        if not exists(self._db_path): makedirs(self._db_path)
        
        self._create_db(self._db_name)
        self._create_db(self._genre_base)
        self._create_db(self._theme_base)
        self._create_db(self._title_base)
        self._create_db(self._year_base)
        self._create_db(self._anime_type)


    def _create_db(self, db_name: str = None):
        if db_name:
            path = f"{self._db_path}{db_name if db_name[-5:-1]=='.json' else db_name + '.json'}"
            if not exists(path):
                with open(path, 'w') as f: 
                    f.write('{}')

            return 0

        path = f"{self._db_path}{self._db_name if self._db_name[-5:-1] == '.json' else self._db_name + '.json'}" 
        if not exists(path):
            with open(path, 'w') as f: 
                f.write('{}')
        # else:
        #     full_path = "/".join(__file__.replace('\\', '/').split('/')[:-1])
        #     print(f'\n[FILE Exist]: {full_path}/{path}')


    def add_anime(
        self, 
        anime_code: int, 
        anime_type: str, 
        title: str, 
        description: str,
        theme: str, 
        genre: List[str], 
        year: int, 
        rank: int, 
        episode: Dict[str, str],
        subtitle: str
        ):
        
        jikan = Jikan()
        anime = jikan.anime(anime_code)

        # DATA BASE PATH
        path = f"{self._db_path}{self._db_name if self._db_name[-5:-1] == '.json' else self._db_name + '.json'}" 
        if not exists(path):
            DBManager()
            
        with open(f'{path}', 'r') as f: anime_dict = loads(f.read())
        
        rank = anime['rank']

        # add full anime details to self._db_name
        if not str(anime_code) in anime_dict:
            anime_dict[anime_code] = {
                "anime_type": anime_type,
                "title": title,
                "description": description,
                "theme": theme,
                "genre": genre,
                "year": year,
                "rank": rank,
                "episode": episode,
                "subtitle": subtitle
            }

            with open(path, 'w') as f: f.write(dumps(anime_dict, indent=4))

        else:
            print(f'\n[FAILED TO ADD ANIME TO]: {path}')
            print(f"[ANIME EXIST]: {anime_code}")


        # add genre base
        genre_path = f"{self._db_path}{self._genre_base if self._genre_base[-5:-1]=='.json' else self._genre_base + '.json'}"
        with open(genre_path, 'r') as f: genre_dict = loads(f.read())
        for g in genre:

            try: 
                genre_dict[g]
            except KeyError: 
                genre_dict[g] = []

            genre_dict[g].append(anime_code)

        with open(genre_path, 'w') as f: f.write(dumps(genre_dict, indent=4))

        # add theme base
        theme_path = f"{self._db_path}{self._theme_base if self._theme_base[-5:-1]=='.json' else self._theme_base + '.json'}"
        with open(theme_path, 'r') as f: theme_dict = loads(f.read())

        try: 
            theme_dict[theme]
        except KeyError: 
            theme_dict[theme] = []

        theme_dict[theme].append(anime_code)

        with open(theme_path, 'w') as f: f.write(dumps(theme_dict, indent=4))

        # add title base
        title_path = f"{self._db_path}{self._title_base if self._title_base[-5:-1]=='.json' else self._title_base + '.json'}"
        with open(title_path, 'r') as f: title_dict = loads(f.read())
        title_dict[title] = anime_code
        with open(title_path, 'w') as f: f.write(dumps(title_dict, indent=4, sort_keys=True))

        # add year base
        year_path = f"{self._db_path}{self._year_base if self._year_base[-5:-1]=='.json' else self._year_base + '.json'}"
        with open(year_path, 'r') as f: year_dict = loads(f.read())

        try: 
            year_dict[year]
        except KeyError: 
            year_dict[year] = []

        year_dict[year].append(anime_code)

        with open(year_path, 'w') as f: f.write(dumps(year_dict, indent=4))

        # anime_type base
        anime_type_path = f"{self._db_path}{self._anime_type if self._anime_type[-5:-1]=='.json' else self._anime_type + '.json'}"
        with open(anime_type_path, 'r') as f: anime_type_dict = loads(f.read())

        try: 
            anime_type_dict[anime_type]
        except KeyError: 
            anime_type_dict[anime_type] = []

        anime_type_dict[anime_type].append(anime_code)

        with open(anime_type_path, 'w') as f: f.write(dumps(anime_type_dict, indent=4))
        

    def update_anime(self, anime_code, rank: int = None, subtitle: str = None):
        path = f"{self._db_path}{self._db_name if self._db_name[-5:-1] == '.json' else self._db_name + '.json'}"

        with open(path, 'r') as f: anime_dict: dict = loads(f.read())
        print(anime_dict)
        if rank: anime_dict[str(anime_code)]['rank'] = rank
        if subtitle: anime_dict[str(anime_code)]['subtitle'] = subtitle
        
        with open(path, 'w') as f: f.write(dumps(anime_dict, indent=4))
        

    def update_episodes(self, anime_code, ep_lang, new_episodes: dict):
        path = f"{self._db_path}{self._db_name if self._db_name[-5:-1] == '.json' else self._db_name + '.json'}"
        with open(path, 'r') as f: anime_dict: dict = loads(f.read())

        try:
            anime_dict[str(anime_code)]['episode'][ep_lang]
        except KeyError:
            anime_dict[str(anime_code)]['episode'][ep_lang] = {}

        for key in new_episodes:
            print(key, new_episodes[key])
            anime_dict[str(anime_code)]['episode'][ep_lang][f"{key:02d}"] = new_episodes[key]

        with open(path, 'w') as f: f.write(dumps(anime_dict, indent=4))


class helpers:
    def load_preview(db_path, anime_code):
        jikan = Jikan()
        anime = jikan.anime(anime_code)

        image_url = anime['image_url']
        title = anime['title']
        episodes = anime['episodes']
        year = anime['aired']['prop']['from']['year']

        with open(db_path, "r") as f: description = loads(f.read())[str(anime_code)]['description']

        title = f"( {year} ) ( {episodes}Ep ) {title}"

        return image_url, title, description

if __name__=='__main__':
    db = DBManager()
    # db.update_episodes(11757, ep_lang='en', new_episodes={2: "url", 26: "url"})
    