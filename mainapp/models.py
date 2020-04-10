from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class UserProfileInfo(models.Model):
#
#     # Create relationship (don't inherit from User!)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     phno=models.CharField(max_length=10)
    # # Add any additional attributes you want
    # portfolio_site = models.URLField(blank=True)
    # # pip install pillow to use this!
    # # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    # profile_pic = models.ImageField(upload_to='basic_app/profile_pics',blank=True)

    # def __str__(self):
    #     # Built-in attribute of django.contrib.auth.models.User !
    #     return self.user.username

class UserStockDetails(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    purchaseDate = models.DateField()
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.purchaseDate)+" "+self.symbol+" "+str(self.quantity)
