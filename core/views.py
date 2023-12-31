from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
import random
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template import loader, Template
from .models import Business, Product, Product_Media, Product_review
from django.db.models import F, Sum, Count
from .filters import PriceFilter
from .forms import Form1
from django.template.defaultfilters import slugify 
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator 
from django.core.mail import send_mail
from django.core.cache import cache
# Create your views here.


def home(request):

    return render(request, 'home.html')

def reroutedashboard(request, pk):
    user = User.objects.get(id=pk)
    business = Business.objects.get(user=user)

    my_view = Dashboard()
    return my_view.get(request, business.slug)

def dash(request, slug):
    biz =  Business.objects.get(slug=slug) 
    products = Product.objects.filter(business=biz)
    reviews = Product_review.objects.filter(product__business=biz)


    context = {'biz':biz, 'products':products, 'reviews':reviews}
    return render(request, 'admindash.html', context)

# class Dashboard(LoginRequiredMixin, View):
class Dashboard(View):
    template_name = 'admindash.html'

    def get(self, request, slug):
        try:
            # Use get_object_or_404 to handle cases where the Business doesn't exist.
            biz = get_object_or_404(Business, slug=slug)
            products = Product.objects.filter(business=biz)
            reviews = Product_review.objects.filter(product__business=biz)
            date = biz.date_created.strftime('%Y-%m-%d')
            product_count = products.count()
            text = f'SHOWING ALL ({product_count} products)'

            context = {'biz': biz, 'text': text, 'products': products, 'reviews': reviews, 'date': date}
            return render(request, self.template_name, context)
        except Exception as e:
           
            return render(request, 'error.html', {'error_message': f"Error: {str(e)}"})

    def post(self, request, slug):
        try:
            biz = get_object_or_404(Business, slug=slug)
            if request.method == 'POST':
                # Update business information based on the form data.
                biz.product_name = request.POST['product_name']
                biz.product_description = request.POST['product_description']
                biz.product_price = request.POST['product_price']
                biz.slug = slugify(request.POST['product_name'])
                biz.status = request.POST['status']
                biz.save()

                
                return redirect('frontend:dashboard', slug=biz.slug)
        except Exception as e:
           
            return render(request, 'error.html', {'error_message': f"Error: {str(e)}"})


class ProductDashboard(View):
    template_name = 'productdash.html'

    def get(self, request, slug, slugx):
        try:
           
            biz = get_object_or_404(Business, slug=slug)
            product = get_object_or_404(Product, slug=slugx)
            reviews = Product_review.objects.filter(product=product)

            context = {'biz': biz, 'product': product, 'reviews': reviews}
            return render(request, self.template_name, context)
        except Exception as e:
           
            return render(request, 'error.html', {'error_message': f"Error: {str(e)}"})

    def post(self, request, slug, slugx):
        try:
            biz = get_object_or_404(Business, slug=slug)
            product = get_object_or_404(Product, slug=slugx)

            if request.method == 'POST':
                
                product.product_name = request.POST['product_name']
                product.product_description = request.POST['product_description']
                product.product_price = request.POST['product_price']
                product.slug = slugify(request.POST['product_name'])
                product.status = request.POST['status']
                product.save()

                
                return redirect('frontend:product_dashboard', slug=biz.slug, slugx=product.slug)
        except Exception as e:
           
            return render(request, 'error.html', {'error_message': f"Error: {str(e)}"})

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
        my_view = Dashboard()
        return my_view.get(request, biz.slug)
        # pre_url = request.META.get('HTTP_REFERER')
        # return redirect(pre_url)
        
        

    context = {'biz':biz, 'product':product, 'reviews':reviews}    
    return render(request, 'edit-product.html', context)

def deleteproduct(request, slug, slugx):
    
    biz = Business.objects.get(slug=slug)
    product = Product.objects.get(slug = slugx)

    if request.method == 'POST':
        delete_text = request.POST.get('delete_text')

        if delete_text == product.product_name:

            product.delete()
       
            my_view = Dashboard()
            return my_view.get(request, biz.slug)
        else:
            messages.error(request, "The input does not match the product name")
            my_view = ProductDashboard()
            return my_view.get(request, biz.slug, product.slug)
        

    context = {'biz':biz, 'product':product}    
    return render(request, 'delete-product.html', context)

def hidereview(request, slug, slugx, pk):
    biz = Business.objects.get(slug=slug)
    product = Product.objects.get(slug = slugx)
    review = Product_review.objects.get(id=pk)

    sort_param = request.GET.get('status')

    if sort_param == 'active':
        product_review = Product_review.objects.filter(pk=pk).update(status='Hidden')
    elif sort_param == 'hidden':
        product_review = Product_review.objects.filter(pk=pk).update(status='Active')

    

    my_view = ProductDashboard()
    return my_view.get(request, biz.slug, product.slug)



class CreatePage(View):
    template_name = 'create_page.html'

    def get(self, request, slug):
        biz = get_object_or_404(Business, slug=slug)
        context = {'choice': CreatePage.viewers_choice, 'biz': biz}
        return render(request, CreatePage.template_name, context)

    def post(self, request, slug):
        biz = get_object_or_404(Business, slug=slug)
        if request.method == 'POST':
            images = request.FILES.getlist('images')
            product = Product(
                product_name=request.POST['product_name'],
                product_description=request.POST['product_description'],
                product_price=request.POST['product_price'],
                product_redirect_url=request.POST['product_payment_link'],
                product_image=request.FILES.get('images'),
                business=biz,
                slug=slugify(request.POST['product_name']),
            )
            product.save()
            
            for image in images:
                media = Product_Media(
                    product_image=image,
                    video=request.FILES.get('video'),
                    product=product
                )
                media.save()

            return redirect('product_page', slug=biz.slug, slugx=product.slug)

def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        if not username:
            messages.error(request, "Email cannot be blank.")
            return redirect('signin')

        if not password:
            messages.error(request, "Password cannot be blank.")
            return redirect('signin')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
            return redirect('signin')

    return render(request, 'login.html')

class ProductList(View):
    template_name = 'product-coza.html'
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


        # f = PriceFilter({'request.GET': '1800000', 'request.GET': '5000000'}, queryset=products)
        # Create a Paginator object
        paginator = Paginator(products, self.items_per_page)

        # Get the current page number from the request
        page_number = request.GET.get('page')

        # Get the Page object for the current page
        page_obj = paginator.get_page(page_number)

        if request.user == biz.user:
            ProductList.template_name = 'dashboard.html'
        else:
            ProductList.template_name = 'product-coza.html'

        
        context = {'biz':biz, 'products':products, 'page':page_obj, 
                   'text':text, 'average':ProductPage.average, 'data': queryset}
        return render(request, ProductList.template_name, context)
    
class ProductPage(View):
    template_name = 'product-pil.html'

    def get(self, request, slug, slugx):
        try:
            biz = Business.objects.get(slug=slug)
            productx = Product.objects.get(slug=slugx)
            product_media = Product_Media.objects.filter(product=productx)
            review = Product_review.objects.filter(product=productx, status="Active")
            related_products = Product.objects.filter(business=biz, status="Active")
            
            # Cache the product for 5 minutes (300 seconds)
            result = cache.get(f'product_{productx.id}')
            if result is not None:
                return result

            # Update product views only if the user is not the business owner
            if request.user != biz.user:
                Product.objects.filter(slug=slugx).update(views=F('views') + 1)

            review_count = review.count()
            review_text = f'{review_count} Reviews'

            product_rating = Product_review.objects.filter(product=productx)
            total_sum = product_rating.aggregate(Sum('rating'))['rating__sum']
            total_count = product_rating.count()

            # Calculate the average rating or set it to 0 if there are no reviews
            average_rating = total_sum / total_count if total_count > 0 else 0

            # Cache the rendered template for this product
            context = {
                'biz': biz,
                'product': productx,
                'product_media': product_media,
                'review': review,
                'review_text': review_text,
                'average': average_rating,
                'related_products': related_products
            }
            response = render(request, ProductPage.template_name, context)

            # Cache the rendered template for 5 minutes
            cache.set(f'product_{productx.id}', response, 300)
            
            return response
        except Business.DoesNotExist:
            messages.error(request, "Business does not exist.")
            return redirect('home')

    def post(self, request, slug, slugx):
        biz = Business.objects.get(slug=slug)
        productx = Product.objects.get(slug=slugx)

        if request.method == 'POST':
            creator = request.POST['review_creator']
            body = request.POST['review_body']
            rating = request.POST['review_rating']
            
            review = Product_review.objects.create(
                creator=creator,
                body=body,
                product=productx,
                rating=rating
            )
            review.save()
            
            Product.objects.filter(slug=slugx).update(reviews_count=F('reviews_count') + 1)

        # Redirect back to the product page after submitting a review
        return redirect('product_page', slug=biz.slug, slugx=productx.slug) 

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

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('email')
        first_name = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        global token
        token = str(random.randint(100001, 999999))

        # Validation checks
        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists.")
            return redirect('creator')

        if not password1:
            messages.error(request, "Password cannot be blank.")
            return redirect('creator')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('creator')

        # If validation passes, create the user
        user = User.objects.create_user(username=username, first_name=first_name, password=password1, email=email)
        user.is_active = False
        user.save()

        # Redirect to a view that handles email verification
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
        

class PasswordResetVerifymail(View):
    token =  str(random.randint(100001,9999999))
    def get(self, request):

        return render(request, 'password_reset_verifymail.html') 
    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            token = PasswordResetVerifymail().token
            if User.objects.filter(email=email).exists():

                # send_mail(
                #     'Trying to change your password?  -  Oxos-ReceiptMkr!',
                #     token,
                #     'mezardini@gmail.com',
                #     [email],
                #     fail_silently=False,
                # )
                reclaim_url = 'http://127.0.0.1:8000/reclaim_password/1/'+token
                print(reclaim_url) 
                return redirect('forgotpassword')
                
            else:
                messages.error(request, "User does not exist. Try again")
                my_page = PasswordResetVerifymail()
                return my_page.get(request)
            

def password_reset_update_password(request, pk, str):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        code = request.POST.get('code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if  password1==password2:
            # user = User.objects.get(id=pk)
            user.set_password(password1)
            user.save()
            
        if  password1!=password2:
            messages.error(request, "Passwords do not match. Try again")
            my_page = PasswordResetVerifymail()
            return my_page.get(request)
        # if code != PasswordResetVerifymail().token:
        #     messages.error(request, "Wrong verification code provided")
        #     my_page = PasswordResetVerifymail()
        #     return my_page.get(request)

    return render(request, 'password_reset_update_password.html') 

# def password_reset_update_password(request, pk, str):
#     user = User.objects.get(id=pk)
#     if request.method == 'POST':
#         code = request.POST.get('code')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if code == PasswordResetVerifymail().token and password1==password2:
#             user = User.objects.get(id=pk)
#             user.set_password(password1)
#             user.save()
            
#         if code == PasswordResetVerifymail().token and password1!=password2:
#             messages.error(request, "Passwords do not match. Try again")
#             my_page = PasswordResetVerifymail()
#             return my_page.get(request)
#         if code != PasswordResetVerifymail().token:
#             messages.error(request, "Wrong verification code provided")
#             my_page = PasswordResetVerifymail()
#             return my_page.get(request)

#     return render(request, 'password_reset_update_password.html') 
