import django

from apps.users.views import UserInfoView,UploadImageView,ChangePwdView,MyCourseView
from apps.users.views import MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView


if django.VERSION >= (3, 1, 0):
    from django.urls import re_path as url
else:
    from django.conf.urls import url

urlpatterns = [
    url(
        r'^info/$',
        UserInfoView.as_view(),
        name="info"
    ),
    url(
        r'^image/upload/$',
        UploadImageView.as_view(),
        name="image"
    ),
    url(
        r'^update/pwd/$',
        ChangePwdView.as_view(),
        name="update_pwd"
    ),
    url(
        r'^mycourses/$',
        MyCourseView.as_view(),
        name="mycourses"
    ),
    url(
        r'^myfavorg/$',
        MyFavOrgView.as_view(),
        name="myfavorg"
    ),
    url(
        r'^myfavteacher/$',
        MyFavTeacherView.as_view(),
        name="myfavteacher"
    ),
    url(
        r'^myfavcourse/$',
        MyFavCourseView.as_view(),
        name="myfavcourse"
    ),
    url(
        r'^messages/$',
        MyMessageView.as_view(),
        name="messages"
    ),


]
