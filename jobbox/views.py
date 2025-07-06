from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser, WorkerProfile, ShopOrIndividualProfile
from django.db.models import Q
from django.views.decorators.cache import never_cache


# Mapping shop categories to relevant professions
worker_professions = {
    "Food/Beverages": ["Cook/Chef", "Waiter"],
    "Electrical/Electronics": ["Electrician", "Maintenance Worker"],
    "Grocery": ["Salesman", "Accountant"],
    "Clothing/Textiles": ["Tailor", "Salesman"],
    "Automobile/Workshop": ["Mechanic", "Driver"],
    "Construction": ["Mason", "Construction Worker"],
}

def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    worker_count = WorkerProfile.objects.count()
    individual_count = ShopOrIndividualProfile.objects.filter(user_type='individual').count()
    shop_count = ShopOrIndividualProfile.objects.filter(user_type='shop').count()

    # You can replace this with real logic later if you have job filling logic
    jobs_filled = 0  

    context = {
        'worker_count': worker_count,
        'individual_count': individual_count,
        'shop_count': shop_count,
        'jobs_filled': jobs_filled,
    }
    return render(request, 'index.html', context)
@never_cache
@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    query = request.GET.get('q')

    # Worker logged in
    if hasattr(user, 'workerprofile'):
        profile = user.workerprofile
        worker_profession = profile.I_am_a
        location = profile.location

        # Reverse lookup: Find categories that need this profession
        matching_categories = [
            category for category, professions in worker_professions.items()
            if worker_profession in professions
        ]
        all_shops = ShopOrIndividualProfile.objects.filter(user_type='shop')
        if query:
            all_shops = all_shops.filter(
                Q(shop_name__icontains=query) |
                Q(category__icontains=query) |
                Q(location__icontains=query)
            )
        group_1 = all_shops.filter(category__in=matching_categories, location=location)
        group_2 = all_shops.filter(category__in=matching_categories).exclude(location=location)
        group_3 = all_shops.exclude(category__in=matching_categories).filter(location=location)
        group_4 = all_shops.exclude(category__in=matching_categories).exclude(location=location)

        shops = list(group_1) + list(group_2) + list(group_3) + list(group_4)


        context['shops'] = shops

    # Shop or Individual logged in
    elif hasattr(user, 'shoporindividualprofile'):
        profile = user.shoporindividualprofile
        category = profile.category
        location = profile.location
        user_type = profile.user_type

        if user_type == 'shop':
            relevant_professions = worker_professions.get(category, [])
            all_workers = WorkerProfile.objects.all()

            if query:
                all_workers = all_workers.filter(
                    Q(Name__icontains=query) |
                    Q(I_am_a__icontains=query) |
                    Q(location__icontains=query)
                )

        # Sort workers by relevance
            group_1 = all_workers.filter(I_am_a__in=relevant_professions, location=location)
            group_2 = all_workers.filter(I_am_a__in=relevant_professions).exclude(location=location)
            group_3 = all_workers.exclude(I_am_a__in=relevant_professions).filter(location=location)
            group_4 = all_workers.exclude(I_am_a__in=relevant_professions).exclude(location=location)

        # Combine into one ordered list
            workers = list(group_1) + list(group_2) + list(group_3) + list(group_4)
            context['workers'] = workers
        
        elif user_type == 'individual':
            household_workers = ["Security Guard", "Maidservant", "Gardener", "Driver", "Baby Sitter"]
            all_workers = WorkerProfile.objects.all()

            if query:
                all_workers = all_workers.filter(
                    Q(Name__icontains=query) |
                    Q(I_am_a__icontains=query) |
                    Q(location__icontains=query)
                )

            group_1 = all_workers.filter(I_am_a__in=household_workers, location=location)
            group_2 = all_workers.filter(I_am_a__in=household_workers).exclude(location=location)
            group_3 = all_workers.exclude(I_am_a__in=household_workers).filter(location=location)
            group_4 = all_workers.exclude(I_am_a__in=household_workers).exclude(location=location)

            workers = list(group_1) + list(group_2) + list(group_3) + list(group_4)
            context['workers'] = workers

    return render(request, 'dashboard.html', context)
