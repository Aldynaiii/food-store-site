from django import forms
from .models import Users, Orders, Products

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['login', 'full_name', 'phone', 'email']

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if Users.objects.filter(login=login).exists():
            raise forms.ValidationError('Логин уже существует')
        return login

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class OrderForm(forms.ModelForm):
    delivery_date = forms.DateField(widget=forms.SelectDateWidget, required=False)
    payment_method = forms.ChoiceField(choices=[('cash', 'Наличные'), ('card', 'Карта')])
    product = forms.ModelChoiceField(queryset=Products.objects.all(), label='Товар')
    quantity = forms.IntegerField(min_value=1, label='Количество')

    class Meta:
        model = Orders
        fields = ['delivery_date', 'payment_method']