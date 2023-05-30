from django.urls import path
from . import views
urlpatterns = [
  path('', views.index, name='index'),
  path('createAccount', views.createAccount, name='createAccount'),
  path('queryAccounts', views.queryAccounts, name='queryAccounts')
 ]