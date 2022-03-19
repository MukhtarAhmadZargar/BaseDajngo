from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from .models import Faq
from django.core.paginator import Paginator #import Paginator



'''
Faq Index 
'''
def FaqHome(request):
    faqs=Faq.objects.all().order_by('-id')
    paginator = Paginator(faqs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'faq/home.html',{'faqs':page_obj})


'''
Create FAQ
'''
@login_required
def AddFAQ(request):
    if request.method=='POST':
        question=request.POST.get('question')
        Answer=request.POST.get('Answer')
        if not Answer:
            Answer= "Not Yet Answered..."
        faq=Faq.objects.create(question=question,answer=Answer)
        faq.save()
        messages.success(request,'FAQ Added Successfully!!!')
        return redirect('faq:faq_home')
    return render(request, 'faq/add.html')


'''
View FAQ
'''
@login_required
def ViewFAQ(request,id):
    faq=Faq.objects.get(id=id)
    return render(request, 'faq/view-faq.html',{'faq':faq})


'''
Edit FAQ
'''
class EditFAQ(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        faq=Faq.objects.get(id=request.GET.get("id"))
        return render(request, 'faq/edit-faq.html',{"faq":faq})

    def post(self,request,*args,**kwargs):
        id=request.GET.get("id")
        faq=Faq.objects.get(id=request.GET.get("id"))

        if request.POST.get("question"):
            faq.question=request.POST.get("question")
            
        if request.POST.get("answer"):
            faq.answer = request.POST.get("answer")
        else:
            faq.answer = "Not Yet Answered..."

        faq.save()
        messages.success(request, 'FAQ Edited Successfully')

        return redirect('faq:View_FAQ' , id=faq.id)


'''
Delete FAQ 
'''
@login_required
def DeleteFAQ(request):
    id=request.GET.get('id')
    faq=Faq.objects.get(id=id)
    faq.delete()
    messages.success(request, 'FAQ Deleted Successfully')
    return redirect('faq:faq_home')
