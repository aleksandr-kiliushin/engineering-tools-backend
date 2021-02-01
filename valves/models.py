from django.db import models


class Equipment(models.Model):
    code           = models.CharField(max_length=100, unique=True)
    dn             = models.IntegerField(null=True)
    equip_type     = models.CharField(max_length=100, null=True)
    full_title     = models.CharField(max_length=100, null=True)
    kvs            = models.FloatField(null=True)
    price          = models.FloatField(null=True)
    type_title     = models.CharField(max_length=100, null=True)
    z              = models.FloatField(null=True)
    discount_group = models.CharField(max_length=100)
    
    def __str__(self):
        return self.code
