import xadmin


from apps.operations.models import UserAsk, CourseComments, UserFavorite,UserCourse,UserMessage
from apps.operations.models import Banner


class BannerAdmin(object):
    list_dislay = ["title", "image", "url","index"]
    search_fields = ["title", "image", "url","index"]
    list_filter = ["title", "image", "url","index"]


class UserAskAdmin(object):

    list_dislay = ["name", "mobile", "course_name"]
    search_fields = ["name", "mobile", "course_name"]
    list_filter = ["name", "mobile", "course_name"]


class UserCourseAdmin(object):
    list_dislay = ["user","course","add_time"]
    search_fields = ["user","course","add_time"]
    list_filter = ["user","course","add_time"]


class CourseCommentsAdmin(object):
    list_dislay = ["user", "course","comments","add_time"]
    search_fields = ["user", "course","comments","add_time"]
    list_filter = ["user", "course","comments","add_time"]


class UserMessageAdmin(object):
    list_dislay = ["user", "message","has_read", "add_time"]
    search_fields = ["user", "message","has_read", "add_time"]
    list_filter = ["user", "message","has_read", "add_time"]


class UserFavoriteAdmin(object):
    list_dislay = ["user", "fav_id","fav_type", "add_time"]
    search_fields = ["user", "fav_id","fav_type", "add_time"]
    list_filter = ["user", "fav_id","fav_type", "add_time"]


xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(Banner,BannerAdmin)