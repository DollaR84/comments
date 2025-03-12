"""Comments URL Configuration

"""

from django.conf.urls import url

from .views import CommentView

app_name = 'comments'
urlpatterns = [
    url(r'^$', CommentView.as_view(), name="index"),
]
