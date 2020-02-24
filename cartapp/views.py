from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainapp.models import Record
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse


@require_POST
def cart_add(request, record_id):
    cart = Cart(request)
    record = get_object_or_404(Record, id=record_id)
    form = CartAddProductForm(request.POST)
    if request.method == "POST":
        cart.add(record=record)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(record=record,
                 quantity=cd['quantity'], update_quantity=cd['update'])
    return HttpResponse(status=204)


def cart_remove(request, record_id):
    cart = Cart(request)
    record = get_object_or_404(Record, id=record_id)
    cart.remove(record)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cartapp/cartdetail.html', {'cart': cart})
