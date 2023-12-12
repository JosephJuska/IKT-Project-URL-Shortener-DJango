from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name="index"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_page, name="logout"),
    path('verification/<str:token>/', views.verification_page, name="verification"),
    path('account/', views.account_page, name="account"),
    path('short/<str:short_url>', views.short_page, name="short"),
    path('redirect/<str:short_url>', views.redirect_page, name="redirect")
]
