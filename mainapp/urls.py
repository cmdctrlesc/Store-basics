from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'mainapp'


urlpatterns = [
    path('', views.mainview, name="mainview"),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('search/', views.search, name="searchresults"),
    path('everythingsearch/', views.everythingsearch, name="everythingsearch"),
    path('albumsearch/', views.albumsearch, name="albumsearch"),
    path('artistsearch/', views.artistsearch, name="artistsearch"),
    path('recordlabelsearch/', views.recordlabelsearch, name="recordlabelsearch"),
    path('allfromlabel/', views.seeallfromlabel, name="allfromlabel"),
    path('allfromartist/', views.seeallfromartist, name="allfromartist"),




]
