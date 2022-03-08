from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator
from django.http import JsonResponse
from django.db.models import Q

from apps.organizations.models import CourseOrg
from apps.organizations.models import CityDict,Teacher
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite


class TeacherDetailView(View):
    def get(self,request,teacher_id,*args,**kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False
        org_fav =False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
                org_fav = True

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request,"teacher-detail.html",{
            "teacher":teacher,
            "teacher_fav":teacher_fav,
            "org_fav":org_fav,
            "hot_teachers": hot_teachers,

        })

class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        # 进行排序
        keywords = request.GET.get("keyword", "")
        s_type = "teacher"
        if keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=keywords))

        sort = request.GET.get("sort", "")

        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")
        teacher_nums = all_teachers.count()
        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(all_teachers, per_page=3, request=request)
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "teachers":teachers,
            "teacher_nums" : teacher_nums,
            "sort":sort,
            "hot_teachers":hot_teachers,
            "keywords": keywords,
            "s_type": s_type
        })




class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav" : has_fav
        })

class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=1):
                has_fav = True

        all_courses = course_org.course_set.all()

        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(all_courses, per_page=5, request=request)
        orgs = p.page(page)


        return render(request, "org-detail-course.html", {
            "all_courses": orgs,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav" : has_fav
        })

class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page" : current_page,
            "has_fav" : has_fav
        })

class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,  "org-detail-homepage.html",{
                "all_courses":all_courses,
                "all_teachers" : all_teachers,
                "course_org" : course_org,
                "current_page" : current_page,
                "has_fav":has_fav,

            })


class AddAskView(View):
    def post(self, request, *args, **kwargs):
        """处理用户咨询"""
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg":"添加出错"
            })


class OrgView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        # org_nums = CourseOrg.objects.count()
        all_citys = CityDict.objects.all()

        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        keywords = request.GET.get("keyword", "")
        s_type = "org"
        if keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 课程筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        city_id = request.GET.get("city", "")

        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))
        # 对机构进行排序
        sort = request.GET.get("sort","")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category": category,
            "city_id": city_id,
            "sort" : sort,
            "hot_orgs" : hot_orgs,
            "keywords": keywords,
            "s_type": s_type,
        })
