from django.urls import path
from django.conf import settings
from . import views
from .views import CreatePage, ProductList, ProductPage, CreateBusiness, Creator


urlpatterns = [
    path('', views.home, name='home'),
    path('createpage/<str:slug>/', CreatePage.as_view(), name="createpage"),
    path('signup/', Creator.as_view(), name="signup"),
    path('createbusiness/<str:pk>/', CreateBusiness.as_view(), name='createbusiness'),
    path('p/<str:slug>/', ProductList.as_view(), name='product_list'),
    path('p/<str:slug>/<str:slugx>/', ProductPage.as_view(), name='product_page'),
    path('payment/<str:slug>/<str:slugx>/', views.processpayment, name='processpayment'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)