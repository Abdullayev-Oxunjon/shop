from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import HiddenInput

from app.models import Product, Feedback, Post, User, Order


class ProductModelForm(forms.ModelForm):
    user = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Product
        exclude = ()


class FeedbackModelForm(forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ()


class PostModelForm(forms.ModelForm):
    user = forms.IntegerField(widget=HiddenInput(), required=False )

    class Meta:
        model = Post
        exclude = ()


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=155)
    confirm_password = forms.CharField(max_length=155)

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).first():
           raise ValidationError("Bu email bazada bor !")
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')

        if password != confirm_password:
            return ValidationError('Confirm password xato kiritildi !')

        return password
    @atomic
    def save(self):
        user = User.objects.create_user(email=self.cleaned_data.get('email'))
        user.set_password(raw_password = self.cleaned_data.get('password'))
        user.save()


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField()
    password = forms.CharField(max_length=55)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data




class OrderForm(forms.ModelForm):
    cart_number = forms.CharField(max_length=16, min_length=16)
    phone_number = forms.CharField(max_length=13)

    class Meta:
        model = Order
        fields = ['cart_number', 'phone_number']