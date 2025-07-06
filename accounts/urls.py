from django.urls import path
from .views import worker_signup, shop_individual_signup, user_login, user_logout, about_view,spt_view,contact_view,edit_shop_profile,edit_individual_profile,edit_worker_profile

urlpatterns = [
    path('signup/worker/', worker_signup, name='worker_signup'),
    path('signup/shop_individual/', shop_individual_signup, name='shop_individual_signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('about/', about_view, name='about'),
    path('spt/', spt_view, name='spt'),
    path('contact/', contact_view, name='contact'),
    path('edit-shop-profile/', edit_shop_profile, name='edit_shop_profile'),
    path('edit_individual_profile/',edit_individual_profile, name='edit_individual_profile'),
    path("edit_worker_profile/", edit_worker_profile, name="edit_worker_profile"),
]
