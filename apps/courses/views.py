from django.shortcuts import render
from pure_pagination import Paginator
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from apps.courses.models import Course, CoureTag, CourseResource, Video
from apps.operations.models import UserFavorite,UserCourse,CourseComments


class VideoView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, course_id, video_id, *args, **kwargs):
        """获取课程章节信息"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))




        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]

        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video" : video,
        })





class CourseCommentView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """获取课程章节信息"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        # 1,学习用户和课程之间的关联
        # 2.对view进行login登录的验证
        # 3. 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]

        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url =  "/login/"
    def get(self, request, course_id, *args, **kwargs):
        """获取课程章节信息"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 1,学习用户和课程之间的关联
        # 2.对view进行login登录的验证
        # 3. 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course = course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course = course)
        user_ids =[user_course.id for user_course in user_courses]

        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course for user_course in all_courses]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources" : course_resources,
            "related_courses" : related_courses,

        })

class CourseDetailView(View):
    def get(self, request,course_id,  *args, **kwargs):
        """获得课程详情"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


        # 通过课程的tag做课程的推荐
        # tag = course.tag
        # related_course = []
        # if tag:
        #     related_course = Course.objects.filter(tag=tag).exclude(id_in=[course.id])[:3]

        tags = course.couretag_set.all()
        tag_list = [tag.tag for tag in tags]
        # tag_list = []
        # for tag in tags:
        #     tag_list.append(tag.tag)
        course_tags = CoureTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html",{
            "course":course,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
            "related_courses" : related_courses,

        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        all_courses = Course.objects.order_by("-add_time")
        hot_courss = Course.objects.order_by("-click_nums")[:3]

        # 搜索关键词
        keywords = request.GET.get("keyword","")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))


        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(all_courses, per_page=2, request=request)
        courses = p.page(page)

        return render(request, "course-list.html",{
            "all_courses" : courses,
            "sort" : sort,
            "hot_courss" : hot_courss,
            "keywords" : keywords,
            "s_type" : s_type
        })


