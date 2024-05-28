# contacts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import ContactForm, UserRegistrationForm
from django.contrib import messages
from django.db.models import Q
from .forms import ContactSearchForm


def home(request):
    return redirect('contact_list')


@login_required
def contact_list(request):
    contacts = Contact.objects.all().order_by('name')  # 按名字排序
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})


@login_required
def edit_contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)

    if request.method == 'POST':
        contact.name = request.POST.get('name')
        contact.phone_number = request.POST.get('phone_number')
        contact.email = request.POST.get('email')
        contact.save()
        messages.success(request, 'Contact updated successfully.')
        return redirect('contact_list')

    return render(request, 'contacts/edit_contact_detail.html', {'contact': contact})
@login_required
def search_results(request):
    if request.method == 'GET':
        form = ContactSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # 在数据库中执行搜索
            results = Contact.objects.filter(name__icontains=query) | \
                      Contact.objects.filter(phone_number__icontains=query) | \
                      Contact.objects.filter(email__icontains=query)
            return render(request, 'contacts/search_results.html', {'results': results, 'query': query})
    else:
        form = ContactSearchForm()
    return render(request, 'contacts/search_results.html', {'form': form})

@login_required
def delete_contact(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    # 处理删除联系人的逻辑，这里只是一个简单的示例
    contact.delete()
    messages.success(request, 'Contact deleted successfully.')
    return redirect('contact_list')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('contact_list')
        else:
            return render(request, 'contacts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'contacts/login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'contacts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
