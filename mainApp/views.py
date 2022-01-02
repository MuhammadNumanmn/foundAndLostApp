from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, CreateItemForm
from django.contrib import messages
from .models import User, ItemDetail, Message
from datetime import datetime, timezone
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    page = 'Lost & Found App'
    items = []
    searchCount = 0
    lostItems = ItemDetail.objects.filter(item_status='Lost')[:4]
    foundItems = ItemDetail.objects.filter(item_status='Found')[:4]
    donatedItems = ItemDetail.objects.filter(item_status='Donated')[:4]

    allItems = ItemDetail.objects.all()
    for item in allItems:
        now = datetime.now(timezone.utc)
        delta = now - item.timeAdded
        # hour = (delta.total_seconds()/60)/60
        days = delta.days
        if days > 7:
            ItemDetail.objects.filter(id=item.id).update(item_status='Donated')

    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            items = ItemDetail.objects.filter(Q(name__icontains=search) | Q(location__icontains=search)
                                          | Q(description__icontains=search))
            searchCount = items.count()

    context = {
        'lostItems': lostItems,
        'foundItems': foundItems,
        'donatedItems': donatedItems,
        'page': page,
        'items': items,
        'searchCount': searchCount,
        'lostCount': lostItems.count(),
        'foundCount': foundItems.count(),
        'donatedCount': donatedItems.count()
    }
    return render(request, 'mainApp/index.html', context)


def loginUser(request):
    page = 'Login User'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email or password is incorrect. ')

    context = {
        'page': page
    }
    return render(request, 'mainApp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def signup(request):
    page = 'Sign Up User'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong, please try again.')

    context = {
        'form': form,
        'page': page
    }
    return render(request, 'mainApp/signup.html', context)


@login_required(login_url='login')
def addItem(request):
    page = 'Add an Item'
    form = CreateItemForm()
    if request.method == 'POST':
        form = CreateItemForm(request.POST, request.FILES)
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        item_status = request.POST.get('item_status')
        dateFL = request.POST.get('dateFL')
        image = request.FILES.get('image')

        item = ItemDetail.objects.create(
            owner=request.user,
            name=name,
            location=location,
            item_status=item_status,
            description=description,
            dateFL=dateFL,
            image=image
        )
        item.save()
        messages.success(request, 'Item saved successfully')
        return redirect('index')

    context = {
        'form': form,
        'page': page
    }
    return render(request, 'mainApp/addItem.html', context)


def itemDetails(request, pk):
    page = 'Item Details'
    item = ItemDetail.objects.get(id=pk)
    item_messages = item.message_set.all().order_by('-created')[:4]
    total_messages = item.message_set.count()

    if request.user.is_authenticated:
        if request.method == 'POST':
            Message.objects.create(
                user=request.user,
                item=item,
                body=request.POST.get('message')
            )
            return redirect('item', pk)
    else:
        messages.warning(request, 'Please login first')
        return redirect('login')

    context = {
        'item': item,
        'item_messages': item_messages,
        'total_messages': total_messages,
        'page': page
    }
    return render(request, 'mainApp/singleItem.html', context)


def updateItem(request, pk):
    page = 'Update an Item'
    item = ItemDetail.objects.get(id=pk)
    form = CreateItemForm(instance=item)

    if request.method == 'POST':
        form = CreateItemForm(request.POST, request.FILES, instance=item)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('item', pk)

    context = {
        'form': form,
        'page': page
    }
    return render(request, 'mainApp/addItem.html', context)


def deleteItem(request, pk):
    page = 'Delete an Item'
    item = ItemDetail.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('index')

    context = {
        'obj': item,
        'page': page
    }
    return render(request, 'mainApp/delete.html', context)


def lostItems(request):
    itemsCount = ItemDetail.objects.filter(item_status='Lost').count
    p = Paginator(ItemDetail.objects.filter(item_status='Lost'), 8)
    page = request.GET.get('page')
    items = p.get_page(page)

    page = 'Lost Items'
    context = {
        'items': items,
        'page': page,
        'itemsCount': itemsCount
    }
    return render(request, 'mainApp/items.html', context)


def foundItems(request):
    itemsCount = ItemDetail.objects.filter(item_status='Found').count()

    p = Paginator(ItemDetail.objects.filter(item_status='Found'), 8)
    page = request.GET.get('page')
    items = p.get_page(page)

    page = 'Found Items'
    context = {
        'items': items,
        'page': page,
        'itemsCount': itemsCount
    }
    return render(request, 'mainApp/items.html', context)


def donatedItems(request):
    itemsCount = ItemDetail.objects.filter(item_status='Donated').count
    p = Paginator(ItemDetail.objects.filter(item_status='Donated'), 8)
    page = request.GET.get('page')
    items = p.get_page(page)

    page = 'Donated Items'
    context = {
        'items': items,
        'page': page,
        'itemsCount': itemsCount
    }
    return render(request, 'mainApp/items.html', context)
