import xadmin

from apps.organizations.models import Teacher, CourseOrg, CityDict


class TeacherAdmin(object):
    list_display = ["name", "org", "click_nums", "fav_nums"]
    search_fields = ["name", "work_years", "click_nums", "fav_nums"]
    list_filter = ["org","work_years","points"]


class CourseOrgAdmin(object):
    list_display = ["name", "desc", "click_nums", "fav_nums"]
    search_fields = ["name", "desc", "click_nums", "fav_nums"]
    list_filter = ["name","click_nums", "fav_nums"]

class CityDictAdmin(object):
    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_editable = ["name", "desc"]


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)