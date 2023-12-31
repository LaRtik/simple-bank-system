from django.urls import path
from accounts import views
from bank_account.views import AboutUsView

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
	path('register/telegram', views.sign_up_telegram, name='register_telegram'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
	path('await_confirm/', views.AwaitConfirm.as_view(), name='await_confirm')
]