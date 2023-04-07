from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from app.models import *
from captcha.fields import CaptchaField


CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'discount_price', 'description', 'brand', 'category', 'product_image']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'discount_price':forms.NumberInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'brand':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(choices=CATEGORY_CHOICES, attrs={'class':'form-control'}),
            'product_image':forms.FileInput(attrs={'class':'form-control'}),
        }


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'discount_price', 'description', 'brand', 'category', 'product_image']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'discount_price':forms.NumberInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'brand':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(choices=CATEGORY_CHOICES, attrs={'class':'form-control'}),
            'product_image':forms.FileInput(attrs={'class':'form-control'}),
        }


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        label = 'Email'
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Username', widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    captcha = CaptchaField()

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'autofocus':True, 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password1 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'autofocus':True, 'class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label=_("Email"), widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(_("There is no user registered with the specified email address."))
        return email


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-class'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-class'}), help_text=password_validation)
    

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zip_code']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zip_code':forms.NumberInput(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'row':'3', 'placeholder':'Say something...'}))
    class Meta:
        model = Comment
        fields = ['body']