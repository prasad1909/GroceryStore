from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, UpdateOrder
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def index(request):
    all_products = Product.objects.all()
    categories = {prod.category for prod in all_products}
    products = []
    for category in categories:
        product = Product.objects.filter(category=category)
        n = len(product)
        if n % 4 == 0:
            number_of_slides = n//4
        else:
            number_of_slides = n//4 + 1
        products.append([product, range(1, number_of_slides), number_of_slides])

    params = {'allProducts': products}

    return render(request, "shop/home.html", params)


@login_required(login_url='/login')
def about(request):
    return render(request, "shop/about.html")


@login_required(login_url='/login')
def contact(request):
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    description = request.POST.get('description', '')
    contact = Contact(name=name, email=email, phone=phone, description=description)
    contact.save()
    return render(request, "shop/contact.html")


@login_required(login_url='/login')
def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = UpdateOrder.objects.filter(order_id=order_id)
                itemList = order[0].items
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.time})
                    response = json.dumps([updates, itemList], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, "shop/tracker.html")


@login_required(login_url='/login')
def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, "shop/productView.html", {'product': product[0]})


@login_required(login_url='/login')
def checkOut(request):
    if request.method == "POST":
        items = request.POST.get('items', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get("address2", '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = UpdateOrder(order_id=order.order_id, update_desc="Order Placed Successfully")
        update.save()
        check = True
        order_id = order.order_id
        return render(request, "shop/checkout.html", {'check': check, 'order_id': order_id})
    return render(request, "shop/checkout.html")


@login_required(login_url='/login')
def search(request):
    return render(request, "shop/search.html")


@login_required(login_url='/login')
def smartphone(request):
    return render(request, "shop/smartphone.html")
