'''
This file handles all movie calls made to imdb server
@author aquarexpert.com
'''
import locale

from bs4 import BeautifulSoup
from .models import *
import requests, re
import omdb, json
from imdbpie import Imdb
from .models import BOMax
from .constants import API_KEY


class ImdbHandler:
    imdb = Imdb()

    @classmethod
    def FetchMovieByTitle(cls, title):
        try:
            print(title)
            movie_list = cls.imdb.search_for_title(title)
            print('*******************************', movie_list)
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
        try:
            unspacedtitle = "".join(title.split())
            req_obj = requests.get(
                'http://www.boxofficemojo.com/data/js/moviegross.php?id=' + unspacedtitle + '.htm&shortgross=0')
            score = re.search('<b>\$(.+?)<\/b>',
                              req_obj.content.decode('utf-8')).group(1)
            return score
        except Exception as e:
            return '0'

    @classmethod
    def FetchMovieByIMDBID(cls, imdbid):

        res = requests.get(
            'https://omdbapi.com/?apikey={}&i={}&plot=short&r=json'.format(
                API_KEY, imdbid))
        movie_data = res.json()
        movie_dict = dict()
        print('fetched movie data: ', movie_data)
        movie_year = int(movie_data['Year'])
        movie_title = movie_data['Title']

        # maximum box office collection of that year
        max_bo = BOMax.objects.get(year=movie_year).collection

        # box office collection of the movie
        bo_collection = Crawler.get_bo_collection(movie_title, movie_year)
        print('final bo collection: ', bo_collection)

        # box office score on the scale of 10
        bo_score = round(bo_collection * 10.0 / max_bo, 1)
        if bo_score > 10.0:
            bo_score = 10.0

        # rotten tomatoes rating as float on scale of 10
        try:
            rt_score = cls.percent_to_float(
                movie_data['Ratings'][1]['Value']) * 10
        except IndexError:
            rt_score = 0.0

        rt_score = round(rt_score, 1)
        movie_dict.update({'box_office': bo_collection})
        movie_dict.update({'boscore': bo_score})
        movie_dict.update({'Metascore': movie_data['Metascore']})
        movie_dict.update({'rtscore': rt_score})
        movie_dict.update({'title': movie_title})
        movie_dict.update({'year': movie_year})
        movie_dict.update({'imdb_id': movie_data['imdbID']})
        print('returning movie dict: ', movie_dict)
        return movie_dict

    @staticmethod
    def percent_to_float(percent_str):
        """
        Returns the float representation of a percent string.
        e.g. '99.5%' => 0.995
        :param percent_str: str, the string representing value in percentage.
        :return: float, float value of the percent str.
        """
        return float(percent_str.strip().strip('%')) / 100


class Crawler(object):
    """
    This class has methods to crawl websites and get box
    office collections and other information of the movies.
    """

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    @staticmethod
    def save_max_bo_collections():
        """
        Gets collection of the highest grosser of each year from the-number.com
        and saves in the database.
        :return: bool, True if saved collection of all the years successfully
        """
        BOMax.objects.all().delete()
        url = 'http://www.the-numbers.com/movies/#tab=year'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html5lib')
        table_rows = soup.find('div', {'id': 'year'}).find(
            'table').find_all('tr')[1:]
        for table_row in table_rows:
            tds = table_row.find_all('td')
            year = int(tds[0].text)
            bo_collection = locale.atoi(tds[-2].text[1:])
            bo_max = BOMax.objects.create(year=year, collection=bo_collection)
            print(bo_max)
        return True

    @classmethod
    def save_top_posters(cls):
        imdb = Imdb()
        top_250 = imdb.top_250()
        # delete all the posters first
        TopPoster.objects.all().delete()
        for movie in top_250:
            title = movie['title']
            url = movie['image']['url']
            num_votes = movie['num_votes']
            TopPoster.objects.create(
                title=title,
                url=url,
                num_votes=num_votes
            )
            print('Saved poster for ', title)

    @staticmethod
    def get_bo_collection(title, year):
        """
        Searches www.the-numbers.com for the movie title and returns the gross
        collection of the movie found on the website.
        :param title: str, title of the movie
        :param year: int, year of the release of the movie
        :return: int, gross collection of the movie in US dollars
        """
        search_title = '+'.join(title.split(' '))
        url = ('http://www.the-numbers.com/search?searchterm=%s&searchtype'
               '=untilmatchfound')
        res = requests.get(url % search_title)
        soup = BeautifulSoup(res.content, 'html5lib')
        try:
            table = soup.find_all('div',
                                  {'id': 'page_filling_chart'}
                                  )[1].find('table')
            table_rows = table.find_all('tr')
        except AttributeError:
            return 0
        for i in range(1, len(table_rows), 2):
            table_row = table_rows[i]
            tds = table_row.find_all('td')
            try:
                release_year = int(tds[1].text.split('/')[-1])
            except ValueError:
                continue
            if abs(release_year - year) <=2:
                bo_str = tds[-2].text[1:]
                try:
                    bo_collection = locale.atoi(bo_str)
                except ValueError:
                    return 0
                return bo_collection
        try:
            bo_str = table_rows[1].find_all('td')[-2].text[1:]
            bo_collection = locale.atoi(bo_str)
        except (AttributeError, ValueError):
            return 0
        return bo_collection
