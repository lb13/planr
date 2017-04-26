from django.conf.urls import url
from . import views

app_name = 'curriculum'

urlpatterns = [
    # /curriculum/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /curriculum/123/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /curriculum/offering/add
    url(r'^offering/add/$', views.OfferingCreate.as_view(), name='offering-add'),
    # /curriculum/offering/add
    url(r'^offering/(?P<pk>[0-9]+)/$', views.OfferingUpdate.as_view(), name='offering-update'),
    # /curriculum/offering/add
    url(r'^offering/(?P<pk>[0-9]+)/delete/$', views.OfferingDelete.as_view(), name='offering-delete'),
]
