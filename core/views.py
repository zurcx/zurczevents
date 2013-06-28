#encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse

from forms import ContactForm

def home(request):
    context = {
        'nome': u'Gileno',
        'email': u'gascf.cin@gmail.com',
    }
    return render(request, 'home.html', context)

def contact(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_mail()
            context['success'] = True
    else:        
        form = ContactForm()
    context['form'] = form
    return render(request, 'contact.html', context)