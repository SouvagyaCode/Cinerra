from django.urls import path
from . import views
from movie_review.views import home
urlpatterns = [
    path('', home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.user_logout, name='logout'),
]
