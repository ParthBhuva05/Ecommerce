from django.shortcuts import render, redirect ,HttpResponse
from account.forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# varification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                username = username
            )
            user.phone_number = phone_number
            user.save()

            # Account Activation

            current_site  = get_current_site(request)
            mail_subject = "Please Activate Your Account"
            message = render_to_string('account/account_varification_mail.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()

            # messages.success(request, "Thank you for registrationwith us we have to sent you on verification mail to your email")
            # return redirect('register')

            return redirect('account/login/?command=varification&email=' + email)

        else:
            messages.error(request, 'Registration Faield...!')
            # return redirect('register')
    else: 
        form = RegistrationForm()
    context = {
        'form': form
    }

    return render(request, 'account/register.html', context)


def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email, password = password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in...!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials...!")
            return redirect('login')

    return render(request, 'account/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logout...!")
    return redirect('login')



# Account Activate
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation your account is activated...!')
        return redirect('login')

    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


        # https://myaccount.google.com/apppasswords?rapt=AEjHL4Optl0sAUYnqeb5P8wz9WruqZK-IKDcaeYPhCdGN7pm-JxQEFPwlwTyPZ82cHHr-sZKEV7aJXPlNEUJO2vauSED18DgvTDWw9fsxG0NXiQ-7ZC8hso


# Dashboard 
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


# Forgot Password 

def forgotpassword(request):
    if request.method=="POST":
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact = email)

            # send mail for reset password

            current_site  = get_current_site(request)
            mail_subject = "Reset your Password"
            message = render_to_string('account/reset_password_mail.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
            messages.success(request, 'Reset Password mail has been send your email.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgotpassword')

    else:
        return render(request, 'account/forgotpassword.html')



# resetpassword_validate

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset your Password...!')
        return redirect('resetPassword')
    
    else:
        messages.error(request, 'This Link has been Expired...!')
        return redirect('login')



def resetPassword(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successfully...!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match...!')
            return redirect('resetPassword')

    else:
        return render(request, 'account/resetPassword.html')