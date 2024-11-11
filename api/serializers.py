from dataclasses import fields
from rest_framework import serializers
from .utils import Util
from datetime import datetime
from .models import DATE_FORMAT, DATETIME_FORMAT, Address, User, Profession, Product, About, Quotation, Order, Category, Cart, Transaction, Message, DeliveryTracker, Job, Service,Review,Comments,DELIVERYSTATUSES, CartItem

def authenticate(email=None, password=None, **kwargs):
    try:
        user = User.objects.get(email=email)
        print(user.password)
        
        if user.verify_password(password):
            
            return user
    except User.DoesNotExist:
        return None

class ProfessionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profession model.
    """
    class Meta:
        model = Profession
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        is_business = validated_data.pop('is_business', False)
        is_tradeperson = validated_data.pop('is_tradeperson', False)
        is_distributor = validated_data.pop('is_distributor', False)
        is_deliverer = validated_data.pop('is_deliverer', False)
        is_superuser = validated_data.pop('is_superuser', False)
        businessname = validated_data.pop('businessname', None)
        professionname = validated_data.pop('professionname', None)
        distributorname = validated_data.pop('distributorname', None)
        deliverername = validated_data.pop('deliverername', None)
        cac = validated_data.pop('cac', None)
        websiteurl = validated_data.pop('websiteurl', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        nin = validated_data.pop('nin', None)
        address = validated_data.pop('address', None)
        phonenumber = validated_data.pop('phonenumber', None)
        
        if is_business:
            if not businessname or not cac or not websiteurl:
                raise serializers.ValidationError("Business name, CAC, and website URL are required for business users.")
            user = User.objects.create_business(email=email, password=password, nin=nin, address=address, phonenumber=phonenumber, businessname=businessname,cac=cac, websiteurl=websiteurl, **validated_data)
        
        elif is_tradeperson:
            if not professionname:
                raise serializers.ValidationError("Profession Name is required for tradepersons.")
            user = User.objects.create_tradeperson(email=email, password=password, nin=nin, address=address, phonenumber=phonenumber,professionname=professionname, **validated_data)
        
        elif is_distributor:
            if not distributorname:
                raise serializers.ValidationError("Distributor name is required for distributors.")
            user = User.objects.create_distributor(email=email, password=password, nin=nin, address=address, phonenumber=phonenumber, distributorname=distributorname, businessname=businessname, websiteurl=websiteurl, **validated_data)
        
        elif is_deliverer:
            if not deliverername:
                raise serializers.ValidationError("Deliverer name is required for deliverers.")
            user = User.objects.create_deliverer(email=email, password=password, nin=nin, address=address, phonenumber=phonenumber, deliverername = deliverername, cac=cac,websiteurl=websiteurl, **validated_data)
        
        elif is_superuser:
            user = User.objects.create_superuser(email=email, password=password, **validated_data)
        else:
            user = User.objects.create_user(email=email, password=password, nin=nin, address=address, phonenumber=phonenumber,**validated_data)
        
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        is_business = validated_data.get('is_business', instance.is_business)
        is_tradeperson = validated_data.get('is_tradeperson', instance.is_tradeperson)
        is_distributor = validated_data.get('is_distributor', instance.is_distributor)
        is_deliverer = validated_data.get('is_deliverer', instance.is_deliverer)
        businessname = validated_data.get('businessname', instance.businessname)
        professionname = validated_data.get('professionname', instance.professionname)
        distributorname = validated_data.get('distributorname', instance.distributorname)
        deliverername = validated_data.get('deliverername', instance.deliverername)
        cac = validated_data.get('cac', instance.cac)
        websiteurl = validated_data.get('websiteurl', instance.websiteurl)

        if is_business:
            if not businessname or not cac or not websiteurl:
                raise serializers.ValidationError("Business name, CAC, and website URL are required for business users.")
            instance.businessname = businessname
            instance.cac = cac
            instance.websiteurl = websiteurl
        
        elif is_tradeperson:
            if not professionname:
                raise serializers.ValidationError("Profession title is required for tradepersons.")
            instance.professionname = professionname
        
        elif is_distributor:
            if not distributorname:
                raise serializers.ValidationError("Distributor name is required for distributors.")
            instance.distributorname = distributorname
            instance.websiteurl = websiteurl
        
        elif is_deliverer:
            if not deliverername:
                raise serializers.ValidationError("Deliverer name is required for deliverers.")
            instance.deliverername = deliverername
            instance.cac = cac
            instance.websiteurl = websiteurl
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = Util.hash_password(password)

        instance.save()
        return instance

class BusinessSerializer(UserSerializer):
    """
    Serializer for business.
    """
    class Meta:
        model = UserSerializer.Meta.model
        fields = ('id',"phonenumber",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_business','businessname','cac',"websiteurl",'date_joined','updatedAt','last_login','last_login_location')

class DistributorSerializer(UserSerializer):
    """
    Serializer for distributor.
    """
    class Meta:
        model = UserSerializer.Meta.model
        fields = ('id',"phonenumber",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_distributor','distributorname','businessname',"websiteurl",'date_joined','updatedAt','last_login','last_login_location')

class TradePersonSerializer(UserSerializer):
    """
    Serializer for tradeperson.
    """
    class Meta:
        model = UserSerializer.Meta.model
        fields = ('id',"title", 'first_name',"last_name","phonenumber",'nin',"passport",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_tradeperson','professionname','regulations','date_joined','updatedAt','last_login','last_login_location')

class DelivererSerializer(UserSerializer):
    """
    Serializer for deliverer.
    """
    class Meta:
        model = UserSerializer.Meta.model
        fields = ('id',"phonenumber",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_deliverer','deliverername','cac',"websiteurl",'date_joined','updatedAt','last_login','last_login_location')

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        #print(email, password,"++++++++++++++++++++++++",self.context.get('request'))

        if email and password:
            user = authenticate(email=email, password=password)
            print(user)
            if not user:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        attrs['user'] = user
        return attrs



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class ProductBusinessSerializer(UserSerializer):
    """
    Serializer for business.
    """
    class Meta:
        model = UserSerializer.Meta.model
        fields = ('id', 'image', 'businessname', 'websiteurl')

class ProductBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'image', 'businessname', 'websiteurl']

class ProductSerializer(serializers.ModelSerializer):
    business = ProductBusinessSerializer(read_only=True)  # Read-only representation of the business
    files = serializers.JSONField(required=False, allow_null=True)
    location = serializers.JSONField(required=False, allow_null=True)
    createdat = serializers.DateTimeField(format=DATETIME_FORMAT, input_formats=[DATETIME_FORMAT])
    updatedat = serializers.DateTimeField(format=DATETIME_FORMAT, input_formats=[DATETIME_FORMAT])
    deletedat = serializers.DateTimeField(format=DATETIME_FORMAT, input_formats=[DATETIME_FORMAT], required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'description', 'price', 'currency', 
            'files', 'createdat', 'updatedat', 'deletedat', 'deleted', 
            'category', 'address', 'location', 'hashtags', 'business'
        ]

    def create(self, validated_data):
        # Extract and validate 'files'
        files_data = validated_data.pop('files', None)
        if files_data:
            for file in files_data:
                if not all(k in file for k in ('name', 'desc', 'date', 'url')):
                    raise serializers.ValidationError("Each file item must contain 'name', 'desc', 'date', 'url'.")

        # Extract and validate 'location'
        location_data = validated_data.pop('location', None)
        if location_data:
            if not all(k in location_data for k in ('lat', 'long')):
                raise serializers.ValidationError("Location must contain 'lat' and 'long'.")

        # Extract and validate 'business'
        business_id = self.initial_data.get('business')  # 'business' is passed in initial data, not validated_data
        if business_id:
            try:
                business = User.objects.get(id=business_id)  # Fetch the business using the business ID
            except User.DoesNotExist:
                raise serializers.ValidationError("Business with this ID does not exist.")
        else:
            raise serializers.ValidationError("Business ID must be provided.")

        # Create the product instance
        product = Product.objects.create(business=business, **validated_data)

        # Assign 'files' and 'location' data
        product.files = files_data
        product.location = location_data
        product.save()  # Save the instance after assigning files and location

        return product

    def update(self, instance, validated_data):
        # Extract and validate 'files'
        files_data = validated_data.pop('files', None)
        if files_data:
            for file in files_data:
                if not all(k in file for k in ('name', 'desc', 'date', 'url')):
                    raise serializers.ValidationError("Each file item must contain 'name', 'desc', 'date', 'url'.")

        # Extract and validate 'location'
        location_data = validated_data.pop('location', None)
        if location_data:
            if not all(k in location_data for k in ('lat', 'long')):
                raise serializers.ValidationError("Location must contain 'lat' and 'long'.")

        # Update instance fields
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.category = validated_data.get('category', instance.category)
        instance.address = validated_data.get('address', instance.address)

        # Update 'files' and 'location' if provided
        if files_data is not None:
            instance.files = files_data
        if location_data is not None:
            instance.location = location_data

        # Save the updated instance
        instance.save()
        return instance


###Address Serializers---------------------
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

#about 
class AboutSerializer(serializers.ModelSerializer):
    """
    Serializer for About model.
    """
    class Meta:
        model = About
        fields = [
            'id', 'company_name', 'story', 'logo', 'phonenumber', 'emailone',
            'emailtwo', 'emailthree', 'address', 'mission', 'values',
            'achievements', 'created_date', 'updated_date', 'branches',
            'policies', 'socials', 'account_details'
        ]

class QuotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quotation
        fields = ['id', 'quotation_by', 'items', 'signature','createdAt', 'updatedAt']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        for item in items_data:
            # Ensure the item has all the required fields
            if not all(k in item for k in ('productid', 'qty', 'name', 'image')):
                raise serializers.ValidationError("Each item must contain 'productid', 'qty', 'name', 'image'.")
        
        quotation = Quotation.objects.create(**validated_data)
        quotation.items = items_data
        quotation.save()
        return quotation

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        for item in items_data:
            # Ensure the item has all the required fields
            if not all(k in item for k in ('productid', 'qty', 'name', 'image')):
                raise serializers.ValidationError("Each item must contain 'productid', 'qty', 'name', 'image'")
        
        instance.quotation_by = validated_data.get('quotation_by', instance.quotation_by)
        instance.signature = validated_data.get('signature', instance.signature)
        instance.items = items_data
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()

    class Meta:
        model = Order
        fields = ['id', 'userid', 'paymentMethod', 'taxPrice', 'shippingPrice', 'totalPrice', 'currency', 'isPaid', 'paidAt', 'isDelivered', 'deliveredAt', 'deliveredBy', 'createdAt', 'items']

    def validate_items(self, items_data):
        # Validate each item in the items list
        for item in items_data:
            if not all(k in item for k in ('productid', 'name', 'image', 'qty', 'price', 'description')):
                raise serializers.ValidationError("Each item must contain 'productid', 'name', 'image', 'qty', 'price', and 'description'.")
        return items_data

    def create(self, validated_data):
        items_data = self.validate_items(validated_data.pop('items'))
        order = Order.objects.create(**validated_data)
        order.items = items_data
        order.save()
        return order

    def update(self, instance, validated_data):
        items_data = self.validate_items(validated_data.pop('items'))
        
        instance.userid = validated_data.get('userid', instance.userid)
        instance.paymentMethod = validated_data.get('paymentMethod', instance.paymentMethod)
        instance.taxPrice = validated_data.get('taxPrice', instance.taxPrice)
        instance.shippingPrice = validated_data.get('shippingPrice', instance.shippingPrice)
        instance.totalPrice = validated_data.get('totalPrice', instance.totalPrice)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.isPaid = validated_data.get('isPaid', instance.isPaid)
        instance.paidAt = validated_data.get('paidAt', instance.paidAt)
        instance.isDelivered = validated_data.get('isDelivered', instance.isDelivered)
        instance.deliveredAt = validated_data.get('deliveredAt', instance.deliveredAt)
        instance.deliveredBy = validated_data.get('deliveredBy', instance.deliveredBy)
        instance.createdAt = validated_data.get('createdAt', instance.createdAt)
        instance.items = items_data
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    products = serializers.JSONField()
    location = serializers.JSONField()

    class Meta:
        model = Cart
        fields = [
            'id', 'userid', 'products', 'total', 'total_discount', 
            'total_tax', 'createdat', 'updatedat', 'location', 'address', 'ipaddress'
        ]

    def validate_products(self, products_data):
        for product in products_data:
            if not all(k in product for k in ('productid', 'name', 'image', 'qty', 'price', 'description')):
                raise serializers.ValidationError("Each product must contain 'productid', 'name', 'image', 'qty', 'price', and 'description'.")
        return products_data

    def validate_location(self, location_data):
        if not all(k in location_data for k in ('lat', 'long')):
            raise serializers.ValidationError("Location must contain 'lat' and 'long'.")
        return location_data

    def create(self, validated_data):
        products_data = self.validate_products(validated_data.pop('products'))
        location_data = self.validate_location(validated_data.pop('location', {}))
        cart = Cart.objects.create(**validated_data)
        cart.products = products_data
        cart.location = location_data
        cart.save()
        return cart

    def update(self, instance, validated_data):
        products_data = self.validate_products(validated_data.pop('products', instance.products))
        location_data = self.validate_location(validated_data.pop('location', instance.location))
        
        instance.userid = validated_data.get('userid', instance.userid)
        instance.total = validated_data.get('total', instance.total)
        instance.total_discount = validated_data.get('total_discount', instance.total_discount)
        instance.total_tax = validated_data.get('total_tax', instance.total_tax)
        instance.createdat = validated_data.get('createdat', instance.createdat)
        instance.updatedat = validated_data.get('updatedat', instance.updatedat)
        instance.address = validated_data.get('address', instance.address)
        instance.ipaddress = validated_data.get('ipaddress', instance.ipaddress)
        instance.products = products_data
        instance.location = location_data
        instance.save()
        return instance

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'createdat', 'updatedat']
        
class TransactionSerializer(serializers.ModelSerializer):
    last_login_location = serializers.JSONField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'reason', 'orderid', 'orderamount', 'totalamount', 'serviceid', 'payeeid',
            'currency', 'payerid', 'payeebank', 'payerbank', 'transaction_fees', 'walletid',
            'status', 'receivername', 'sendername', 'debit', 'last_login_location', 'createdAt', 'qrcode'
        ]

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        
        # Generate QR code if not provided
        if not transaction.qrcode:
            data_to_encode = f"Transaction ID: {transaction.id}\nTotal Amount: {transaction.totalamount}\nCurrency: {transaction.currency}"
            # import os
            # print(os.getcwd(),"======================")
            transaction.qrcode = Util.gen_qrcode(data_to_encode,'base/oashe_logo.png')
            transaction.save()
        if not transaction.receipt:
            order_data = {
                "order_id": "123456",
                "date": "2024-06-19",
                "customer_name": "John Doe",
                "customer_address": "123 Elm Street, Springfield",
                "items": [
                    {"name": "Widget A", "quantity": 2, "price": 19.99},
                    {"name": "Widget B", "quantity": 1, "price": 29.99},
                    {"name": "Widget C", "quantity": 3, "price": 9.99},
                ],
                "total": 99.94
            }
            transaction.receipt = Util.generate_pdf_receipt_in_memory(order_data,'base/oashe_logo.png')
            transaction.save()
        
        return transaction

class MessageSerializer(serializers.ModelSerializer):
    files = serializers.JSONField()

    class Meta:
        model = Message
        fields = [
            'id', 'senderid', 'receiverid', 'editable', 'deletable', 'deletedat', 'read', 'body', 
            'files', 'createdat', 'updatedat'
        ]

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.senderid = validated_data.get('senderid', instance.senderid)
        instance.receiverid = validated_data.get('receiverid', instance.receiverid)
        instance.editable = validated_data.get('editable', instance.editable)
        instance.deletable = validated_data.get('deletable', instance.deletable)
        instance.deletedat = validated_data.get('deletedat', instance.deletedat)
        instance.read = validated_data.get('read', instance.read)
        instance.body = validated_data.get('body', instance.body)
        instance.files = validated_data.get('files', instance.files)
        instance.createdat = validated_data.get('createdat', instance.createdat)
        instance.updatedat = validated_data.get('updatedat', instance.updatedat)
        instance.save()
        return instance
 
class DeliveryTrackerSerializer(serializers.ModelSerializer):
    listofstats = serializers.JSONField()
    prevstats = serializers.JSONField()
    currentstat = serializers.JSONField()

    class Meta:
        model = DeliveryTracker
        fields = [
            'id', 'userid', 'sent', 'listofstats', 'prevstats', 'currentstat', 
            'received', 'receivedby', 'receivedbyimage', 'receivedbysignatureornin', 
            'receivedbysignatureorninverified', 'receivedat', 'createdat', 'updatedat', 'deliveryaddress'
        ]

    def validate_status_timestamp(self, stats):
        allowed_statuses = DELIVERYSTATUSES
        
        if not isinstance(stats, list):
            raise serializers.ValidationError("The field must be a list of dictionaries.")

        for stat in stats:
            if 'status' not in stat or 'timestamp' not in stat:
                raise serializers.ValidationError("Each stat must contain 'status' and 'timestamp'.")
            if stat['status'] not in allowed_statuses:
                raise serializers.ValidationError(f"Invalid status value for ->'{stat['status']}'.")
            try:
                datetime.fromisoformat(stat['timestamp'])
            except ValueError:
                raise serializers.ValidationError("Invalid timestamp format. It should be in ISO 8601 format.")

        return stats

    def validate(self, data):
        if 'listofstats' in data:
            data['listofstats'] = self.validate_status_timestamp(data['listofstats'])
        if 'prevstats' in data:
            data['prevstats'] = self.validate_status_timestamp(data['prevstats'])
        if 'currentstat' in data:
            data['currentstat'] = self.validate_status_timestamp([data['currentstat']])[0]  # Validate as list with one item

        return data

    def create(self, validated_data):
        return DeliveryTracker.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.userid = validated_data.get('userid', instance.userid)
        instance.sent = validated_data.get('sent', instance.sent)
        instance.listofstats = validated_data.get('listofstats', instance.listofstats)
        instance.prevstats = validated_data.get('prevstats', instance.prevstats)
        instance.currentstat = validated_data.get('currentstat', instance.currentstat)
        instance.received = validated_data.get('received', instance.received)
        instance.receivedby = validated_data.get('receivedby', instance.receivedby)
        instance.receivedbyimage = validated_data.get('receivedbyimage', instance.receivedbyimage)
        instance.receivedbysignatureornin = validated_data.get('receivedbysignatureornin', instance.receivedbysignatureornin)
        instance.receivedbysignatureorninverified = validated_data.get('receivedbysignatureorninverified', instance.receivedbysignatureorninverified)
        instance.receivedat = validated_data.get('receivedat', instance.receivedat)
        instance.createdat = validated_data.get('createdat', instance.createdat)
        instance.updatedat = validated_data.get('updatedat', instance.updatedat)
        instance.deliveryaddress = validated_data.get('deliveryaddress', instance.deliveryaddress)
        instance.save()
        return instance

class JobSerializer(serializers.ModelSerializer):
    files = serializers.JSONField()
    location = serializers.JSONField()

    class Meta:
        model = Job
        fields = [
            'id', 'name', 'ownerid', 'description', 'url_link', 'files',
            'difficulty', 'requiredProfession', 'deleted', 'createdAt', 'endDate',
            'updatedAt', 'started', 'completed', 'completeddate', 'completedby',
            'address', 'location'
        ]

    def validate_files(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Files must be a list.")
        for file in value:
            if not all(key in file for key in ('name', 'desc', 'date', 'content', 'url')):
                raise serializers.ValidationError(
                    "Each file must contain 'name', 'desc', 'date', 'content', and 'url'.")
        return value

    def validate_location(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Location must be a dictionary.")
        if not all(key in value for key in ('lat', 'long')):
            raise serializers.ValidationError("Location must contain 'lat' and 'long'.")
        return value

    def create(self, validated_data):
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class ServiceSerializer(serializers.ModelSerializer):
    files = serializers.JSONField(required=False)
    location = serializers.JSONField(required=False)

    class Meta:
        model = Service
        fields = ['id', 'jobid', 'tradepersonid', 'accepted', 'started', 'starteddate', 'inprogress', 'completed', 'completeddate', 'description', 'files', 'reviewid', 'createdAt', 'location', 'user', 'price']
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'user']

    def validate_files(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Files must be a list of objects")
        for file in value:
            if not all(k in file for k in ('name', 'desc', 'date', 'url')):
                raise serializers.ValidationError("Each file must contain 'name', 'desc', 'date', and 'url'")
        return value

    def validate_location(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Location must be a dictionary")
        if not all(k in value for k in ('lat', 'long')):
            raise serializers.ValidationError("Location must contain 'lat' and 'long'")
        return value
    
    def create(self, validated_data):
        return Service.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'body', 'userid', 'files', 'status', 'productid', 'delivererid', 'distributorid', 'rating', 'createdAt']
        read_only_fields = ['id', 'createdAt']

    def validate_files(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Files must be a list of objects")
        for file in value:
            if not all(k in file for k in ('name', 'desc', 'date', 'url')):
                raise serializers.ValidationError("Each file must contain 'name', 'desc', 'date', and 'url'")
        return value

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'body', 'userid', 'files', 'reviewid', 'createdAt']
        read_only_fields = ['id', 'createdAt']

    def validate_files(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Files must be a list of objects")
        for file in value:
            if not all(k in file for k in ('name', 'desc', 'date', 'url')):
                raise serializers.ValidationError("Each file must contain 'name', 'desc', 'date', and 'url'")
        return value