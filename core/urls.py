from django.urls import path

from core.views import ProductsApiView, ProductsCreateApiView

urlpatterns = [
    path('products/', ProductsApiView.as_view()),
    path('products/create/', ProductsCreateApiView.as_view())
]
