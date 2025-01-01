from django.db import models

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField()
    image = models.ImageField(upload_to='profile')
    
    Balance=models.DecimalField(max_digits=10,decimal_places=2,default=500.00)
    Pin_No=models.CharField(max_length=4,null=True,blank=True)
    bank_number = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.bank_number:
            last_aadhar = Bank.objects.all().order_by('bank_number').last()
            if last_aadhar:
                self.bank_number = last_aadhar.bank_number + 1
            else:
                self.bank_number = 123456789000
        super().save(*args,**kwargs)
