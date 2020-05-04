from django.db import models
from django.contrib.auth.models import User

class UserStockDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    purchaseDate = models.DateField()
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    website = models.CharField(max_length=50, null=True)
    costprice = models.IntegerField(null=True)
    currency = models.CharField(max_length=20, null=True)
    shortName = models.CharField(max_length=70, null=True)

    def __str__(self):
        return str(self.purchaseDate)+" "+self.symbol+" "+str(self.quantity)
