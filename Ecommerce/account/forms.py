from django import forms
from account.models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Enter Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ['first_name','last_name', 'phone_number', 'email', 'password']
        

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        clean_data = super(RegistrationForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password does not match...!')