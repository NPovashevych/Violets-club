from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from club.models import Member, Variety, Violet


class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "experience",
            "status",
            "country",
            "city",
        )

    def clean_experience(self):
        return validate_experience(self.cleaned_data["experience"])


class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "experience",
            "status",
            "country",
            "city",
        )

    def clean_experience(self):
        return validate_experience(self.cleaned_data["experience"])


def validate_experience(experience: int):
    if experience < 0:
        raise ValidationError("Experience should be more 0")
    elif experience > 90:
        raise ValidationError("This cannot be true")
    return experience


class MemberSearchForm(forms.Form):
    username = forms.CharField(
        max_length=120,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class VioletSearchForm(forms.Form):
    sort = forms.CharField(
        max_length=120,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by sort"})
    )


class VioletForm(forms.ModelForm):
    member = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Violet
        fields = "__all__"
