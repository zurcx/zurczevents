#encoding: utf-8

from django.db.models import Q
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import (render, get_object_or_404, 
    redirect)
from django.core.paginator import (Paginator, PageNotAnInteger,
    EmptyPage)

from gallery.forms import AlbumForm, PhotoFormset

from models import Event
from forms import CommentForm, EventForm

def index(request):
    template_name = 'events/index.html'
    context = {}
    events = Event.objects.all()
    search = request.GET.get('search', '')
    if search:
        events = events.filter(Q(name__icontains=search) \
                               | Q(description__icontains=search))
    
    paginator = Paginator(events, 10)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['page_obj'] = page_obj
    context['paginator'] = paginator
    context['events'] = events
    context['search'] = search
    return render(request, template_name, context)

def details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    template_name = 'events/details.html'
    if not event.public and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.save()
            return redirect('events_details', event.pk)
    else:
        form = CommentForm()
    context = {
        'event': event,
        'comment_form': form,
    }
    return render(request, template_name, context)

@login_required
def create(request):
    template_name = 'events/create.html'
    context = {}
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            next_url = event.get_absolute_url()
            return HttpResponseRedirect(next_url)
    else:
        form = EventForm()
    context['form'] = form
    return render(request, template_name, context)

@login_required
def my(request):
    template_name = 'events/my.html'
    context = {}
    events = Event.objects.filter(user=request.user)
    paginator = Paginator(events, 10)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['page_obj'] = page_obj
    context['paginator'] = paginator
    context['events'] = events
    return render(request, template_name, context)

@login_required
def edit(request, pk):
    template_name = 'events/edit.html'
    event = get_object_or_404(Event, pk=pk,
                              user=request.user)
    context = {}
    context['event'] = event
    if request.method == 'POST':
        form = EventForm(data=request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events_my')
    else:
        form = EventForm(instance=event)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def delete(request, pk):
    template_name = 'events/delete.html'
    event = get_object_or_404(Event, pk=pk,
                              user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('events_my')
    context = {}
    context['event'] = event
    return render(request, template_name, context)

@login_required
def albums(request, pk):
    template_name = 'events/albums.html'
    event = get_object_or_404(Event, pk=pk,
                              user=request.user)
    context = {}
    context['event'] = event
    return render(request, template_name, context)

@login_required
def create_album(request, pk):
    template_name = 'events/create_album.html'
    event = get_object_or_404(Event, pk=pk,
                              user=request.user)
    context = {}
    if request.method == 'POST':
        form = AlbumForm(data=request.POST)
        formset = PhotoFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            album = form.save(commit=False)
            album.event = event
            album.save()
            formset.instance = album
            formset.save()
            return redirect('gallery_album', album.pk)
    else:
        form = AlbumForm()
        formset = PhotoFormset()
    context['event'] = event
    context['form'] = form
    context['formset'] = formset
    return render(request, template_name, context)