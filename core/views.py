from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_object_or_404
from django.urls import reverse
import random
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template import loader, Template
from .models import Business, Product, Product_Media, Product_review
from django.template.defaultfilters import slugify 
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator 
# Create your views here.


def home(request):

    return render(request, 'dtox.html')



class CreatePage(View):
    template_name = 'create_page.html'
    viewers_choice = 'templates/home.html'

    

    def get(self, request, slug):
        biz = Business.objects.get(slug=slug)

        context = {'choice': CreatePage.viewers_choice, 'biz':biz}
        return render(request, CreatePage.template_name, context)
    
    def post(self, request, slug):
        biz = Business.objects.get(slug=slug)

        if request.method == 'POST':
            images = request.POST.getlist('images')
            image_list = []

            product = Product.objects.create(
                product_name = request.POST['product_name'],
                product_description = request.POST['product_description'],
                product_price = request.POST['product_price'],
                product_payment_link = request.POST['product_payment_link'],
                business = biz,
                slug = slugify(request.POST['product_name']),
            )
            
            for image in images:
                media = Product_Media.objects.create(
                    product_image = image,
                    video = request.POST['video'],
                    product = product
                )
                product.save()
                media.save()

            my_view = ProductPage()
            return my_view.get(request, biz.slug, product.slug)
    

def product_list(request, slug):
    biz = Business.objects.get(slug=slug)

    context = {'biz':biz}
    return render(request, 'shop.html', context)

class ProductList(View):
    template_name = 'product-details.html'
    items_per_page = 12
    # text = 'SHOWING 1-8 0F 25'

    def get(self, request, slug):
        biz = Business.objects.get(slug=slug)
        products = Product.objects.filter(business=biz)
        # productz = Product.objects.get(business=biz)
        product_count = products.count()
        # product_review = Product_review.objects.filter(product=productz)
        text = 'SHOWING ALL'
        if product_count > 12:
            text = 'SHOWING 1-12 0F ' + str(product_count)

        product_rating = Product_review.objects.filter(product__business=biz)
        total_sum = sum(obj.rating for obj in product_rating)
        total_count = product_rating.count()
        if total_count > 0:
            average = total_sum / total_count
        else:
            average = 0 
        # Create a Paginator object
        paginator = Paginator(products, self.items_per_page)

        # Get the current page number from the request
        page_number = request.GET.get('page')

        # Get the Page object for the current page
        page_obj = paginator.get_page(page_number)
        # product_media = products.product_media_set.all()

        context = {'biz':biz, 'products':products, 'page':page_obj, 'text':text, 'average':ProductPage.average}
        return render(request, 'shop.html', context)
    
class ProductPage(View):
    template_name = 'product-details.html'

    average = 1
    def get(self, request, slug, slugx):
        biz = Business.objects.get(slug=slug)
        productx = Product.objects.get(slug=slugx)
        product_media = Product_Media.objects.filter(product=productx)
        review = Product_review.objects.filter(product=productx)

        review_text = str(review.count()) + ' Reviews'
        product_rating = Product_review.objects.filter(product=productx)
        total_sum = sum(obj.rating for obj in product_rating)
        total_count = product_rating.count()
        if total_count > 0:
           ProductPage.average = total_sum / total_count
        else:
            ProductPage.average = 0 

        context = {'biz':biz,'product':productx,'product_media':product_media, 'review':review, 
                   'review_text':review_text, 'average':ProductPage.average}
        return render(request, 'product-details.html', context)
    def post(self, request, slug, slugx):
        biz = Business.objects.get(slug=slug)
        productx = Product.objects.get(slug=slugx)

        if request.method == 'POST':
            review = Product_review.objects.create(
                creator = request.POST['review_creator'],
                body = request.POST['review_body'],
                product = productx,
                rating = request.POST['review_rating']
            )
            review.save()
        my_view = ProductPage()
        return my_view.get(request, biz.slug, productx.slug)


class CreateBusiness(View):
    template_name = 'createbusiness.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)

        return render(request, CreateBusiness.template_name)
    def post(self, request, slug):
        return render(request, CreateBusiness.template_name)
    
def processpayment(request, slug, slugx):
    biz = Business.objects.get(slug=slug)
    productx = Product.objects.get(slug=slugx)
    if request.method == 'POST':
        images = request.POST.getlist('images')
        image_list = []

        product = Product.objects.create(
            product_name = request.POST['product_name'],
            product_description = request.POST['product_description'],
            product_price = request.POST['product_price'],
            product_payment_link = request.POST['product_payment_link'],
            business = biz,
            slug = slugify(request.POST['product_name']),
        )
        
        for image in images:
            media = Product_Media.objects.create(
                product_image = image,
                video = request.POST['video'],
                product = product
            )
            product.save()
            media.save()

        
        return redirect(ProductPage, biz, product.slug)
    
    context = {'biz':biz, 'product':productx}
    return render(request, 'collectdetails.html', context)


def business_product_list(request, slug):
    biz = Business.objects.get(slug=slug)

    context = {'bizness':biz}
    return render(request, 'product_list.html', context)

class Creator(View):
    template_name = 'signup.html'

    def get(self, request):
         
        return render(request, Creator.template_name)
    

