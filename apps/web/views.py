import random

from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.web.models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.core.mail import send_mail
from .serializer import ProfileUpdateSerializer
from rest_framework.views import View
from .forms import MovieSearchForm
from .utility import ImdbHandler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status


redirect_checker = 0


@csrf_exempt
def signup_auth(request):
    if request.method == 'POST':
        data = request.POST
        username = data['email']
        password = data['password']
        first_name = data['Fname']
        last_name = data['lname']
        email = username
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   email=email)
        user.save()
        user.set_password(password)
        user.save()
        global redirect_checker
        redirect_checker = 1
        user = authenticate(username=username, password=password)
        request.session['movie_session'] = user.username
        login(request, user)
        return redirect('/web/home/')
    else:
        return redirect('/web/login/')


def load_login_page(request):
    if request.session.get('movie_session'):
        return redirect('/web/home/')
    else:
        err = request.GET.get('err', '')
        message = request.GET.get('message', '')
        print(err)
        if err == "True":
            return render(request, 'index.html',
                          {'message': message, 'block': "block",
                           "success_bit": redirect_checker})
        else:
            global redirect_checker
            if redirect_checker == 1:
                redirect_checker = 0
                return render(request, 'index.html', {
                    'message': "Successfully Registered ,Please login",
                    'block': "block",
                    "success_bit": redirect_checker})
            else:
                return render(request, 'index.html', {"block": "none"})


@csrf_exempt
def login_auth(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=str(data['email']),
                            password=str(data['password']))
        if user is not None and data['user_type'] == 'web':
            login(request, user)
            request.session['movie_session'] = user.username
            return redirect('/web/home/')
        else:
            return redirect('/web/login/?err=True')
    else:
        return redirect('/web/login/')


def logout_view(request):
    username = request.session.get('movie_session')
    if username:
        del request.session['movie_session']
        logout(request)
        return redirect('/web/login/')
    else:
        return redirect('/web/home/')


class LeaderBoardView(View):

    def get(self, request):
        username = request.session.get('movie_session')
        if username:
            user = User.objects.get(username=username)
            users = User.objects.filter(is_superuser=False).order_by('-score')
            c = 1
            user_info_list = list()
            for user in users:
                user_info = dict()
                user_info.update({"first_name": user.first_name})
                user_info.update({"index": c})
                user_info.update({"username": user.username})
                user_info.update({"score": user.score})
                user_info_list.append(user_info)
                c = c + 1
            return render(request, 'leaderboard.html',
                          {"leader_form": user_info_list, "fname": user.first_name})
        else:
            return redirect(('/web/login/'))

    def post(self, request):
        try:
            data = request.POST
            user = User.objects.get(username=data['username'])
            try:
                mapobj = map_userMovie.objects.filter(uobj=user)
                print(mapobj['mobj'])
            except Exception as e:
                pass
            listofmovies = []
            for i in mapobj:
                i = i.mobj
                data = {}
                data.update({"Movies": i.name})
                data.update({"Box_office": i.box_office})
                data.update({"boscore": i.boscore})
                data.update({"rtscore": i.rtscore})
                data.update({"totalscore": i.totalscore})
                listofmovies.append(data)

            return JsonResponse({"status": True, "movies": listofmovies})
        except Exception as e:
            print(e)
            return JsonResponse({"status": False})


def reset_password(request):
    email = request.GET.get('email', '')
    if request.method == 'POST':
        data = request.POST
        obj = otp.objects.get(uobj__username=email, code=data['otp'])
        obj.uobj.password = obj.uobj.set_password(data['password'])
        obj.save()
    return redirect('/web/login/')


class ForgotPassword(View):
    """
    This class deals with opening of forget password page and requesting otp.
    """
    email = None
    user_instance = None
    data = None

    def post(self, request):
        self.data = dict(request.POST.lists())
        self.email = self.data['email'][0]
        self.user_instance = User.get_user_instance(self.email)
        if self.user_instance is None:
            return JsonResponse({"success": "False", "msg": "Invalid Email ID"},
                                status=400)
        else:
            r = random.randint(1111, 9999)
            otpobj = otp.objects.create(uobj=self.user_instance, code=int(r))
            otpobj.save()
            msg = send_mail("Password Recovery mail ",  # mail subject
                            "Please use this code to reset the password for the fantasy account . Here is the code:" + str(
                                r),
                            # mail body
                            'noreply@fantasymovie.com',  # mail from
                            [self.email]  # mail to
                            )
            if msg == 1:
                request.session['forget_pass_session'] = self.email
                return JsonResponse({"success": "true"
                                     },
                                    status=200
                                    )
            else:
                return JsonResponse({"success": False,
                                     "msg": "Please try after some time"
                                     },
                                    status=400)

    def get(self, request):
        try:
            request.session['forget_pass_session']
            return render(request, 'forget_pass.html')

        except Exception as e:
            return redirect(
                ('/web/login/?err=True&message="Invalid Email address"'))


class ResetPassword(View):
    """
    this class is to set new password for the user.
    """
    otp = None
    password = None
    email = None

    def post(self, request):
        self.email = request.session['forget_pass_session']
        self.otp = dict(request.POST.lists())['otp'][0]
        self.password = dict(request.POST.lists())['new_password'][0]
        del request.session['forget_pass_session']
        otp_obj = otp.get_user(email=self.email)
        if otp_obj is None:
            return redirect('/web/login/?err=True&message=Request otp.')
        else:
            if str(otp_obj.code) == str(self.otp):
                user_obj = otp_obj.uobj
                user_obj.set_password(self.password)
                user_obj.save()
                otp_obj.delete()
                return redirect('/web/login/?err=False')
            else:
                otp_obj.delete()
                return redirect('/web/login/?err=True&message=Invalid otp')


class HomeView(View):
    template_name = 'home.html'
    form = MovieSearchForm()

    def get(self, request):
        username = request.session.get('movie_session')
        if username:
            top_posters = list(TopPoster.objects.all())
            if len(top_posters) >= 10:
                top_10 = random.sample(top_posters, 10)
            else:
                top_10 = top_posters
            user = User.get_user_instance(request.session['movie_session'])
            return render(request, self.template_name,
                          {'search_form': self.form, "block": "none",
                           "fname": user.first_name,
                           "posters": top_10})
        return redirect('/web/login/')


class SearchMovie(View):
    template_name = 'home.html'
    form = MovieSearchForm()
    movie_title = ''
    statucpaginator = ''
    paginator = Paginator(list(), 10)

    def post(self, request):
        self.movie_title = request.POST['movie_title']
        movie_list = ImdbHandler.FetchMovieByTitle(self.movie_title)
        self.paginator = Paginator(movie_list, 10)
        request.session['search_title'] = self.movie_title
        movies = self.paginator.page(1)
        return render(request, self.template_name,
                      {'search_form': self.form, 'block': "block",
                       'movies': movies, 'length': len(movies)})

    def get(self, request):
        username = request.session.get('movie_session')
        if not username:
            return redirect('/web/login/')

        self.movie_title = request.session.get('search_title')
        if not self.movie_title:
            return redirect('/web/home/')

        page = request.GET.get('page', 1)
        movie_list = ImdbHandler.FetchMovieByTitle(self.movie_title)
        self.paginator = Paginator(movie_list, 10)
        user = User.get_user_instance(username)
        try:
            movies = self.paginator.page(page)
        except PageNotAnInteger:
            movies = self.paginator.page(1)
        except EmptyPage:
            movies = self.paginator.page(self.paginator.num_pages)
        return render(request, self.template_name,
                      {'search_form': self.form, "fname": user.first_name,
                       'block': "block", 'movies': movies,
                       'length': len(movies)})


class RemoveMovieView(View):
    def post(self, request):
        data = request.POST
        imdbid = data['imdbid']
        email = request.session.gt('movie_session')
        if not email:
            return redirect('/web/login/')

        map_obj = map_userMovie.objects.get(uobj__username=email,
                                           mobj__imdbid=imdbid)
        user = map_obj.uobj
        user.score -= map_obj.mobj.totalscore
        user.score = round(user.score, 1)
        user.save()
        map_obj.delete()
        return JsonResponse({"status": True})


class AddMovieView(View):
    """
    This class deals with adding movies to user.
    """

    def post(self, request):
        data = request.POST
        imdbid = data['imdb_id']
        email = request.session.get('movie_session')
        if not email:
            return redirect('/web/login/')

        map_obj = map_userMovie.objects.filter(
            uobj__username=email).aggregate(num_movies=Count('mobj'))
        does_exist = map_userMovie.objects.filter(
            uobj__username=email,
            mobj__imdbid=imdbid).exists()
        if does_exist:
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            data = {"message": "This movie is already in your colleciton."}
            return JsonResponse(data=data, status=status_code)

        if map_obj['num_movies'] < 6:
            print("movie can be added as num_movies = {}".format(
                map_obj['num_movies']))
            force_save = int(data['force_save'])
            print('Force save: ', force_save)
            if imdbid != '':
                print("Fetching movie info with IMDB id {}...".format(
                    data['imdb_id']))
                movie_data = ImdbHandler.FetchMovieByIMDBID(data['imdb_id'])
                print("...Done!")

                if movie_data['boscore'] == 0 and not force_save:
                    data = {
                        "message": ("Box office score is not available, so"
                                    " it'll be set to 0. Do you still want"
                                    " to continue?")
                    }
                    status_code = status.HTTP_300_MULTIPLE_CHOICES
                    return JsonResponse(
                        data=data,
                        status=status_code
                    )
                if movie_data['rtscore'] == 0 and not force_save:
                    data = {
                        "message": ("Rotten tomatoes rating not available, so it"
                                    "'ll be set to 0. Do you still  want to"
                                    " continue?")
                    }
                    status_code = status.HTTP_300_MULTIPLE_CHOICES
                    return JsonResponse(
                        data=data,
                        status=status_code
                    )
            else:
                movie_data = {'rtscore': 0,
                              "boscore": 0,
                              "box_office": 0,
                              "type": "upcoming"
                     }
            print("The movie info: {}".format(movie_data))
            user = User.objects.get(username=email)
            movie_object = Movies.AddMovie(movie_data)
            map = map_userMovie.objects.create(uobj=user, mobj=movie_object)
            map.save()
            user.score += movie_object.totalscore
            user.score = round(user.score, 1)
            user.save()
            return JsonResponse({"message": "Movie added successfully", "status": True})
        else:
            data = {"message": ("Can't add more than 6 movies, please remove"
                                " some movies before adding new ones.")}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return JsonResponse(data=data, status=status_code)


class ProfileView(View):
    """
    User profile handler class.
    """
    template = 'profile.html'
    form = ProfileUpdateSerializer

    def get(self, request):
        try:
            user_instance = User.objects.get(
                username=request.session['movie_session'])
            return render(request,
                          self.template,
                          {
                              "block": "none",
                              "uobj": user_instance,
                              "fname": user_instance.first_name,
                              "MEDIA_URL": settings.MEDIA_URL
                          }
                          )
        except KeyError:
            return redirect('/web/login/')

    def post(self, request):
        try:
            request_data = request.POST
            user_instance = User.objects.get(
                username=request.session['movie_session'])
            serialized = ProfileUpdateSerializer(data=request_data)
            if serialized.is_valid():
                serialized.update(user_instance, serialized.data)
            else:
                return render(request, self.template)
            try:
                profile_pic = request.FILES['profile']
                user_instance.picture = profile_pic
                user_instance.save()
            except KeyError:
                pass
            return render(request, self.template, {'uobj': user_instance,
                                                   'block': "block",
                                                   "fname": user_instance.first_name,
                                                   'MEDIA_URL': settings.MEDIA_URL
                                                   })
        except Exception as e:
            print(e)
            return redirect('/web/login/')


class MyMoviesView(View):

    template = 'mymovies.html'

    def get(self, request):
        email = request.session['movie_session']
        user = User.objects.get(username=email)
        try:
            mapobj = map_userMovie.objects.filter(uobj=user)
        except Exception as e:
            print(e)
            pass
        # print ("kkkkkkkkkkkkkkkkkkkk")
        listofmovies = []
        for i in mapobj:
            listofmovies.append(i.mobj)
        print(listofmovies)

        return render(request, self.template,
                      {"mymovies_form": listofmovies, "fname": user.first_name})

    def post(self, request):
        data = request.POST
        imdbid = data['imdbid']
        movie = Movies.objects.get(imdbid=imdbid)
        return JsonResponse(data={'movie': movie.name,
                                  'bo': movie.box_office,
                                  'rt_score': movie.rtscore,
                                  'bo_score': movie.boscore,
                                  'total': movie.totalscore
                                  },
                            status=status.HTTP_200_OK)
