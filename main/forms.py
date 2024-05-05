from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from .models import *
from ckeditor.widgets import CKEditorWidget
User = ModAdmin

class RegisterForm(forms.ModelForm):
    """
    The default registration form for users.
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']  # Sử dụng 'username' thay vì 'username'

    def clean_username(self):
        '''
        Verify username is available.
        '''
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data



class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'is_active']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Username',
            'autofocus': True,
            'required': 'required'
        })
    )
    
    password = forms.CharField(label='', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'pass',
            'placeholder': 'Mật khẩu',
            'required': 'required'
        }),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MemberForm(forms.ModelForm):
    class Meta:
        model = ModAdmin
        fields = ['username', 'password', "full_name", "email", "mssv",  "image", "role", "class_school", "is_staff","describe"]  

    widget_attrs = {
        'class': 'form-control',
    }
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )
    full_name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )
    mssv = forms.CharField(
        label='MSSV',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )
    describe = forms.CharField(
        widget=CKEditorWidget(),  # Use CKEditorWidget for the 'content' field
    )
    image = forms.CharField(
        label='Image Url',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )
    # image = forms.ImageField(
    #     label='Image',
    #     widget=forms.FileInput(attrs={'class': 'form-control', "id" : "formFile"}),
    # )
    # role = forms.CharField(
    #     label='Role',
    #     widget=forms.TextInput(attrs={**widget_attrs,}),
    # )
    class_school = forms.CharField(
        label='Class School',
        widget=forms.TextInput(attrs={**widget_attrs,}),
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'author', 'abstract', 'link_paper', 'link_github', 'institute','interest', 'id_user', 'year']

    widget_attrs = {
        'class': 'form-control',
    }

    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Write some title ...'}),
    )
    author = forms.CharField(
        label='Author',
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Write some author ...'}),
    )
    abstract = forms.CharField(
        label='Abstract',
        widget=forms.Textarea(attrs={**widget_attrs, 'placeholder': 'Write some abstract ...'}),
    )
    link_paper = forms.CharField(
        label='Link_paper',
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Write some link paper ...'}),
    )
    link_github = forms.CharField(
        label='Link_github',
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Write some link github ...'}),
    )
    institute = forms.CharField(
        label='Institute',
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Write some institute ...'}),
    )
    # interest = forms.BooleanField(
    #     label='Interest',
    #     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    # )
    id_user = forms.ModelChoiceField(
        label='User',
        queryset=ModAdmin.objects.all(),  # Replace with your actual queryset
        widget=forms.Select(attrs={**widget_attrs, 'placeholder': 'Write some User ...'}),
    )
    year = forms.IntegerField(
        label='Year',
        widget=forms.NumberInput(attrs={**widget_attrs, 'placeholder': 'Year'}),
    )


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = [ 'image_avatar', 'name_event', 'content', 'time', 'id_user', 'form_register']

    widget_attrs = {
        'class': 'form-control',
    }

    image_avatar = forms.ImageField(
        label="Image background",
        widget=forms.FileInput(attrs={'class': 'form-control', "id" : "formFile"}),
    )

    name_event = forms.CharField(
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Event Name'}),
    )

    content = forms.CharField(
        widget=CKEditorWidget(),  # Use CKEditorWidget for the 'content' field
    )

    time = forms.DateField(
        widget=forms.DateInput(attrs={**widget_attrs, 'placeholder': 'Event Time', 'type': 'date'}),
    )

    id_user = forms.ModelChoiceField(
        queryset=ModAdmin.objects.all(),  # Replace with your actual queryset
        widget=forms.Select(attrs={**widget_attrs}),
    )

    form_register = forms.CharField(
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Registration Form'}),
    )

