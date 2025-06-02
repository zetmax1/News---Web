from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news', news_list, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail'),
    path('contact', ContactPageView.as_view(), name='contact'),
    path('local/', LocalNewsView.as_view(), name='local_news'),
    path('foreign/', ForeignNewsView.as_view(), name='world_news'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news'),
    path('sport/', SportNewsView.as_view(), name='sport_news'),
]