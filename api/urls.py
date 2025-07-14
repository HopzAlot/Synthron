from django.urls import path
from .views import ConfigureBuildView, LlamaGenerateView, llama_ui, RegisterView,LoginView,LogoutView,RefreshTokenView, BuildHistory
urlpatterns = [
    path('configure/', ConfigureBuildView.as_view(), name='configure_build'),
    path('llama/', LlamaGenerateView.as_view(), name='llama'),
    path('index/', llama_ui, name='ui'),
     path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('history/', BuildHistory.as_view(), name='history')
]
