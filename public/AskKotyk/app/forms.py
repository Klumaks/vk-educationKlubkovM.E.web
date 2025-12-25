from django import forms
from django.contrib.auth import authenticate
from django.forms.widgets import PasswordInput
from django.core.exceptions import ValidationError
from app.models import User, Question, Answer, Tag
import os

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your login here'
        })
    )
    password = forms.CharField(
        max_length=128,
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    'Sorry, wrong password!'
                )

        return cleaned_data


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your login'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    nickname = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your nickname'
        })
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password_confirm = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Sorry, this email address already registered!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Passwords do not match')

        return cleaned_data


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter up to 3 tags separated by commas'
        }),
        help_text='Add up to 3 tags separated by commas'
    )

    class Meta:
        model = Question
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question title',
                'maxlength': '100'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your question in detail',
                'rows': 6,
                'maxlength': '1000'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 10:
            raise ValidationError('Title must be at least 10 characters long')
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if len(text) < 20:
            raise ValidationError('Question text must be at least 20 characters long')
        return text

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        if len(tags_list) > 3:
            raise ValidationError('You can add maximum 3 tags')

        return tags_list


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your answer here',
                'rows': 6
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if len(text) < 10:
            raise ValidationError('Answer must be at least 10 characters long')
        return text


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError('Image file too large ( > 2MB )')
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            extension = os.path.splitext(avatar.name)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError('Unsupported file extension. Use: JPG, JPEG, PNG, GIF')
        return avatar
