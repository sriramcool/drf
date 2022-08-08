from django.urls import  path
from . import views

urlpatterns = [
    path('', views.ProductCreateAPIView.as_view()),
    path('all/', views.ProductListAPIView.as_view()),
    path('viewcreate/', views.ProductListCreateApiView.as_view(), name="viewcreate"),
    path('<str:title>/', views.ProductDetailAPIView.as_view(), name="product-detail"), # keyword argument "title(lookup field)" should be passed
    path('api/<int:pk>/', views.api),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
]
