import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from .utils import Util

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = DATE_FORMAT + ' %H:%M:%S'
MAX_LENGTH = 2555
CURRENCIES = [("USD","USD"),("EUR","EUR"),("NGN","NGN"),("GBP","GBP"),
           ("PHP","PHP"),("KES","KES"),("TZS","TZS"),("UGX","UGX"),("RWF","RWF"),("BIF","BIF"),
           ]
DELIVERYSTATUSES = ['shipped', 'processing', 'out for delivery', 'delivered', 'pending', 'canceled', 'returned']
DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'

def parsedatetoint(datefield):
    return int(datefield.strftime(DATETIMEFORMAT))

class Profession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True, blank=False )
    createdAt = models.CharField(max_length=200, null=True, blank=False )
    updatedAt = models.CharField(max_length=200, null=True, blank=False )
    regulations = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
# Custom User Manager
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, nin, address, phonenumber, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        email = self.normalize_email(email)
        user = self.model(email=email, nin=nin, address=address, phonenumber=phonenumber, **extra_fields)
        user.password = Util.hash_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, nin, address, phonenumber, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('first_name', first_name)
        extra_fields.setdefault('last_name', last_name)
        return self._create_user(email, password, nin, address, phonenumber, **extra_fields)
    
    def create_tradeperson(self, email, password, nin, address, phonenumber, professionname, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_tradeperson', True)
        extra_fields.setdefault('professionname', professionname)
        return self._create_user(email, password, nin, address, phonenumber, **extra_fields)
    
    def create_business(self, email, password, nin, address, phonenumber, businessname,cac, websiteurl, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_business', True)
        extra_fields.setdefault('businessname', businessname)
        extra_fields.setdefault('cac', cac)
        extra_fields.setdefault('websiteurl', websiteurl)
        return self._create_user(email, password, nin, address, phonenumber, **extra_fields)
    
    def create_distributor(self, email, password, nin, address, phonenumber, distributorname, businessname,websiteurl, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_distributor', True)
        extra_fields.setdefault('distributorname',distributorname)
        extra_fields.setdefault('businessname', businessname)
        extra_fields.setdefault('websiteurl', websiteurl)
        return self._create_user(email, password, nin, address, phonenumber, **extra_fields)
    
    def create_deliverer(self, email, password, nin, address, phonenumber, deliverername,cac,websiteurl, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_deliverer', True)
        extra_fields.setdefault('deliverername', deliverername)
        extra_fields.setdefault('cac', cac)
        extra_fields.setdefault('websiteurl', websiteurl)
        return self._create_user(email, password, nin, address, phonenumber, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

# Create your User Model here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    password = models.CharField(max_length=255555)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    nin = models.CharField(max_length=20, null=True, blank=True)
    passport = models.CharField(max_length=20, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    address = models.UUIDField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    verifiedAt = models.CharField(max_length=200, null=True, blank=True)
    avgratings = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    is_tradeperson = models.BooleanField(default=False)
    professionname = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True)
    regulations = models.JSONField(null=True, blank=True)

    is_business = models.BooleanField(default=False)
    businessname = models.CharField(max_length=200, null=True, blank=False)
    cac = models.CharField(max_length=200, null=True, blank=True)
    websiteurl = models.CharField(max_length=200, null=True, blank=True)

    is_distributor = models.BooleanField(default=False)
    distributorname = models.CharField(max_length=200, null=True, blank=False)

    is_deliverer = models.BooleanField(default=False)
    deliverername = models.CharField(max_length=200, null=True, blank=False)

    date_joined = models.CharField(max_length=200, null=True, blank=True)
    updatedAt = models.CharField(max_length=200, null=True, blank=False )
    last_login = models.DateTimeField(auto_now=True)
    last_login_location = models.JSONField(null=True, blank=True)
    # Add related_name to avoid clashes with Django's auth.User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',  # Avoid clashes with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',  # Avoid clashes with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nin', 'address', 'phonenumber']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'       

    def __str__(self):
        return self.email
    
    def verify_password(self,provided_password):
        return Util.verify_password(self.password,provided_password)
        
## Address models-----------------------------------------------------------------------------------------
class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    houseNumber = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return {
            "id": self.id,
            "houseNumber": self.houseNumber,
            "city": self.city,
            "state": self.state,
            "postalCode": self.postalCode,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

## Review/rating model-----------------------------------------------------------------------------------
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True, blank=False )
    body = models.TextField(null=True, blank=True)
    userid = models.CharField(max_length=200, null=True, blank=False )
    files = models.JSONField(null=True, blank=True)#{name, desc, date, url}
    status = models.BooleanField(default=False)##like or dislike
    productid = models.CharField(max_length=200, null=True, blank=False )
    delivererid = models.CharField(max_length=200, null=True, blank=False )
    distributorid = models.CharField(max_length=200, null=True, blank=False )
    rating = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.CharField(max_length=200, null=True, blank=False )

    def __str__(self):
        return {'id':self.id, 'title':self.title, 'body':self.body, 'userid':self.userid, 'files':self.files, 'status':self.status, 'productid':self.productid, 'delivererid':self.delivererid, 'distributorid':self.distributorid, 'rating':self.rating, 'createdAt':self.createdAt}

class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(null=True, blank=True)
    userid = models.CharField(max_length=200, null=True, blank=False )
    files = models.JSONField(null=True, blank=True)#{name, desc, date, url}
    reviewid = models.CharField(max_length=200, null=True, blank=True )
    createdAt = models.CharField(max_length=200, null=True, blank=False )
    
    def __str__(self) -> str:
        return {'id':self.id, 'body':self.body, 'userid':self.userid, 'files':self.files,'reviewid':self.reviewid, 'createdAt':self.createdAt}

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True, blank=False )
    ownerid = models.CharField(max_length=200, null=True, blank=False )
    description = models.TextField(null=True, blank=True)
    url_link = models.CharField(max_length=200, null=True, blank=False )
    files = models.JSONField(null=True, blank=True)#{name, desc, date, content, url}
    DIFFICULTY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    difficulty = models.IntegerField(null=True, blank=True, default=1, choices=DIFFICULTY_CHOICES)
    requiredProfession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.CharField(max_length=200, null=True, blank=False )
    endDate = models.CharField(max_length=200, null=True, blank=False )
    updatedAt = models.CharField(max_length=200, null=True, blank=False )
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completeddate = models.CharField(max_length=200, null=True, blank=False )
    completedby = models.CharField(max_length=200, null=True, blank=False )
    address = models.CharField(max_length=200, null=True, blank=False )
    location = models.JSONField(null=True, blank=True)

    @property
    def duration(self):
        return parsedatetoint(self.endDate) - parsedatetoint(self.createdAt)

## services models-----------------------------------------------------------------------------------------
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jobid = models.CharField(max_length=200, null=False, blank=False )
    tradepersonid = models.CharField(max_length=200, null=False, blank=False )
    accepted = models.BooleanField(default=False) 
    started = models.BooleanField(default=False)
    starteddate = models.CharField(max_length=200, null=True, blank=False )
    inprogress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completeddate = models.CharField(max_length=200, null=True, blank=False )
    description = models.TextField(null=True, blank=True)
    files = models.JSONField(null=True, blank=True)#{name, desc, date, url}
    reviewid = models.CharField(max_length=200, null=True, blank=False )
    createdAt = models.CharField(max_length=200, null=True, blank=False )
    updatedAt = models.CharField(max_length=200, null=True, blank=False )
    location = models.JSONField(null=True, blank=True)#{lat,long}
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True )
    price = models.DecimalField(max_digits=1000000000, decimal_places=2, null=True, blank=True )

    def __str__(self):
        return self.id+'  '+self.price
    
## Order model-----------------------------------------------------------------------------------------
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userid = models.CharField(max_length=200, null=True, blank=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    currency = models.CharField(choices=CURRENCIES,max_length=200, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.CharField(max_length=200, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.CharField(max_length=200, null=True, blank=True)
    deliveredBy = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.CharField(max_length=200, null=True, blank=True)
    items = models.JSONField(null=True, blank=True) #{productid, name, image, qty, price, description}

    def __str__(self):
        return str(self.id)+'  '+self.totalPrice+' by '+self.userid+' at '+self.createdAt

## quotation model ----------------------------------------------
class Quotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quotation_by = models.CharField(max_length=200, null=True, blank=True)
    items = models.JSONField(default=list,null=True, blank=True)#{id, name, qty, image}
    signature = models.TextField(null=True, blank=True)
    createdAt = models.CharField(max_length=200, null=True, blank=True)
    updatedAt = models.CharField(max_length=200, null=True, blank=True)
    
    @property
    def count_items(self):
        # Check the type of items and return the count accordingly
        if isinstance(self.items, (list, tuple, set)):
            return len(self.items)
        elif isinstance(self.items, dict):
            return len(self.items.keys())
        return 0  # If items is not a list, tuple, set, or dict, return 0
    
## categories model----------------------------------------------------------------------------
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True, blank=False )
    icon = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
 
    def __str__(self):
        return self.name
     
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    currency = models.CharField(choices=CURRENCIES,max_length=200, null=True, blank=True)
    files = models.JSONField(null=True, blank=True)#{name, desc, date, url}
    createdat = models.DateTimeField()
    updatedat = models.DateTimeField()
    deletedat = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    business = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    location = models.JSONField(null=True, blank=True)#{lat,long}
    hashtags = models.JSONField(default=list, blank=True)  # Can store as a list of strings

    def __str__(self):
        return self.name or "Unnamed Product"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    senderid = models.CharField(max_length=200, null=True, blank=True)
    receiverid = models.CharField(max_length=200, null=True, blank=True)
    editable = models.BooleanField(default=False)
    deletable = models.BooleanField(default=False)
    deletedat = models.CharField(max_length=200, null=True, blank=True)
    read = models.BooleanField(default=False)
    body = models.TextField(null=True, blank=True)
    files = models.JSONField(null=True, blank=True)#{name, desc, date, content, url}
    createdat = models.CharField(max_length=200, null=True, blank=True)
    updatedat = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.body

class DeliveryTracker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userid = models.CharField(max_length=200, null=True, blank=True)
    sent = models.BooleanField(default=False)
    listofstats = models.JSONField(null=True, blank=True)
    prevstats = models.JSONField(null=True, blank=True)
    currentstat = models.JSONField(null=True, blank=True)
    received=models.BooleanField(default=False)
    receivedby = models.CharField(max_length=200, null=True, blank=True)
    receivedbyimage = models.TextField(null=True, blank=True)
    receivedbysignatureornin = models.TextField(null=True, blank=True)
    receivedbysignatureorninverified = models.BooleanField(default=False)
    receivedat = models.CharField(max_length=200, null=True, blank=True)
    createdat = models.CharField(max_length=200, null=True, blank=True)
    updatedat = models.CharField(max_length=200, null=True, blank=True)
    deliveryaddress = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.currentstat
    

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reason = models.CharField(max_length=200, null=True, blank=True)
    orderid = models.CharField(max_length=200, null=True, blank=True)
    orderamount = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    totalamount = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    serviceid = models.CharField(max_length=200, null=True, blank=True)
    payeeid = models.CharField(max_length=200, null=True, blank=True)  
    
    currency = models.CharField(choices=CURRENCIES,max_length=200, null=True, blank=True)
    payerid = models.CharField(max_length=200, null=True, blank=True)
    payeebank = models.CharField(max_length=200, null=True, blank=True)
    payerbank = models.CharField(max_length=200, null=True, blank=True)
    transaction_fees = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    walletid = models.CharField(max_length=200, null=True, blank=True)
    stat = [("success","success"),("failed","failed"),("pending","pending")]
    status = models.CharField(choices=stat,max_length=200, null=True, blank=True)
    receivername = models.CharField(max_length=200, null=True, blank=True) 
    sendername = models.CharField(max_length=200, null=True, blank=True)
    debit = models.BooleanField(default=False)
    last_login_location = models.JSONField(null=True, blank=True)#{lat,long}
    createdAt = models.CharField(max_length=200, null=True, blank=True)
    qrcode = models.TextField(null=True, blank=True)
    receipt = models.TextField(null=True, blank=True)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userid = models.CharField(max_length=200, null=True, blank=True)
    products= models.JSONField(null=True, blank=True)#{productid, name, image, qty, price, description}
    total = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    total_discount = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(
        max_digits=1000000000, decimal_places=2, null=True, blank=True)
    createdat = models.CharField(max_length=200, null=True, blank=True)
    updatedat = models.CharField(max_length=200, null=True, blank=True)
    location = models.JSONField(null=True, blank=True)#{lat,long}
    address = models.CharField(max_length=200, null=True, blank=True)
    ipaddress= models.CharField(max_length=200, null=True, blank=True)

class About(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=200)
    story = models.TextField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    phonenumberpre = models.CharField(max_length=15)
    phonenumber = models.CharField(max_length=15)
    emailone = models.EmailField(max_length=200)
    emailtwo = models.EmailField(max_length=200, blank=True, null=True)
    emailthree = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    values = models.TextField(blank=True, null=True)
    achievements = models.JSONField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    branches = models.JSONField(blank=True, null=True)
    policies = models.TextField(blank=True, null=True)
    socials = models.JSONField(blank=True, null=True)
    account_details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['-created_date']

@receiver(pre_save, sender=About)
def limit_about_instance(sender, instance, **kwargs):
    if About.objects.exists() and not instance.pk:
        raise ValidationError("Only one instance of About is allowed")