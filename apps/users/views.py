from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator,PageNotAnInteger

from apps.courses.models import Course
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm,RegisterPostForm,UploadImageForm
from apps.users.forms import UserInfoForm,ChangePwdForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from djangoProject.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile
from apps.operations.models import UserCourse,UserFavorite,UserMessage,Banner
from apps.organizations.models import CourseOrg,Teacher


def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums':request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class MyMessageView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self,request,*args,**kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "messages"
        for message in messages:
            message.has_read = True
            message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, per_page=1, request=request)
        messages = p.page(page)

        return render(request,"usercenter-message.html",{
            "current_page" : current_page,
            "messages" : messages
        })


class MyFavCourseView(LoginRequiredMixin,View):

    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavcourse"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Course.objects.get(id=fav_course.fav_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list" : course_list,
            "current_page" : current_page
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavteacher"
        teacher_list =[]
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list" : teacher_list,
            "current_page" : current_page
        })


class MyFavOrgView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list =[]
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list" : org_list,
            "current_page" : current_page
        })


class MyCourseView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self,request,*args,**kwargs):
        current_page = "mycourses"
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request,"usercenter-mycourse.html",{
            "my_courses" : my_courses,
            "current_page":current_page
        })

class ChangePwdView(View):
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():

            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
                return JsonResponse({
                    "status": "fail",
                    "msg":"密码不一致"
                })
            user = request.user
            user.set_password(pwd1)
            user.save()
            login(request,user)


            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(pwd_form.errors)


class UserInfoView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self,request, *args, **kwargs):
        current_page = "info"
        return render(request, "usercenter-info.html",{
            "current_page":current_page
        })

    def post(self,request, *args,**kwargs):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(user_info_form.errors)

class UploadImageView(LoginRequiredMixin,View):
    login_url = "/login/"

    def post(self,request, *args, **kwargs):
        # 处理用户上传头像
        # files = request.FILES["image"]
        # self.save_file(files)

        # 如果用一个文件上传多次,相同名称的文件应该如何处理
        # 文件的路径应该写到user
        # 还没有做表单验证

        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status":"success",

            })
        else:
            return JsonResponse({
                "status":"fail"
            })

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request,"register.html",{
                "register_get_form":register_get_form
            })


class DynamicLoginView(View):

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]

            existed_user = UserProfile.objects.filter(mobile=mobile)
            if existed_user:
                user = existed_user[0]

            else:
                user = UserProfile(username=mobile)
                password = generate_random(10, 1)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {"login_form": login_form})


class SendSmsView(View):
    def get(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]

            # 随机生成数字验证码
            code = generate_random(4, 0)
            res_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if res_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8")
                r.set(mobile, code)
                r.expire(str(mobile), 60 * 5)  # 5分钟过期
            else:
                re_dict["msg"] = res_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        banners = Banner.objects.all()[:3]
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next":next,
            "banners":banners
        })

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():

            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)

            if user is not None:
                # 查询到用户
                login(request, user)
                # 登录成功应该怎么返回页面
                next = request.GET.get("next","")
                if next:
                    return HttpResponseRedirect(reverse("next"))
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form,"banners" : banners})

        else:
            return render(request, "login.html", {"login_form": login_form,"banners" : banners})
