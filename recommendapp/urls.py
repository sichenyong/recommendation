from django.urls import path
from recommendapp import views

urlpatterns = [
    path('',views.recommend, name="recommend"),
    
    path('hotvenues',views.getHotVenues, name="hotvenues"),

    path('rating',views.doRating, name="dorating"),

    path('search',views.search_venue, name='search')
]