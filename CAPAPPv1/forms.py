from django.contrib.auth.forms import UserCreationForm
from .models import Student, Course, Room, User, Contact
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'same as your roll no.',
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_name',
            'father_name',
            'enrollment_no',
            'course',
            'dob',
            'gender']
############################################################


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'message'
        ]
#############################################################


class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_name',
            'father_name',
            'enrollment_no',
            'dob',
            'gender',
            'course',
            'room',
            'reserved_start_date',
            'reserved_end_date'
        ]


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['room',
                  'reserved_start_date',
                  'reserved_end_date'
                  ]


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=False))