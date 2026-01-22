from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True) # ==> te9bel null w te9bel ''
    last_name = models.CharField(max_length=50) # ==> not null 
    email = models.EmailField(unique=True)  # !!!! @ integrate into email <==> str
    age = models.PositiveIntegerField() # default validator age > 0 datatype ==> int 
    is_active = models.BooleanField(default=True) # boolean ==> True or False 
    created_at = models.DateTimeField(auto_now_add=True) # DateTimeField ==> date + time | DateField ==> only date | TimeField ==> only time
    classe = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" # return full name ==> firstname + lastname 