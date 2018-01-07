from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^index.html$', views.index_search, name="search"),
    url(r'^clusters/index.html$', views.index_cluster, name="cluster")
]
