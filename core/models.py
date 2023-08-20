from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.


class Business(models.Model):
    business_name = models.TextField(unique=True)
    business_description = models.TextField(null=True)
    business_contact_number = models.CharField(max_length=500, null=True, blank=True)
    slug = models.TextField(unique=True, null=True)
    # business_cta_name = models.TextField(null=True, blank=True)
    # business_call_to_action = models.URLField(null=True, blank=True)
    # business_secret_key = models.CharField(max_length=1500, null=True, blank=True)
    business_instagram_link = models.URLField(null=True, blank=True)
    business_facebook_link = models.URLField(null=True, blank=True)
    business_twitter_link = models.URLField(null=True, blank=True)
    business_linkedin_link = models.URLField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = [ '-date_created']

    def __str__(self):
        return self.business_name


class Product(models.Model):

    HIDDEN = 'Hidden'
    ACTIVE = 'Active'
    STATUS = [
       (HIDDEN, ('Hidden')),
       (ACTIVE, ('Active')),
    ]
    product_name = models.TextField(null=True)
    product_description = models.TextField(null=True)
    product_terms = models.TextField(null=True)
    product_price = models.FloatField(null=True)
    product_redirect_url = models.URLField(null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    slug = models.TextField(unique=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    product_image = models.ImageField(upload_to='media/', default='')
    views = models.IntegerField(default=0, null=True)
    cta_click = models.IntegerField(default=0, null=True)
    reviews_count = models.IntegerField(default=0, null=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True)

    class Meta:
        ordering = [ '-date_created']

    def __str__(self):
        return self.product_name + ' by ' + self.business.business_name
    
    # def resize_image(self, width, height):
    #     img = Image.open(self.product_image)
    #     img = img.resize((width, height), Image.ANTIALIAS)
    #     buffered = BytesIO()
    #     img.save(buffered, format="PNG")
    #     self.product_image = InMemoryUploadedFile(buffered, None, self.product_image.name, 'image/jpeg', buffered.tell(), None)

    # def save(self, *args, **kwargs):
    #     if self.pk and self.product_image:
    #         # Resize the uploaded image to desired dimensions (e.g., 800x600)
    #         self.resize_image(200, 200)

    #     super().save(*args, **kwargs)


class Product_Media(models.Model):
    product_image = models.ImageField(upload_to='media', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    video = models.FileField(upload_to='media', null=True, blank=True, default='/static/images/nva.mov')



    def __str__(self):
        return self.product.product_name
    
    # def resize_image(self, width, height):
    #     img = Image.open(self.product_image)
    #     img = img.resize((width, height), Image.ANTIALIAS)
    #     buffered = BytesIO()
    #     img.save(buffered, format="PNG")
    #     self.product_image = InMemoryUploadedFile(buffered, None, self.product_image.name, 'image/jpeg', buffered.tell(), None)

    # def save(self, *args, **kwargs):
    #     if self.pk and self.product_image:
    #         # Resize the uploaded image to desired dimensions (e.g., 800x600)
    #         self.resize_image(400, 400)

    #     super().save(*args, **kwargs)
    

class Product_review(models.Model):
    HIDDEN = 'Hidden'
    ACTIVE = 'Active'
    STATUS = [
       (HIDDEN, ('Hidden')),
       (ACTIVE, ('Active')),
    ]
    creator = models.CharField(max_length=500, null=True)
    body = models.TextField(null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default=ACTIVE, null=True)

    class Meta:
        ordering = [ '-created']

    def __str__(self):

        return self.body[0:20] + ' by ' + self.product.product_name