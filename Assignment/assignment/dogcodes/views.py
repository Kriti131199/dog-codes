from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, FilterForm, ContactForm
from .models import ResponseList, ResponseCode
import re



DOG_URL = "https://http.dog/{}.jpg"


ALL_CODES = [str(code) for code in range(100, 600)]


def match_codes(pattern):
    regex = pattern.replace('x', r'\\d')
    return [code for code in ALL_CODES if re.match(regex, code)]


def home_view(request):
    from .forms import ContactForm  # if not already imported
    contact_form = ContactForm()
    message_sent = False

    if request.method == 'POST' and 'name' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Optional: save or email the form data
            print(contact_form.cleaned_data)  # Debug/demo
            message_sent = True
            contact_form = ContactForm()  # Clear form after submission

    return render(request, 'dogcodes/base.html', {
        'contact_form': contact_form,
        'message_sent': message_sent
    })

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search')
    else:
        form = SignupForm()
    return render(request, 'dogcodes/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('search')
    else:
        form = AuthenticationForm()
    return render(request, 'dogcodes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

#@login_required(login_url='/login/')
def search_view(request):
    if not request.user.is_authenticated:
        return render(request, 'dogcodes/search.html', {
            'error_message': 'Please log in to use the search feature.'
        })
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            pattern = form.cleaned_data['filter_input']
            name = form.cleaned_data['list_name']
            codes = match_codes(pattern)
            response_list = ResponseList.objects.create(user=request.user, name=name)
            for code in codes:
                ResponseCode.objects.create(
                    list=response_list,
                    code=code,
                    image_url=DOG_URL.format(code)
                )
            return redirect('lists')
    else:
        form = FilterForm()
    return render(request, 'dogcodes/search.html', {'form': form})

#@login_required(login_url='/login/')
def lists_view(request):
    if not request.user.is_authenticated:
        return render(request, 'dogcodes/lists.html', {
            'error_message': 'Please log in to view your lists.'
        })
    lists = ResponseList.objects.filter(user=request.user)
    return render(request, 'dogcodes/lists.html', {'lists': lists})

@login_required(login_url='/login/')
def list_details_view(request, list_id):
    response_list = get_object_or_404(ResponseList, id=list_id, user=request.user)
    return render(request, 'dogcodes/list-details.html', {'list': response_list})

@login_required(login_url='/login/')
def delete_list_view(request, list_id):
    response_list = get_object_or_404(ResponseList, id=list_id, user=request.user)
    response_list.delete()
    return redirect('lists')

@login_required(login_url='/login/')
def edit_list_view(request, list_id):
    response_list = get_object_or_404(ResponseList, id=list_id, user=request.user)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            response_list.name = new_name
            response_list.save()
            return redirect('lists')
    return render(request, 'dogcodes/edit-list.html', {'list': response_list})
