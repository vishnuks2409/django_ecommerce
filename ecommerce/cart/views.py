from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Account,Order_table
from django.http import HttpResponse

# Cart view

@login_required
def add_to_cart(request,pk):
    p=Product.objects.get(id=pk)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    return cart_view(request)


@login_required
def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price

    return render(request,'cart.html',{'cart':cart,'total':total})

def cart_decrement(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if(cart.quantity>1):

            cart.quantity -=1
            cart.save()
            p.stock +=1
            p.save()
        else:
            cart.delete()
            p.stock +=1
            p.save()

    except:
        pass
    return cart_view(request)

def remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock +=cart.quantity
        p.save()
    except:
        pass
    return cart_view(request)

@login_required
def place_order(request):
    if (request.method =="POST"):
        phone=request.POST['phone']
        address = request.POST['address']
        account = request.POST['account']

        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total=total+i.quantity*i.product.price
        try:
            ac=Account.objects.get(acctnum=account)
            if(ac.amount >= total):
                ac.amount=ac.amount-total
                ac.save()
                for i in c:
                    o=Order_table.objects.create(user=u,product=i.product,address=address,phone=phone,no_of_items=i.quantity,order_status="Paid")
                    o.save()
                c.delete()
                msg="Order Placed Successfully"
                return render(request,'order_detail.html',{'msg':msg})
            else:
                msg = "Insufficient balance.can't place order"
                return render(request, 'order_detail.html', {'msg': msg})

        except:
            pass

    return render(request,'orderform.html')

@login_required
def orderview(request):
    u=request.user
    customer=Order_table.objects.filter(user=u)

    return render(request,'orderview.html',{'customer':customer,'u':u.username})