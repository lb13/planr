from django.conf.urls import url, include
from django.contrib import admin
from curriculum import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^curriculum/', include('curriculum.urls')),
]
