from django.core.mail import send_mail
import pydotenv

ENV = pydotenv.Environment()


def send(message):
    mail_to = ENV["MAIL_TO"]
    if mail_to:
        send_mail(
            "Capybara API Feedback",
            message,
            None,
            [mail_to],
            fail_silently=False,
        )
