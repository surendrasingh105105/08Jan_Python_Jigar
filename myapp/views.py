from django.shortcuts import render,redirect
from .models import Contact,User,Product,Wishlist,Cart,Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
# Create your views here.

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)


def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    try:
       
        amount = int(request.POST['amount'])
        
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user,amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()
    carts=Cart.objects.filter(user=user)
    for i in carts:
    	i.payment_status="paid"
    	i.save()

    carts=Cart.objects.filter(user=user,payment_status="pending")
    request.session['cart_count']=len(carts)
    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)


def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def cart(request):
	return render(request,'cart.html')

def shop(request):
	products=Product.objects.all()
	all=len(products)
	men=len(Product.objects.filter(product_collection="men"))
	women=len(Product.objects.filter(product_collection="women"))
	kids=len(Product.objects.filter(product_collection="kids"))
	return render(request,'shop.html',{'all':all,'products':products,'men':men,'women':women,'kids':kids})

def color_red(request):
	products=Product.objects.filter(product_color="red")
	all=len(Product.objects.all())
	men=len(Product.objects.filter(product_collection="men"))
	women=len(Product.objects.filter(product_collection="women"))
	kids=len(Product.objects.filter(product_collection="kids"))
	return render(request,'shop.html',{'all':all,'products':products,'men':men,'women':women,'kids':kids})

def color_blue(request):
	products=Product.objects.filter(product_color="blue")
	all=len(Product.objects.all())
	men=len(Product.objects.filter(product_collection="men"))
	women=len(Product.objects.filter(product_collection="women"))
	kids=len(Product.objects.filter(product_collection="kids"))
	return render(request,'shop.html',{'all':all,'products':products,'men':men,'women':women,'kids':kids})

def collection_men(request):
	products=Product.objects.all()
	all=len(products)
	products=Product.objects.filter(product_collection="men")
	men=len(Product.objects.filter(product_collection="men"))
	women=len(Product.objects.filter(product_collection="women"))
	kids=len(Product.objects.filter(product_collection="kids"))
	return render(request,'shop.html',{'all':all,'products':products,'men':men,'women':women,'kids':kids})

def collection_women(request):
	products=Product.objects.all()
	all=len(products)
	products=Product.objects.filter(product_collection="women")
	men=len(Product.objects.filter(product_collection="men"))
	women=len(Product.objects.filter(product_collection="women"))
	kids=len(Product.objects.filter(product_collection="kids"))
	return render(request,'shop.html',{'all':all,'products':products,'men':men,'women':women,'kids':kids})

def collection_kids(request):
	products=Product.objects.all()
	all=len(products)
	products=Product.objects.filter(product_collection="kids")
	men=len(Product.objects.filter(product_collection="men"))
	women=len(Product.objects.filter(product_collection="women"))
	kids=len(Product.objects.filter(product_collection="kids"))
	return render(request,'shop.html',{'all':all,'products':products,'men':men,'women':women,'kids':kids})	

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				subject=request.POST['subject'],
				message=request.POST['message'],
			)
		msg="Contact Saved Successfully"
		return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def shop_single(request):
	return render(request,'shop-single.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						usertype=request.POST['usertype'],
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
					)
				msg="User SignUp Successfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password']
				)
			if user.usertype=="user":
				request.session['email']=user.email
				request.session['fname']=user.fname
				wishlists=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlists)
				carts=Cart.objects.filter(user=user)
				request.session['cart_count']=len(carts)
				return render(request,'index.html')
			elif user.usertype=="seller":
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'seller_index.html')
			else:
				pass

		except:
			msg="Email or Password Is Incorrect"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except Exception as e:
		print(e)
		return render(request,'login.html')

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	print(user.usertype)
	if user.usertype=="user":
		if request.method=="POST":
			
			if user.password==request.POST['old_password']:
				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					return redirect('logout')
				else:
					msg="New & Confirm New Password Does Not Matched"
					return render(request,'change_password.html',{'msg':msg})
			else:
				msg="Old Password Does Not Matched"
				return render(request,'change_password.html',{'msg':msg})
		else:
			return render(request,'change_password.html')
	elif user.usertype=="seller":
		if request.method=="POST":
			if user.password==request.POST['old_password']:
				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					print("Password Updated")
					return redirect('logout')
				else:
					msg="New & Confirm New Password Does Not Matched"
					return render(request,'seller_change_password.html',{'msg':msg})
			else:
				msg="Old Password Does Not Matched"
				return render(request,'seller_change_password.html',{'msg':msg})
		else:
			return render(request,'seller_change_password.html')
	else:
		pass

def seller_index(request):
	return render(request,'seller_index.html')

def seller_add_product(request):
	if request.method=="POST":
		product_seller=User.objects.get(email=request.session['email'])
		Product.objects.create(
				product_seller=product_seller,
				product_collection=request.POST['product_collection'],
				product_category=request.POST['product_category'],
				product_size=request.POST['product_size'],
				product_color=request.POST['product_color'],
				product_price=request.POST['product_price'],
				product_desc=request.POST['product_desc'],
				product_image=request.FILES['product_image']
			)
		msg="Product Added Successfully"
		return render(request,'seller_add_product.html',{'msg':msg})
	else:
		return render(request,'seller_add_product.html')

def seller_view_product(request):
	product_seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(product_seller=product_seller)
	return render(request,'seller_view_product.html',{'products':products})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_collection=request.POST['product_collection']
		product.product_category=request.POST['product_category']
		product.product_size=request.POST['product_size']
		product.product_color=request.POST['product_color']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		return render(request,'seller_edit_product.html',{'product':product})
	else:
		return render(request,'seller_edit_product.html',{'product':product})

def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller_view_product')

def product_detail(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass
	try:
		Cart.objects.get(user=user,product=product,payment_status="pending")
		cart_flag=True
	except:
		pass
	return render(request,'product_detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(
			user=user,
			product=product
		)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
			user=user,
			product=product,
			product_price=product.product_price,
			product_qty=1,
			total_price=product.product_price
		)
	return redirect('cart')

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status="pending")
	for i in carts:
		net_price=net_price+i.total_price

	request.session['cart_count']=len(carts)
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product,payment_status="pending")
	cart.delete()
	return redirect('cart')

def change_qty(request):
	print("change qty called")
	cart=Cart.objects.get(pk=request.POST['cid'])
	product_qty=int(request.POST['product_qty'])
	print(" Product_qty : ",product_qty)
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')

def myorders(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status="paid")
	return render(request,'myorders.html',{'carts':carts})
