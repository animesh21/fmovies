"""
This is the url configuration file for the web module.
@author info@asquarexpert.com
"""

from django.conf.urls import url,include
from django.contrib import admin
from apps.web import views
urlpatterns = [
    url(r'^/$', views.load_login_page),
    url(r'/login/$', views.load_login_page),
    url(r'/login/login_auth/', views.login_auth),
    url(r'/home/', views.HomeView.as_view()),
    url(r'/logout/', views.logout_view),
    url(r'/signup/', views.signup_auth),
    # url(r'/reset_password/', views.forget_page),
    url(r'/forget_pass/',views.ForgotPassword.as_view()),
    url(r'/reset_pass/', views.ResetPassword.as_view()),
    url(r'/leaderboard/', views.LeaderBoardView.as_view()),
    url(r'/searchmovie/', views.SearchMovie.as_view()),
    url(r'/addmovie/', views.AddMovieView.as_view()),
    url(r'/removemovie/', views.RemoveMovieView.as_view()),
    # url(r'/profile/', views.ProfileView.as_view()),
    url(r'/Profile/', views.ProfileView.as_view()),
    url(r'/mymovies/', views.MyMoviesView.as_view()),
    url(r'/showmovie/', views.LeaderBoardView.as_view())
]
