from django.db import models
from django.contrib.auth.models import User

# Role based access
class Profile(models.Model):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('staff','Staff'),
        ('viewer','Viewer'),
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    




class Category(models.Model):
    name=models.CharField(max_length=50)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
         
# Items model
class Item(models.Model):
    item_name=models.CharField(max_length=50)
    category=models.ForeignKey('Category',on_delete=models.CASCADE,blank=True,null=True)
    supplier=models.ForeignKey('Supplier',on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.PositiveIntegerField(default=0)
    description=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.item_name

    class Meta:
        ordering=['-date_added']    
    


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        return self.name

class StockEntry(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='entries')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_added = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)     

    def __str__(self):
        return f"Added {self.quantity_added} to {self.item.item_name}"


class StockExit(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='exits')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_removed = models.PositiveIntegerField()
    date_removed = models.DateTimeField(auto_now_add=True)
    removed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Removed {self.quantity_removed} from {self.item.item_name}"        

