import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from Project.settings import EMAIL_HOST_USER

def Sent_OTP(request, email):
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key)
    otp = totp.now()
    request.session['otp_secret_key'] = otp
    
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)

    subject = 'OTP VERIFICATIONS'
    message = f'Here Is Your OTP {otp}'
    from_mail = EMAIL_HOST_USER
    to_mail = [email]

    send_mail(subject, message, from_mail, to_mail)
