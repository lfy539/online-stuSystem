import django
from apps.organizations.views import OrgView, AddAskView, OrgHomeView,OrgTeacherView
from apps.organizations.views import OrgCourseView,OrgDescView,TeacherListView,TeacherDetailView
if django.VERSION >= (3, 1, 0):
    from django.urls import re_path as url
else:
    from django.conf.urls import url

urlpatterns = [
    url(
        r'^list/$',
        OrgView.as_view(),
        name="list"
    ),
    url(
        r'^add_ask/$',
        AddAskView.as_view(),
        name="add_ask"
    ),
    url(
        r'^(?P<org_id>\d+)/$',
        OrgHomeView.as_view(),
        name="home"
    ),
    url(
        r'^(?P<org_id>\d+)/teacher/$',
        OrgTeacherView.as_view(),
        name="teacher"
    ),
    url(
        r'^(?P<org_id>\d+)/course/$',
        OrgCourseView.as_view(),
        name="course"
    ),
    url(
        r'^(?P<org_id>\d+)/desc/$',
        OrgDescView.as_view(),
        name="desc"
    ),
    url(
        r'^teachers/$',
        TeacherListView.as_view(),
        name="teachers"
    ),
    url(
        r'^teachers/(?P<teacher_id>\d+)/$',
        TeacherDetailView.as_view(),
        name="teacher_detail"
    ),

]
