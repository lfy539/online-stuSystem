import django
from apps.operations.views import AddFavView,AddCommentView


if django.VERSION >= (3, 1, 0):
    from django.urls import re_path as url
else:
    from django.conf.urls import url

urlpatterns = [
    url(
        r'^fav/$',
        AddFavView.as_view(),
        name="fav"
    ),
    url(
        r'^comment/$',
        AddCommentView.as_view(),
        name="comment"
    ),


]