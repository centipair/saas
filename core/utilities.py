import hashlib
import random
import datetime
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
#from django.utils.html import strip_tags

from django.conf import settings
import os
import re
import base64

us_states = ["Alabama",
             "Alaska",
             "Arizona",
             "Arkansas",
             "California",
             "Coloroda",
             "Connecticut",
             "Delaware",
             "Florida",
             "Georgia",
             "Hawaii",
             "idaho",
             "Illinois",
             "Indiana",
             "Lowa",
             "Kansas",
             "Kentucky",
             "Louisiana",
             "Maine",
             "Maryland",
             "Massachusetts",
             "Michigan",
             "Minnesota",
             "Mississippi",
             "Missouri",
             "Montana",
             "Nebraska",
             "Nevada",
             "New Hampshire",
             "New Jersey",
             "New Mexico",
             "New York",
             "North Carolina",
             "North Dakota",
             "Ohio",
             "Oklahoma",
             "Oregon",
             "Pennsylvania",
             "Rhode Island",
             "South Carolina",
             "South Dakota",
             "Tennessee",
             "Texas",
             "Utah",
             "Vermont",
             "Virginia",
             "Washington",
             "West Virginia",
             "Wisconsin",
             "Wyoming"]


def url_to_hyperlink(cleaned_text):
    url_reg = ('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)'
               '*)')
    urls = re.findall(url_reg, cleaned_text)
    for each_url in urls:
        cleaned_text = cleaned_text.replace(
            each_url[0],
            '<a href="' + each_url[0] +
            '">' +
            each_url[0] + '</a>')
    return cleaned_text


def unique_name(mixer):
    salt = hashlib.sha256(str(random.random())).hexdigest()[:10]
    key = hashlib.sha256(salt + mixer).hexdigest()
    return key


def send_activation_email(email, key):
    email_subject = 'Activate your account'
    email_body = 'Account activation Link %(site_url)s/activate/%(activation_key)s' % {"site_url": settings.SITE_URL, "activation_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def send_password_reset_email(email, key):
    email_subject = 'Password reset'
    email_body = 'Password Reset Link %(site_url)s/password/reset/form/%(activation_key)s' % {"site_url": settings.SITE_URL, "activation_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def send_register_success_email(email):
    subject = 'Registration request received'
    email_body_text = 'Registration request received successfully. We will let you know when it is approved'
    email_body_html  = render_to_string('mail/signup_success.html', {"email": email, "subject": subject })
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    msg = EmailMultiAlternatives(subject,
                                 email_body_text,
                                 from_email, [to_email])
    msg.attach_alternative(email_body_html, "text/html")
    msg.content_subtype = "html"
    msg.send()
    return


def send_vendor_approval_email_bkp(email, key):
    email_subject = 'Request approved'
    email_body = ' Approval link: %(site_url)sstore/vendor/create/account/%(approval_key)s' % {"site_url": settings.SITE_URL, "approval_key": key}
    send_mail(email_subject,
              email_body,
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)


def send_vendor_approval_email(email, key):
    email_subject = 'Request approved'
    email_body = 'Your somethinglocal request has been approved. Please signin to add your items.'
    send_mail(email_subject,
              email_body,
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)


def send_contact_email(contact_details):
    email_subject = "Contact inquiry from: " + contact_details["name"]
    email_body = contact_details["name"] + "\r\n" + contact_details["email"] + "\r\n" + contact_details["message"] \
                 + "\r\n" + contact_details["website"] + "\r\n" + contact_details["twitter"] + "\r\n" + contact_details["facebook"]
    send_mail(email_subject,
              email_body,
              settings.EMAIL_HOST_USER,
              ["rafael@somethingloc.al"],
              fail_silently=False)


def send_sale_notification_email(item):
    email_subject = 'SomethingLocal Sold Item: ' + item.title
    email_body = 'Seling price:' + str(item.price) + '\r\n' +\
                 'Please visit your dashboard for more details'
    send_mail(email_subject,
              email_body,
              settings.EMAIL_HOST_USER,
              [item.store.owner.email],
              fail_silently=False)
    return


def send_payment_receipt():
    return


def send_stock_low_warning_email(item):
    email_subject = "Warning Low stock for Item: " + item.title
    email_body = 'Item : ' + item.title + '\r\n' + \
                 'Remaining: ' + str(item.stock)
    send_mail(email_subject,
              email_body,
              settings.EMAIL_HOST_USER,
              [item.store.owner.email],
              fail_silently=False)


def replace_email_with_username(username):
    replaced = username
    replaced = replaced.replace('@', 'at')
    replaced = replaced.replace('.', 'dot')
    return replaced


def create_key(mixer, expiry):
    salt = hashlib.sha256(str(random.random())).hexdigest()[:10]
    key = hashlib.sha256(salt + mixer).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    return {"key": key, "expiry": key_expires}


def random_string():
    key = base64.b64encode(
        hashlib.sha256(str(random.getrandbits(256))).digest(),
        random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')
    return key


def reply_object():
    """
    reference for the reply json object
    """
    reply_object = {"code": "", "status_code": 200}
    return reply_object


def create_directory(dir_name):
    """
    creates new directory
    """
    newpath = settings.SITE_TEMPLATE_DIR + "/" + dir_name
    if not os.path.exists(newpath):
        os.makedirs(newpath)


def delete_pin_image(file_name):
    try:
        os.remove(settings.UPLOAD_PATH + "similar_" + file_name)
    except:
        pass
    try:
        os.remove(settings.UPLOAD_PATH + "more_" + file_name)
    except:
        pass
    try:
        os.remove(settings.UPLOAD_PATH + "pin_" + file_name)
    except:
        return


def delete_item_file(file_name):
    try:
        os.remove(settings.UPLOAD_PATH + file_name)
    except:
        pass
    try:
        os.remove(settings.UPLOAD_PATH + "thumb_" + file_name)
    except:
        pass
    try:
        os.remove(settings.UPLOAD_PATH + "display_" + file_name)
    except:
        return


def delete_file(file_name):
    try:
        os.remove(settings.UPLOAD_PATH + file_name)
    except:
        pass


def html_log(content, name="log.html"):
    log_file = settings.LOG_PATH + "/"+name
    f = open(log_file, "w")
    f.write(content)
    f.close()


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_limit_offset(request):
    limit_offset = {"limit": 20, "offset": 0}
    try:
        if "limit" in request.GET:
            limit_offset["limit"] = int(request.GET["limit"])
        if "offset" in request.GET:
            limit_offset["offset"] = int(request.GET["offset"])
    except:
        return limit_offset

    return limit_offset
