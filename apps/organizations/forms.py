from django import forms
import re
from apps.operations.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11,min_length=11,required=True)
    class Meta:
        model = UserAsk
        fields = ["name","mobile","course_name"]

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "/^[1]([3-9])[0-9]{9}$/"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法",code="mobile_invalid")