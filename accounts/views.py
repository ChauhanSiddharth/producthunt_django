from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from products.models import Product
# Create your views here.

def login(request):
	if request.method=='POST':
		user = auth.authenticate(username= request.POST['username'],password = request.POST['password'])
		if user is not None:
			auth.login(request,user)
			return redirect('home')
		else:
			return render(request, 'accounts/login.html',{'error':'username or password is incorrect'})
	else:
		return render(request, 'accounts/login.html')

def signup(request):
	if request.method=='POST':
		if request.POST['password']== request.POST['cpassword']:
			try:
				user = User.objects.get(username = request.POST['username'])
				return render(request,'accounts/signup.html',{'error':'Your username is taken'})
			except User.DoesNotExist:
				user = User.objects.create_user(request.POST['username'],password=request.POST['password'])
				auth.login(request,user)
				return redirect('home')
		else:
			return render(request,'accounts/signup.html',{'error':'password must match'})
		#User
	else:
		return render(request, 'accounts/signup.html')

@login_required
def myprofile(request):
	user = auth.authenticate(username=request.user.username)
	user_data = User.objects.filter(username=request.user)
	posts = Product.objects.filter(hunter=request.user)
	return render(request, 'products/profile.html',{'userdata':user_data,'posts':posts})

@login_required
def deletePost(request,product_id):
	user = auth.authenticate(username=request.user.username)
	user_data = User.objects.filter(username=request.user)
	posts = Product.objects.filter(pk=product_id).delete()
	return redirect('/accounts/profile/')

@login_required
def editPost(request, product_id):
	user = auth.authenticate(username=request.user.username)
	user_data = User.objects.filter(username=request.user)
	if request.POST:
		if request.POST.get('title') or request.POST.get('url') or request.POST.get('body') or request.FILES['image']:
			title = request.POST.get('title')
			url = request.POST.get('url')
			body = request.POST.get('body')
			if request.FILES:
				product = Product.objects.filter(pk=product_id)
				product.image = request.FILES['image']
				product.icon = request.FILES['icon']
				product.save()
			Product.objects.filter(pk=product_id).update(title = title)
			Product.objects.filter(pk=product_id).update(url = url)
			Product.objects.filter(pk=product_id).update(body = body)
			return redirect('/accounts/profile/')


def searchPost(request):
	if request.method=='POST':
		searchText = request.POST['searchPost']
		posts = Product.objects.filter(title__icontains=searchText)

		if posts:
			return render(request, 'products/search.html',{'searchResult':posts,'message':'Found'})
		else:
			return render(request, 'products/search.html',{'message':"Not Found"})

def logout(request):
	if request.method=='POST':
		auth.logout(request)
		return redirect('home')
	# TODO dont forget
	return render(request, 'accounts/home.html')
