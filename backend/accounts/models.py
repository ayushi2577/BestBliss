import string
import random
#from /features.models import Bookings,membership_plans

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,email,password,name,**extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")   #should raise vallueerror as http response is at serializer lebvel
        if not password:
            raise ValueError("The Password field must be set.")   #should raise vallueerror as http response is at serializer lebvel
        elif not name:
            raise ValueError("The Name field must be set.")   #should raise vallueerror as http response is at serializer lebvel
        
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,name,**extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password,name,**extra_fields)

class User(AbstractBaseUser):
    id=models.CharField(null=False,unique=True,primary_key=True)
    email=models.EmailField(null=False,unique=True,max_length=50)
    name=models.CharField(null=False,max_length=20)
    membership=models.CharField(default='customer',max_length=15)
    tier_level=models.IntegerField(default=1)
    reward_points=models.IntegerField(default=0)
    referal_link=models.CharField(null=False,unique=True,max_length=200)

    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    objects=UserManager()  #do not miss parentheses here 
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']  #for superuser as and Django explicitly forbids putting your USERNAME_FIELD (here, email) or password inside 
    #REQUIRED_FIELDS. Django automatically requires those. Keeping them there will break the application.

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        #custom ID (e.g., BB-1001, BB-1002...) if it doesn't exist yet
        if not self.id:
            starting_number = 1000
            prefix = "BB-"  
            
            # Find the highest existing ID number in the database
            last_user = User.objects.all().order_by('id').last()
            last_user = User.objects.all().order_by('id').last()
            if last_user and last_user.id.startswith(prefix):
                try:
                    # Extract the number part and increment it
                    last_number = int(last_user.id.replace(prefix, ""))
                    self.id = f"{prefix}{last_number + 1}"
                except ValueError:
                    # Fallback if something goes wrong with parsing
                    self.id = f"{prefix}{starting_number + 1}"
            else:
                self.id = f"{prefix}{starting_number}"

        # Generate a unique custom referral link if it doesn't exist yet
        if not self.referal_link:
            link_prefix = "https://bestbliss.com/ref/"
            # Generates a random 8-character alphanumeric string (e.g., A7k9PqX2)
            random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            self.referal_link = f"{link_prefix}{random_suffix}"

        # Call the real Django save method to write to the database
        super(User, self).save(*args, **kwargs)
