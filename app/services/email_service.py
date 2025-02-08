import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "authservice.projecttesting@gmail.com"
SMTP_PASSWORD = "txtxjyqakllwdnog"

# Custom email templates
EMAIL_TEMPLATES = {
    "register": """\
Hey {name}, 🎉

Welcome to **AI Resume Screener**! 🚀 We’re excited to have you on board.  
To complete your registration, please verify your email by entering the **One-Time Password (OTP)** below:

🔐 **{otp}**  

This OTP is **valid for 90 seconds**, so use it quickly! ⏳  

If you didn’t sign up, don’t worry—just ignore this email.  

Stay awesome,  
**AI Resume Screener Team**  
📧 support@ai-resume.com
    """,

    "login": """\
Hey {name}, 👋

Looks like you’re trying to log in! Here’s your **One-Time Password (OTP):**  

🔐 **{otp}**  

This OTP is **valid for 90 seconds** to keep your account secure. ⏳  

If this wasn’t you, we recommend changing your password immediately.  

Stay safe,  
**AI Resume Screener Team**  
📧 support@ai-resume.com
    """,

    "password_reset": """\
Hello {name}, 🔄

We received a request to reset your password. If this was you, use the OTP below:  

🔐 **{otp}**  

This OTP is **valid for 90 seconds**. If you **did not request** a password reset, simply ignore this email.  

Need help? We’re here for you!  

Warm regards,  
**AI Resume Screener Team**  
📧 support@ai-resume.com
    """,

    "registration_complete": """\
Hey {name}, 🎉

Your registration is now **complete!** ✅  
You can now log in to **AI Resume Screener** and start using all the features.

If you have any issues, feel free to reach out to us.  
Enjoy your job search journey with AI-powered insights!

Best,  
**AI Resume Screener Team**  
📧 support@ai-resume.com
    """
}

def send_email(email, otp, name, email_type):
    """Send an email with a custom template based on email_type"""
    msg = EmailMessage()
    msg["Subject"] = "🎉 Welcome to AI Resume Screener!" if email_type == "registration_complete" else "🔐 Secure Access: Your OTP Code"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email

    body = EMAIL_TEMPLATES.get(email_type, "").format(name=name, otp=otp or "N/A")
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
