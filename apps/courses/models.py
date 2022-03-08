from datetime import datetime

from django.db import models

from apps.users.models import BaseMode
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
# 1. 设计表结构有几个重要的点
"""
    实体1 《关系》 实体2
    课程 章节 视频 课程资源
"""


# 2. 课程实体的具体字段


# 3. 每个字段的类型，是否必填？


class Course(BaseMode):
    '''课程'''
    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True, on_delete=models.CASCADE)
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    degree = models.CharField('难度', choices=DEGREE_CHOICES, max_length=2)
    students = models.IntegerField("学习人数", default=0)
    fav_nums = models.IntegerField("收藏人数", default=0)
    image = models.ImageField("封面图", upload_to="courses/%Y/%m", max_length=100)
    click_nums = models.IntegerField("点击数", default=0)
    tag = models.CharField('课程标签', default='', max_length=10)
    category = models.CharField("课程类别", max_length=20, default="")
    youneed_know = models.CharField('课程须知', max_length=300, default='')
    teacher_tell = models.CharField('老师告诉你', max_length=300, default='')
    is_classics = models.BooleanField(default=False,verbose_name="是否经典")
    detail = models.TextField("课程详情")
    notice = models.CharField(verbose_name="课程公告",max_length=300,default="")
    is_banner = models.BooleanField(default=False,verbose_name="是否广告位")


    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()


class CoureTag(BaseMode):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="课程")
    tag = models.CharField('课程标签', default='', max_length=10)

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.tag

class Lesson(BaseMode):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseMode):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseMode):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100)
    file = models.FileField("下载地址", upload_to="course/resource/%Y/%m", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
