from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

'''
contact us form
'''

class ContactUs(View):
    def get(self,request,*args,**kwargs):
        return render(request, "contact/contact-us.html", {'status':'active'})
    
    def post(self,request,*args,**kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        contact=Contact.objects.create(name = name, email = email,subject = subject, message = message)
        contact.save()
        messages.success(request, 'We will get back to You Shortly!!!.')
        return redirect('contactapp:contact_us')

'''
contact-us list
'''

@login_required
def contacts(request):
    contacts=Contact.objects.all()
    return render(request, 'contact/contact-list.html', {'contacts':contacts})


'''
Reply To Contact us
'''
class send_reply(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        contact=Contact.objects.get(id=request.GET.get('id'))
        return render(request, 'contact/contact-reply.html', {'contact':contact})
    def post(self,request,*args,**kwargs):
        contact=Contact.objects.get(id=request.GET.get('id'))
        msg= request.POST.get("message")
        file=request.FILES.get("file")
        if file is None:
            file=None
        current_site = get_current_site(request)
        context = {
            'contact':contact,'msg':msg,'file':file, 'domain':current_site.domain,
        }
        message = render_to_string('registration/verify_email.html', context)
        mail_subject = request.POST.get("subject")
        to_email="mohitk3320@gmail.com"
        email_message = EmailMultiAlternatives(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
        html_email = render_to_string('registration/verify_email.html',context)
        email_message.attach_alternative(html_email, 'text/html')
        email_message.send()
        ContactReply.objects.create(reply= msg, contact=Contact.objects.get(id=contact.id),image_file=file, subject=mail_subject)
        return redirect('contactapp:contacts')


'''
View Reply
'''

def DisplayReply(request):
    return render(request, 'registration/verify_email.html')