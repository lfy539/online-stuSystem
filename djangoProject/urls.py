"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

import xadmin

from apps.users.views import LoginView, LogoutView,SendSmsView,DynamicLoginView,RegisterView

from djangoProject.settings import MEDIA_ROOT
from apps.operations.views import IndexView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(),name="index"),
    # path('login/', TemplateView.as_view(template_name="login.html"),name="login"),
    path('login/', LoginView.as_view(),name="login"),
    path('d_login/',DynamicLoginView.as_view(), name="d_login"),
    path('register',RegisterView.as_view(),name="register"),
    path('logout/', LogoutView.as_view(),name="logout"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms"),

    # 配置上传文件注释url
    url(r'media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),

    # 配置上传文件注释url
    # url(r'static/(?P<path>.*)$',serve,{"document_root":STATIC_ROOT}),

    # 机构相关
    url(r'^org/', include(('apps.organizations.urls',"organizations"),namespace="org")),

    # 课程相关
    url(r'^course/', include(('apps.courses.urls',"courses"),namespace="course")),

    # 用户相关操作
    url(r'^op/', include(('apps.operations.urls',"operations"),namespace="op")),
    # 用户个人中心
    url(r'^users/', include(('apps.users.urls',"users"),namespace="users")),




]

# 编写一个view的几个步骤
 # 1. view 代码
 # 2. 配置url
 # 3. 修改html页面相关的地址
