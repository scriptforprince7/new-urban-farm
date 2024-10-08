from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from unicodedata import decimal
from pyexpat import model
from email.policy import default
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.urls import reverse


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("disabled", "Disabled"),
    ("published", "Published"),
)

COURIER_PARTNER = (
    ("not assigned", "NOT ASSIGNED"),
    ("dtdc", "DTDC"),
    ("trackon", "Trackon"),
)

ACTIVE_STATUS = (
    ("disabled", "Disabled"),
    ("published", "Published"),
)

RATING = (
    ("1", "★"),
    ("2", "★★"),
    ("3", "★★★"),
    ("4", "★★★★"),
    ("5", "★★★★★"),
)

COLOR = (
    ("red", "Red"),
    ("black", "Black"),
    ("pink", "Pink"),
    ("blue", "Blue"),
    ("orange", "Orange"),
)

def user_directory_path(instance, filename):
    user_id = instance.user.id if instance.user else 'unknown'
    return 'user_{0}/{1}'.format(user_id, filename)



class Main_category(models.Model):
    mid = ShortUUIDField(unique=True, max_length=30, prefix="main_cat", alphabet="abcdefgh12345")
    main_title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="N/A")
    meta_description = models.CharField(max_length=100, default="N/A")
    meta_title = models.CharField(max_length=100, default="N/A")
    meta_tag = models.CharField(max_length=100, default="N/A")
    active_status = models.CharField(choices=ACTIVE_STATUS, max_length=10, default="disabled")
    image = models.ImageField(upload_to="category",default="maincategory.jpg")
    banner_image = models.ImageField(upload_to="category",default="maincategorybanner.jpg")

    class Meta:
        verbose_name_plural = "Main Categories"

    def main_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_category_banner_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.banner_image.url))
    
    def main_category_icon_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.icon_img.url))
    
    def get_absolute_url(self):
        return reverse('core:main_category', kwargs={'main_title': str(self.main_title)})
    
    def __str__(self):
        return self.main_title
    
class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    cat_title = models.CharField(max_length=100, default="Mobile & Laptop")
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")
    big_image = models.ImageField(upload_to=user_directory_path, default="bigcategory.jpg")


    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def category_big_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.big_image.url))
    
    def get_absolute_url(self):
        return reverse('core:inner-category', kwargs={'cat_title': str(self.cat_title)})
    
    def __str__(self):
        return self.cat_title
    

class Tags(models.Model):
    pass    
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345")
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, default="Mobile & Laptop")
    packing_size = models.CharField(max_length=500, default="Box 100 Pcs")
    minimum_order_qty = models.CharField(max_length=500, default="1")
    maximum_order_qty = models.CharField(max_length=500, default="1")
    unit_item = models.CharField(max_length=100, default="BOX")
    application = models.CharField(max_length=100, default="starter/seed")
    material = models.CharField(max_length=100, default="Cocopith")
    hsn_code = models.CharField(max_length=100, default="5305")
    gst_rate = models.CharField(max_length=100, default="18%")
    product_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=9999, decimal_places=2, default="1")
    old_price = models.DecimalField(max_digits=9999, decimal_places=2, default="2")
    specifications = models.TextField(max_length=500,null=True, blank=True, default="N/A")
    product_status = models.CharField(choices=STATUS, max_length=10, default="published")
    in_stock = models.BooleanField(default=True)
    summer_sale= models.BooleanField(default=False)
    new_arrival= models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=7, prefix="sku", alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")

    class Meta:
        verbose_name_plural = "Product"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'product_slug': self.product_slug})
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"

class ProductSeo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    canonical_link = models.CharField(max_length=500, default="N/A")
    meta_description = models.CharField(max_length=500, default="N/A")
    meta_title = models.CharField(max_length=500, default="N/A")
    meta_tag = models.CharField(max_length=500, default="N/A")
    meta_robots = models.CharField(max_length=500, default="N/A")
    og_url = models.CharField(max_length=500, default="N/A")
    og_title = models.CharField(max_length=500, default="N/A")
    og_description = models.CharField(max_length=500, default="N/A")
    og_image = models.CharField(max_length=500, default="N/A")
    twitter_title = models.CharField(max_length=500, default="N/A")
    twitter_description = models.CharField(max_length=500, default="N/A")
    twitter_description = models.CharField(max_length=500, default="N/A")


    class Meta:
        verbose_name_plural = "Product Seo"


class ProductVarient(models.Model):
    pvid = ShortUUIDField(unique=True, max_length=30, prefix="pvid", alphabet="abcdefgh12345") 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, default="Product Varient")
    status = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")

    class Meta:
        verbose_name_plural = "Product Varient"

    def variant_images(self):
        return ProductVariantTypes.objects.filter(product_variant=self)
    
    def __str__(self):
        return self.title

    def product_varient_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    

class ProductVariantTypes(models.Model):
    product_variant = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant_title = models.CharField(max_length=500, default="Product Varient")
    varient_price = models.DecimalField(max_digits=9999, decimal_places=2, default="1")
    gst_rate = models.CharField(max_length=12, default="5%")
    packaging_size = models.CharField(max_length=100, default="Packaging Size")
    in_stock = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.variant_title

    class Meta:
        verbose_name_plural = "Product Variant Types"

class ProductVariation(models.Model):
    product_variant = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variation_title = models.CharField(max_length=500, default="Product Variation")
    status = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.variation_title

    class Meta:
        verbose_name_plural = "Product Variation"

class ProductVariationTypes(models.Model):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variation_title = models.CharField(max_length=500, default="Product Variation")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Variation Types"

    def __str__(self):
        return self.variation_title

class ProductVariationTypesPrices(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_variant_type = models.ForeignKey(ProductVariantTypes, on_delete=models.SET_NULL, null=True)
    product_variation_types = models.ForeignKey(ProductVariationTypes, on_delete=models.SET_NULL, null=True)
    varient_type_price = models.DecimalField(max_digits=9999, decimal_places=2, default="1")
    gst_rate = models.CharField(max_length=12, default="5%")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Variation Types Prices"

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    courier_partner = models.CharField(choices=COURIER_PARTNER, max_length=30, default="Not Assigned")
    tracking_id = models.CharField(max_length=100, default="N/A")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    pin_details = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    division = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    shipping_street_address = models.CharField(max_length=200, blank=True, null=True)
    shipping_address_line1 = models.CharField(max_length=200, blank=True, null=True)
    shipping_address_line2 = models.CharField(max_length=200, blank=True, null=True)
    billing_zipcode = models.CharField(max_length=200, blank=True, null=True)
    billing_checkout_city = models.CharField(max_length=200, blank=True, null=True)
    billing_checkout_district = models.CharField(max_length=200, blank=True, null=True)
    billing_checkout_division = models.CharField(max_length=200, blank=True, null=True)
    billing_checkout_state = models.CharField(max_length=200, blank=True, null=True)
    billing_street_address = models.CharField(max_length=200, blank=True, null=True)
    billing_address_line1 = models.CharField(max_length=200, blank=True, null=True)
    billing_address_line2 = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    companyname = models.CharField(max_length=200, blank=True, null=True)
    gstnumber = models.CharField(max_length=200, blank=True, null=True)
    price_wo_gst_total = models.DecimalField(max_digits=99999, decimal_places=2, default="0")
    gst_rates_final = models.DecimalField(max_digits=99999, decimal_places=2, default="0.00")  # For storing the GST rate

    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    total = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    price_wo_gst = models.DecimalField(max_digits=99999, decimal_places=2, default="0")  # Update field name
    gst_rates_final = models.DecimalField(max_digits=99999, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url)) 





class PrivacyPolicy(models.Model):
    privacy_policy_content = HTMLField()


    class Meta:
        verbose_name_plural = "Privacy Policy"


class Blogs(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to="blogs-images", default="blogs.jpg")
    blog_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True) 
    blog_description = HTMLField()   
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blogs"

class InvoiceNumber(models.Model):
    number = models.IntegerField(default=1)

    def increment(self):
        self.number += 1
        self.save()

    def __str__(self):
        return f'Invoice No: INW2324-{self.number:04d}'
    
class Testimonials(models.Model):
    testimonial_name = models.CharField(max_length=100)
    testimonial_company = models.CharField(max_length=100)
    testimonial_image = models.ImageField(upload_to="blogs-images", default="blogs.jpg")
    testimonial = HTMLField()   
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Testimonials"