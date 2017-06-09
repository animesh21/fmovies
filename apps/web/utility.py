'''
This file handles all movie calls made to imdb server
@author aquarexpert.com
'''
from .models import *
import requests, re
import omdb, json
from imdbpie import Imdb


class ImdbHandler:
    imdb = Imdb()

    @classmethod
    def FetchMovieByTitle(cls, title):
        try:
            print(title)
            movie_list = cls.imdb.search_for_title(title)
            # print('*******************************',movie_list)
            upcominglist = Upcoming_movies.getlist(title=title)
            if movie_list is None:
                return upcominglist
            else:
                # print(movie_list)
                movie_list += upcominglist
                return movie_list
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def fetch_boxoffice(title):
        print("inside fetch_boxoffice")
        try:
            unspacedtitle = "".join(title.split())
            print('just before hitting the api for unspaced title {}'.format(unspacedtitle))
            req_obj = requests.get(
                'http://www.boxofficemojo.com/data/js/moviegross.php?id=' + unspacedtitle + '.htm&shortgross=0')
            print('printing from fetch_boxoffice: ', req_obj.content)
            score = re.search('<b>\$(.+?)<\/b>',
                              req_obj.content.decode('utf-8')).group(1)
            return score
        except Exception as e:
            return 0

    @classmethod
    def FetchMovieByIMDBID(cls, imdbid):

        api_key = '9950c17c'
        fmobj = requests.get(
            'https://omdbapi.com/?apikey={}&i={}&plot=short&r=json'.format(
                api_key, imdbid))
        movie_list = json.loads(fmobj.content.decode('utf-8'))
        movie_dict = {}
        boxoffice_collection = cls.fetch_boxoffice(title=movie_list['Title'])
        movie_dict.update({'box_office': boxoffice_collection})
        movie_dict.update({'boscore': movie_list['imdbRating']})
        movie_dict.update({'Metascore': movie_list['Metascore']})
        movie_dict.update({'rtscore': movie_list['Metascore']})
        movie_dict.update({'title': movie_list['Title']})
        movie_dict.update({'year': movie_list['Year']})
        movie_dict.update({'imdb_id': movie_list['imdbID']})
        print('returning movie dict: ', movie_dict)
        return movie_dict
