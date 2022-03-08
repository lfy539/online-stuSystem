from django import forms
from captcha.fields import CaptchaField
from apps.users.models import UserProfile


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=4)
    password2 = forms.CharField(required=True, min_length=4)

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name","gender","birthday","address"]


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    #  code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def changed_mobile(self):
        mobile = self.data.get("mobile")
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("手机号码已注册")
        return mobile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    # def clean_code(self):
    #     mobile = self.data.get("mobile")
    #     code = self.data.get("code")
    #     r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=0,charset="utf8")
    #     redis_code = r.get(str(mobile))
    #     if code != redis_code:
    #         raise forms.ValidationError("验证码不正确")
    #     return self.cleaned_data
