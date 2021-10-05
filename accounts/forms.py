from django import forms
from .models import Account, forgotPassword, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердить Пароль'
    }))
    class Meta:
        model = Account
        fields = ['name', 'surname', 'phone_number', 'password']
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password     = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Введенные пароли не совпадают'
            )
    

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите ваше имя'
        self.fields['surname'].widget.attrs['placeholder'] = 'Введите ваше фамилия'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Введите номер телефона'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class forgotPasswordForm(forms.ModelForm):
    class Meta:
        model = forgotPassword
        fields = ['name', 'surname', 'phone_number']

    
    def __init__(self, *args, **kwargs):
        super(forgotPasswordForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите ваше имя'
        self.fields['surname'].widget.attrs['placeholder'] = 'Введите ваше фамилия'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Введите номер телефона'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'surname', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self). __init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ('Image Files only')}, widget = forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self). __init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
