from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import StoreView, ProductView, ProductAnalytics, StoreAnalytics

urlpatterns = [
    path('stores/', StoreView.as_view()),
    path('products/', ProductView.as_view()),
    path('analytics/products/', ProductAnalytics.as_view()),
    path('analytics/stores/', StoreAnalytics.as_view()),
    path('auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls'))   
]