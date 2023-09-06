from django.urls import path
from django.conf import settings
from . import views
from .views import CreatePage, ProductList, ProductPage, CreateBusiness, Creator, Dashboard,  VerifyEmail, ProductDashboard, PasswordResetVerifymail


urlpatterns = [
    path('', views.home, name='home'),
    path('createpage/<str:slug>/', CreatePage.as_view(), name="createpage"),
    path('signup/', Creator.as_view(), name="signup"),
    path('signin/', views.signin, name='signin'),
    path('reclaim_password/<int:pk>/<str:str>/', views.password_reset_update_password, name='reclaim_password'),
    path('reroutedash/<str:pk>/', views.reroutedashboard, name='rrdash'),
    path('createbusiness/<str:pk>/', CreateBusiness.as_view(), name='createbusiness'),
    path('cta/<str:slug>/', views.cta_click, name="cta-click"),
    path('dashboard/<str:slug>/', Dashboard.as_view(), name="dashboard"),
    path('dash/<str:slug>/<str:slugx>/', ProductDashboard.as_view(), name="productdashboard"),
    path('p/<str:slug>/', ProductList.as_view(), name='product_list'),
    path('p/<str:slug>/<str:slugx>/', ProductPage.as_view(), name='product_page'),
    path('payment/<str:slug>/<str:slugx>/', views.processpayment, name='processpayment'),
    path('verifyemail/<int:pk>/', views.verifymail, name='verifymail'),
    path('p/<str:slug>/<str:slugx>/edit/', views.editproduct, name='editproduct'),
    path('p/<str:slug>/<str:slugx>/delete/', views.deleteproduct, name='deleteproduct'),
    path('p/<str:slug>/<str:slugx>/<int:pk>/hidereview/', views.hidereview, name='hidereview'),
    path('dash/<str:slug>/', views.dash, name='dash'),
    path('forgot-password/', PasswordResetVerifymail.as_view(), name="forgotpassword"),
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)