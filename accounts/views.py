from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ShopIndividualSignupForm, WorkerSignupForm, CustomLoginForm,ShopProfileEditForm,IndividualProfileEditForm,WorkerProfileEditForm
from .models import CustomUser, ShopOrIndividualProfile, WorkerProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

def shop_individual_signup(request):
    if request.method == "POST":
        form = ShopIndividualSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True 
            user.is_shop_or_individual = True  # Ensure the user is marked correctly
            user.save()

            user_type = form.cleaned_data["user_type"]
            if user_type == "shop":
                ShopOrIndividualProfile.objects.create(
                    user=user,
                    user_type=form.cleaned_data['user_type'],  # Matches models.py
                    shop_name=form.cleaned_data.get('shop_name', ''),  # Matches models.py
                    owner_name=form.cleaned_data.get('owner_name', ''),  # Matches models.py
                    category=form.cleaned_data.get('category', ''),  # Matches models.py
                    description=form.cleaned_data.get('description', ''),  # Matches models.py
                    email=form.cleaned_data['email'],  # Matches models.py
                    contact_number=form.cleaned_data['contact_number'],  # Matches models.py
                    location=form.cleaned_data['location'],  # Matches models.py
                    profile_picture=form.cleaned_data.get('profile_picture', None)  # Matches models.py
                )
            else:
                name = form.cleaned_data.get('owner_name', '')
                owner_name = "" 
                user.Name = name
                user.save()
                ShopOrIndividualProfile.objects.create(
                    user=user,
                    user_type=user_type,  # Only saves user_type, contact, location, and profile picture
                    owner_name=None,
                    Name=name,
                    email=form.cleaned_data["email"],
                    contact_number=form.cleaned_data["contact_number"],
                    location=form.cleaned_data["location"],
                    profile_picture=form.cleaned_data.get("profile_picture", None),
                )
        
            
            return redirect("homepage")
    else:
        form = ShopIndividualSignupForm()
    return render(request, "accounts/shop_individual_signup.html", {"form": form})

def worker_signup(request):
    if request.method == "POST":
        form = WorkerSignupForm(request.POST, request.FILES)  # Include FILES for profile pictures
        if form.is_valid():
            user = form.save(commit=False)
            user.is_worker = True  # Ensure the user is marked correctly
            wname = form.cleaned_data.get('Name', '')
            user.Wname = wname
            user.Name=None
            user.save()
            
            # Create and save the WorkerProfile
            WorkerProfile.objects.create(
                user=user,
                I_am_a=form.cleaned_data['I_am_a'],
                Name=form.cleaned_data['Name'],
                Other_skills=form.cleaned_data.get('Other_skills', ''),  # Optional
                contact_number=form.cleaned_data['contact_number'],
                email=form.cleaned_data['email'],
                experience_in_years=form.cleaned_data['experience_in_years'],
                profile_picture=form.cleaned_data.get('profile_picture', None),  # Optional
                location=form.cleaned_data['location'],
            )
            
            
            return redirect("homepage")
    else:
        form = WorkerSignupForm()
    return render(request, "accounts/worker_signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")  # Change this to your actual homepage/dashboard URL
            else:
                messages.error(request, "Invalid username or password")  

        else:
            messages.error(request, "Invalid username or password")
    else:
        form = CustomLoginForm()

    return render(request, "accounts/login.html", {'form': form})

def user_logout(request):
    logout(request)
    return redirect("homepage")  # Redirect to homepage after logout
def about_view(request):
    return render(request, 'accounts/about.html')
def spt_view(request):
    return render(request, 'accounts/spt.html')
def contact_view(request):
    return render(request, 'accounts/contact.html')
@never_cache
@login_required
def edit_shop_profile(request):
    user = request.user
    try:
        profile = ShopOrIndividualProfile.objects.get(user=user)
        if profile.user_type.lower() != 'shop':
            return redirect('dashboard')  # ❌ Block access if not a Shop
    except ShopOrIndividualProfile.DoesNotExist:
        return redirect('dashboard')  # ❌ Block access if profile doesn't exist

    if request.method == 'POST':
        form = ShopProfileEditForm(request.POST, request.FILES, instance=profile)

        # 🔧 Check if the 'clear' checkbox was checked
        clear_image = request.POST.get('profile_picture-clear')

        if form.is_valid():
            updated_profile = form.save(commit=False)

            # Update fields in CustomUser model
            user.email = form.cleaned_data['email']
            user.contact_number = form.cleaned_data['contact_number']
            user.owner_name = form.cleaned_data['owner_name']
            user.shop_name = form.cleaned_data['shop_name']
            user.description = form.cleaned_data['description']

            # 🔧 Handle clearing or updating the profile picture
            if clear_image:
                user.profile_picture.delete(save=False)
                user.profile_picture = None
            elif form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data['profile_picture']

            user.save()

            # 🔧 Update ShopOrIndividualProfile
            updated_profile.email = form.cleaned_data['email']
            updated_profile.contact_number = form.cleaned_data['contact_number']
            updated_profile.owner_name = form.cleaned_data['owner_name']
            updated_profile.shop_name = form.cleaned_data['shop_name']
            updated_profile.description = form.cleaned_data['description']

            if clear_image:
                updated_profile.profile_picture.delete(save=False)
                updated_profile.profile_picture = None
            elif form.cleaned_data.get('profile_picture'):
                updated_profile.profile_picture = form.cleaned_data['profile_picture']

            updated_profile.user = user
            updated_profile.save()

            return redirect('dashboard')
    else:
        initial_data = {
            'email': user.email,
            'contact_number': user.contact_number,
            'owner_name': user.owner_name,
            'shop_name': user.shop_name,
            'description': user.description,
            'profile_picture': user.profile_picture,
        }
        form = ShopProfileEditForm(instance=profile, initial=initial_data)

    return render(request, 'accounts/edit_shop_profile.html', {'form': form})
@never_cache
@login_required
def edit_individual_profile(request):
    user = request.user
    try:
        profile = ShopOrIndividualProfile.objects.get(user=user, user_type='individual')
    except ShopOrIndividualProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = IndividualProfileEditForm(request.POST, request.FILES, instance=profile)
        clear_image = request.POST.get('profile_picture-clear')

        if form.is_valid():
            updated_profile = form.save(commit=False)

            # Update CustomUser
            user.email = form.cleaned_data['email']
            user.contact_number = form.cleaned_data['contact_number']
            user.Name = form.cleaned_data['Name']

            if clear_image:
                user.profile_picture.delete(save=False)
                user.profile_picture = None
            elif form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data['profile_picture']

            user.save()

            # Update Profile
            updated_profile.email = form.cleaned_data['email']
            updated_profile.contact_number = form.cleaned_data['contact_number']
            updated_profile.Name = form.cleaned_data['Name']

            if clear_image:
                updated_profile.profile_picture.delete(save=False)
                updated_profile.profile_picture = None
            elif form.cleaned_data.get('profile_picture'):
                updated_profile.profile_picture = form.cleaned_data['profile_picture']

            updated_profile.user = user
            updated_profile.save()

            return redirect('dashboard')
    else:
        initial_data = {
            'email': user.email,
            'contact_number': user.contact_number,
            'Name': user.Name,
            'profile_picture': user.profile_picture,
        }
        form = IndividualProfileEditForm(instance=profile, initial=initial_data)

    return render(request, 'accounts/edit_individual_profile.html', {'form': form})
@never_cache
@login_required
def edit_worker_profile(request):
    user = request.user
    try:
        profile = WorkerProfile.objects.get(user=user)
    except WorkerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = WorkerProfileEditForm(request.POST, request.FILES, instance=profile)
        clear_image = request.POST.get('profile_picture-clear')

        if form.is_valid():
            updated_profile = form.save(commit=False)

            # Update CustomUser
            user.Wname = form.cleaned_data['Name']
            user.email = form.cleaned_data['email']
            user.contact_number = form.cleaned_data['contact_number']
            user.experience_in_years = form.cleaned_data['experience_in_years']

            if clear_image:
                user.profile_picture.delete(save=False)
                user.profile_picture = None
            elif form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data['profile_picture']

            user.save()

            # Update WorkerProfile
            updated_profile.Name = form.cleaned_data['Name']
            updated_profile.email = form.cleaned_data['email']
            updated_profile.contact_number = form.cleaned_data['contact_number']
            updated_profile.experience_in_years = form.cleaned_data['experience_in_years']

            if clear_image:
                updated_profile.profile_picture.delete(save=False)
                updated_profile.profile_picture = None
            elif form.cleaned_data.get('profile_picture'):
                updated_profile.profile_picture = form.cleaned_data['profile_picture']

            updated_profile.user = user
            updated_profile.save()

            return redirect('dashboard')
    else:
        initial_data = {
            'Name': user.Wname,
            'email': user.email,
            'contact_number': user.contact_number,
            'experience_in_years': user.experience_in_years,
            'profile_picture': user.profile_picture,
        }
        form = WorkerProfileEditForm(instance=profile, initial=initial_data)

    return render(request, 'accounts/edit_worker_profile.html', {'form': form})