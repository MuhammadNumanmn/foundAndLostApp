from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('addItem/', views.addItem, name='addItem'),
    path('item/<str:pk>/', views.itemDetails, name='item'),
    path('updateItem/<str:pk>/', views.updateItem, name='updateItem'),
    path('deleteItem/<str:pk>/', views.deleteItem, name='deleteItem'),
    path('lostItems/', views.lostItems, name='lostItems'),
    path('foundItems/', views.foundItems, name='foundItems'),
    path('donatedItems/', views.donatedItems, name='donatedItems'),
]
