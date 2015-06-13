from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from bookmarks.forms import *


def main_page(request):
    return render_to_response('main_page.html', RequestContext(request))


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')  # return to '/' (main page)


def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested user not found.')
    bookmarks = user.bookmark_set.all()
    template = get_template('user_page.html')
    variables = RequestContext(request, {
        'username': username,
        'bookmarks': bookmarks
    })

    output = template.render(variables)
    return HttpResponse(output)


def register_page(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
        )
        return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)