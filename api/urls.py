from django.urls import path
from . import views
urlpatterns=[
    path('data/', views.getdata, name='getdata'),
    path('configure/', views.configure_build, name='configure_build'),
    path('llama', views.llama_generate, name='llama'),
    path('index', views.llama_ui, name='ui')
]