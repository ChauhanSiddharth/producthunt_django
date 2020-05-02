from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from accounts.models import UserProfile, FriendModel
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
				user = User.objects.create_user(request.POST['username'],password=request.POST['password'], email=request.POST['email'])
				auth.login(request,user)
				return redirect('addinfo')
		else:
			return render(request,'accounts/signup.html',{'error':'password must match'})
	else:
		return render(request, 'accounts/signup.html')

@login_required
def addInfo(request):
	user = auth.authenticate(username=request.user.username)
	if request.method=='POST':
		if request.POST['firstname']:
			firstname = request.POST.get('firstname')
			lastname = request.POST.get('lastname')
			dob = request.POST.get('dob')
			address = request.POST.get('address')
			bio = request.POST.get('bio')
			profession = request.POST.get('profession')
			userData = UserProfile(user = request.user, firstname=firstname, lastname=lastname, dob=dob,address=address,bio=bio, profession=profession)
			userData.save()
			return redirect('profile')
	else:
		return render(request, 'accounts/submit-info.html')

@login_required
def myprofile(request):
	user_data = UserProfile.objects.filter(user=request.user)
	posts = Product.objects.filter(hunter=request.user)
	for data in user_data:
		name = data
	friendReq = FriendModel.objects.filter(member=name)
	if not friendReq:
		friendReq = FriendModel.objects.filter(friend=request.user)
	return render(request, 'products/profile.html',{'userdata':user_data,'posts':posts,'friend_requests':friendReq})

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
		if request.POST.get('title') or request.POST.get('url') or request.POST.get('body') or request.FILES['image'] or request.FILES['icon']:
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

def viewUser(request, username):
	try:
		result = User.objects.filter(username=username)
	except:
		return
	for data in result:
		username = data.id
	friend_check = False
	if request.POST:
		getUser = UserProfile.objects.filter(user=request.POST.get('member'))
		getFriend = User.objects.filter(username=request.POST.get('friend'))
		for i in getFriend:
			friendID = i
		for g in getUser:
			userID = g
		sendReq = FriendModel(member=userID, friend=friendID)
		sendReq.save()
	for fm in FriendModel.objects.all():
		print(fm.member,fm.friend)
		for up in UserProfile.objects.filter(user=request.user):
			for fup in UserProfile.objects.filter(user=username):
				print('fup-->',fm.member,fup.firstname)
				print('user-->',fm.friend,request.user)
				if fm.member.firstname == up.firstname and fm.friend == fup.user:
					friend_check = True
				if fm.member.firstname == fup.firstname and fm.friend == request.user:
					friend_check = True
	data = UserProfile.objects.filter(user=username)
	posts = Product.objects.filter(hunter=username)
	return render(request, 'accounts/user.html', {'userdata':data, 'posts':posts,'is_friend':friend_check})

@login_required
def accountSettings(request):
	user_data = UserProfile.objects.filter(user=request.user)
	if request.POST:
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		dob = request.POST.get('dob')
		address = request.POST.get('address')
		profession = request.POST.get('profession')
		bio = request.POST.get('bio')
		UserProfile.objects.filter(user=request.user).update(firstname=firstname)
		UserProfile.objects.filter(user=request.user).update(lastname=lastname)
		UserProfile.objects.filter(user=request.user).update(dob=dob)
		UserProfile.objects.filter(user=request.user).update(address=address)
		UserProfile.objects.filter(user=request.user).update(profession=profession)
		UserProfile.objects.filter(user=request.user).update(bio=bio)
		user_data = UserProfile.objects.filter(user=request.user)
		return render(request, 'accounts/updateaccount.html', {'userdata': user_data})
	else:
		return render(request, 'accounts/updateaccount.html', {'userdata': user_data})

@login_required
def notification(request):
	user_data = UserProfile.objects.filter(user=request.user)
	friendReq = FriendModel.objects.filter(friend=request.user)
	if not friendReq:
		for data in user_data:
			name = data
		friendReq = FriendModel.objects.filter(member=name)
	if request.POST:
		FriendModel.objects.filter(member=request.POST.get('member')).update(added=True)
	return render(request, 'accounts/notification.html', {'userdata': user_data,'friend_requests':friendReq})


def searchPost(request):
	if request.method=='POST':
		searchText = request.POST['searchPost']
		posts = Product.objects.filter(title__icontains=searchText)
		member = User.objects.filter(username=searchText)
		if posts or member:
			return render(request, 'products/search.html',{'searchResult':posts,'message':'Found','member':member})
		else:
			return render(request, 'products/search.html',{'message':"Not Found"})

def logout(request):
	if request.method=='POST':
		auth.logout(request)
		return redirect('home')
	# TODO dont forget
	return render(request, 'accounts/home.html')
