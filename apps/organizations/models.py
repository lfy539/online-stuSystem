from datetime import datetime

from django.db import models

from apps.users.models import BaseMode


class CityDict(models.Model):
    name = models.CharField('城市', max_length=20)
    desc = models.CharField('描述', max_length=200)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseMode):
    ORG_CHOICES = (
        ("pxjg", u"培训机构"),
        ("gx", u"高校"),
        ("gr", u"个人"),
    )
    name = models.CharField('机构名称', max_length=50)
    desc = models.TextField('机构描述')
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name=u"机构类别", default="pxjg")
    click_nums = models.IntegerField('点击数', default=0)
    tag = models.CharField('机构标签', max_length=10, default='全国知名')
    fav_nums = models.IntegerField('收藏数', default=0)
    students = models.IntegerField("学习人数", default=0)
    course_nums = models.IntegerField("课程数", default=0)
    image = models.ImageField('logo', upload_to='org/%Y/%m', max_length=100)
    address = models.CharField('机构地址', max_length=150, )
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)

    def courses(self):
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    def teachers(self):
        return self.teacher_set.all()

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaseMode):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构', on_delete=models.CASCADE)
    name = models.CharField('教师名', max_length=50)
    work_years = models.IntegerField('工作年限', default=0)
    work_company = models.CharField('就职公司', max_length=50)
    work_position = models.CharField('公司职位', max_length=50)
    points = models.CharField('教学特点', max_length=50)
    click_nums = models.IntegerField('点击数', default=0)
    fav_nums = models.IntegerField('收藏数', default=0)
    teacher_age = models.IntegerField('年龄', default=25)
    image = models.ImageField(
        upload_to="teacher/%Y/%m",
        verbose_name="头像",
        max_length=100)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()
