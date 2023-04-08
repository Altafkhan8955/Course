from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="files/thumbnail/")
    date = models.DateTimeField(auto_now_add=True)
    resource = models.FileField(upload_to="files/resource/")
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class CourseProperty(models.Model):
    description = models.CharField(max_length=50, null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Tag(CourseProperty):
    pass
class Prerequisite(CourseProperty):
    pass
class Learning(CourseProperty):
    pass

class Video(models.Model):
    title = models.CharField(max_length=100,null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length=30, null=False)
    is_preview = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    password = models.CharField(max_length=250)
    @staticmethod
    def get_user_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

class UserCourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.firstname} - {self.course.name}'

class Payment(models.Model):
    order_id = models.CharField(max_length=50,null=False)
    payment_id = models.CharField(max_length=50)
    user_course = models.ForeignKey(UserCourse,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

class CouponCode(models.Model):
    code = models.CharField(max_length=7)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coupons')
    dicount = models.IntegerField(default=0)
    expiredate = models.DateField(default=False)
