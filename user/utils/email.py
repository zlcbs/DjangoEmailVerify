from __future__ import unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render


def send_activate_mail(request, to, subject, template, **kwargs):
    html = render(request, template + '.html', {'token': kwargs['token'], 'username': kwargs['username']})
    text = render(request, template + '.txt', {'token': kwargs['token'], 'username': kwargs['username']})

    msg = EmailMultiAlternatives(subject, text.content.decode('utf-8'), 'zlcbs97@aliyun.com', ['1429974159@qq.com'])
    msg.attach_alternative(html.content.decode('utf-8'), "text/html")

    msg.send()
