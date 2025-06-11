from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/create/', NewsCreateView.as_view(), name='create_news'),
    path('news/<slug:news>/', news_detail, name='news_detail'),
    path('news/<slug>/update/', NewsUpdateView.as_view(), name='update_news'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='delete_news'),
    path('contact', ContactPageView.as_view(), name='contact'),
    path('local/', LocalNewsView.as_view(), name='local_news'),
    path('foreign/', ForeignNewsView.as_view(), name='world_news'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news'),
    path('sport/', SportNewsView.as_view(), name='sport_news'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresults/', SearchResultsView.as_view(), name='search_results'),
]