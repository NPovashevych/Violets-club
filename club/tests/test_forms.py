from django.test import TestCase

from club.forms import (
    MemberCreationForm,
    MemberSearchForm,
    VioletSearchForm,
)


class MemberCreationFormTest(TestCase):
    def test_member_creation_form_with_additional_fields(self):
        test_data = {
            "username": "test_username",
            "password1": "password_test",
            "password2": "password_test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test@email.com",
            "experience": "10",
            "status": "beginner",
            "country": "test_country",
            "city": "test_city",
        }
        form = MemberCreationForm(data=test_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)

    def test_member_experience_is_valid(self):
        test_data = {"experience": "10", }
        form = MemberCreationForm(data=test_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)

    def test_member_experience_is_not_valid(self):
        test_data = {"experience": "100", }
        form = MemberCreationForm(data=test_data)
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    def test_member_search_is_valid(self):
        test_data = {"username": "test_username", }
        form = MemberSearchForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_violet_search_is_valid(self):
        test_data = {"sort": "test_sort", }
        form = VioletSearchForm(data=test_data)
        self.assertTrue(form.is_valid())
