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
from django.db.models import F
from .filters import PriceFilter
from .forms import Form1
from django.template.defaultfilters import slugify 
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator 
# Create your views here.


def home(request):

    return render(request, 'home.html')

def dash(request, slug):
    biz =  Business.objects.get(slug=slug) 
    products = Product.objects.filter(business=biz)
    reviews = Product_review.objects.filter(product__business=biz)


    context = {'biz':biz, 'products':products, 'reviews':reviews}
    return render(request, 'dash.html', context)

class Dashboard(View):
    template_name = 'dash.html'

    def get(self, request, slug):
        biz =  Business.objects.get(slug=slug) 
        products = Product.objects.filter(business=biz)
        reviews = Product_review.objects.filter(product__business=biz)
        date = biz.date_created.strftime('%Y-%m-%d')

        context = {'biz':biz, 'products':products, 'reviews':reviews, 'date':date}
        return render(request, Dashboard.template_name, context)



def editproduct(request, slug, slugx):
    
    biz = Business.objects.get(slug=slug)
    product = Product.objects.get(slug = slugx)
    reviews = Product_review.objects.filter(product=product)

    if request.method == 'POST':
        images = request.POST.getlist('images')
        image_list = []
        specific_product = Product.objects.filter(slug = slugx)
        product_update = specific_product.update(
                product_name = request.POST['product_name'],
                product_description = request.POST['product_description'],
                product_price = request.POST['product_price'],
                business = biz,
                slug = slugify(request.POST['product_name']),
                status = request.POST['status'],
            )
        # for image in images:
        #         media = Product_Media.objects.create(
        #             product_image = image,
        #             video = request.POST['video'],
        #             product = product
        #         )
        #         media.save()
        my_view = ProductList()
        return my_view.get(request, biz.slug)
        

    context = {'biz':biz, 'product':product, 'reviews':reviews}    
    return render(request, 'edit-product.html', context)

def deleteproduct(request, slug, slugx):
    
    biz = Business.objects.get(slug=slug)
    product = Product.objects.get(slug = slugx)

    if request.method == 'POST':
        delete_text = request.POST.get('delete_text')

        if delete_text == product.product_name:

            product.delete()
       
            my_view = ProductList()
            return my_view.get(request, biz.slug)
        else:
            messages.error(request, "The input does not match the product name")
            return redirect('deleteproduct', biz.slug, product.slug)
        

    context = {'biz':biz, 'product':product}    
    return render(request, 'delete-product.html', context)

def hideproduct(request, slug, slugx):
    biz = Business.objects.get(slug=slug)
    product = Product.objects.get(slug = slugx)


    product_status = Product.objects.filter(slug=slugx).update(status='Hidden')

    my_view = ProductList()
    return my_view.get(request, biz.slug)



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
            images = request.FILES.getlist('images')
            image_list = []

            productcreate = Product.objects.create(
                    product_name = request.POST['product_name'],
                    product_description = request.POST['product_description'],
                    product_price = request.POST['product_price'],
                    product_redirect_url = request.POST['product_payment_link'],
                    product_image = request.FILES.get('images'),
                    business = biz,
                    slug = slugify(request.POST['product_name']),
                )
            productcreate.save()
            for image in images:
                media = Product_Media.objects.create(
                    product_image = image,
                    video = request.FILES.get('video'),
                    product = productcreate
                )
                
                media.save()

            my_view = ProductPage()
            return my_view.get(request, biz.slug, productcreate.slug)
    
def signin(request):

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        if not request.POST.get('email'):
            messages.error(request, "Email cannot be blank.")
            return redirect('signin')

        if not request.POST.get('password'):
            messages.error(request, "Password cannot be blank.")
            return redirect('signin')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

class ProductList(View):
    template_name = 'index-aler.html'
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
        
        # product_media = products.product_media_set.all()
        queryset = products

        # Check if the 'sort' query parameter is present in the URL
        sort_param = request.GET.get('sort')

        if sort_param == 'newest':
            # Sort the queryset by the 'created_date' field in descending order (newest to oldest)
            products = queryset.order_by('-date_created')
            # context = {'biz':biz, 'products':products, 'page':page_obj, 
            #        'text':text, 'average':ProductPage.average, 'data': queryset}
            # return render(request, 'date-filter.html', context)

        elif sort_param == 'oldest':
            # Sort the queryset by the 'created_date' field in ascending order (oldest to newest)
            products = queryset.order_by('date_created')
            # context = {'biz':biz, 'products':products, 'page':page_obj, 
            #        'text':text, 'average':ProductPage.average, 'data': queryset}
            # return render(request, 'date-filter.html', context)
        
        price_queryset = products

        # Check if the 'sort' query parameter is present in the URL
        sort_param = request.GET.get('price')

        if sort_param == 'highest':
            # Sort the queryset by the 'created_date' field in descending order (newest to oldest)
            products = price_queryset.order_by('-product_price')
            # context = {'biz':biz, 'products':products, 'page':page_obj, 
            #        'text':text, 'average':ProductPage.average, 'pricedata': querysetx}
            # return render(request, 'price-filter.html', context)

        elif sort_param == 'lowest':
            # Sort the queryset by the 'created_date' field in ascending order (oldest to newest)
            products = price_queryset.order_by('product_price')
            # context = {'biz':biz, 'products':products, 'page':page_obj, 
            #        'text':text, 'average':ProductPage.average, 'pricedata': querysetx}
            # return render(request, 'price-filter.html', context)
        

        search_keyword = request.GET.get('search')

        search_queryset = products

        if search_keyword:
            # Filter the queryset to include objects that have the search_keyword in their 'object_name'
            products = search_queryset.filter(product_name__icontains=search_keyword)
            # context = {'biz':biz, 'products':products, 'page':page_obj, 
            #        'text':text, 'average':ProductPage.average, 'search': querysety}
            # return render(request, 'search-filter.html', context)



        # Create a Paginator object
        paginator = Paginator(products, self.items_per_page)

        # Get the current page number from the request
        page_number = request.GET.get('page')

        # Get the Page object for the current page
        page_obj = paginator.get_page(page_number)

        if request.user == biz.user:
            ProductList.template_name = 'dashboard.html'
        else:
            ProductList.template_name = 'index-aler.html'

        
        context = {'biz':biz, 'products':products, 'page':page_obj, 
                   'text':text, 'average':ProductPage.average, 'data': queryset}
        return render(request, ProductList.template_name, context)
    
class ProductPage(View):
    template_name = 'product-pil.html'

    average = 1
    def get(self, request, slug, slugx):
        biz = Business.objects.get(slug=slug)
        productx = Product.objects.get(slug=slugx)
        product_media = Product_Media.objects.filter(product=productx)
        review = Product_review.objects.filter(product=productx)
        if request.user != biz.user:
            product_views = Product.objects.filter(slug=slugx).update(views=F('views') +1)
        
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
        return render(request, ProductPage.template_name, context)
    def post(self, request, slug, slugx):
        biz = Business.objects.get(slug=slug)
        productx = Product.objects.get(slug=slugx)

        if request.method == 'POST':
            creator = request.POST['review_creator']
            body = request.POST['review_body']
            review = Product_review.objects.create(
                creator = request.POST['review_creator'],
                body = request.POST['review_body'],
                product = productx,
                rating = request.POST['review_rating']
            )
            review.save()
            review_count = Product.objects.filter(slug=slugx).update(reviews_count=F('reviews_count') +1)
            mail = EmailMessage(
                "New comment on your product",
                creator + ' commented: ' + body + ' on your product: ' + productx.product_name,
                'settings.EMAIL_HOST_USER',
                [biz.user.email],
            )
            mail.fail_silently = False
            mail.content_subtype = 'html'
            mail.send()
        my_view = ProductPage()
        return my_view.get(request, biz.slug, productx.slug)
   

def cta_click(request, slug):
    productx = Product.objects.get(slug=slug)
    click = Product.objects.filter(slug=slug).update(cta_click=F('cta_click') +1)
    url = productx.product_redirect_url

    return redirect(url)

class CreateBusiness(View):
    template_name = 'createbusiness.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)

        return render(request, CreateBusiness.template_name)
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        if request.method == 'POST':
            business = Business.objects.create(
                business_name = request.POST['product_name'],
                business_description = request.POST['product_description'],
                slug = slugify(request.POST['product_name']), 
                user = user
            )
            business.save()
            businessx = ProductList()
            return businessx.get(request, business.slug)
        # return render(request, CreateBusiness.template_name)
    
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
    # template_name = 'signup.html'

    def get(self, request):
         
        return render(request, 'signup.html')
    
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('email')
            first_name = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            global token
            token =  str(random.randint(100001,999999))

            
            if User.objects.filter(email=email).exists():
                    messages.error(request, "User already exists.")
                    return redirect('signup')

            if not request.POST.get('password1'):
                messages.error(request, "Password cannot be blank.")
                return redirect('signup')

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('signup')

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "User already exists.")
                    return redirect('signup')
                else:
                    # html_message = loader.render_to_string(
                    # 'email-welcome.html',
                    # {
                    #     'user_name': first_name,
                    #     'token':token
                        
                    
                    # }
                    # )                 
                    # mail = EmailMessage(
                    #     "Verification Code for Your New Account",
                    #     html_message,
                    #     'settings.EMAIL_HOST_USER',
                    #     [email],
                    # )
                    # mail.fail_silently = False
                    # mail.content_subtype = 'html'
                    # mail.send()
                    print(token)                    
                    user = User.objects.create_user(username=username,first_name=first_name, password=password1, email=email)
                    
                    user.is_active = False
                    user.save()
                    
                    # my_page = VerifyEmail()
                    # return my_page.get(request, token, user)
                    return redirect('verifymail', pk=user.id)
                    


class VerifyEmail(View):

    def get(self, request, token, user):

        return render(request, 'verify.html')

def verifymail(request, pk):

    user = User.objects.get(id=pk) 
    if request.method == 'POST':
        entetoken = request.POST.get('token')
        entered_token = str(entetoken)
        if entetoken == token:
            messages.error(request, "Email validated, you can now signin.")
            user.is_active = True
            user.save()
            print(token)  
            my_biz = CreateBusiness()
            return my_biz.get(request, user.id)
            

        elif entered_token != token:
            messages.error(request, "Token incorrect.")
            user.is_active = False
            user.save()
            print(token)  
            my_view = Creator()
            return my_view.get(request)
        
    return render(request, 'verify.html')
        
        
    

