from django.contrib import admin
from sell.models import Course,Tag,Prerequisite,Learning,Video,Customer,UserCourse,Payment,CouponCode
from django.utils.html import format_html
# Register your models here.
class Tagadmin(admin.TabularInline):
    model = Tag

class Prerequisiteadmin(admin.TabularInline):
    model = Prerequisite

class Learningadmin(admin.TabularInline):
    model = Learning

class Videoadmin(admin.TabularInline):
    model = Video

class Courseadmin(admin.ModelAdmin):
    inlines = [Tagadmin, Prerequisiteadmin, Learningadmin, Videoadmin]
    list_display = ['name', 'get_price', 'get_discount', 'active']
    list_filter = ("discount", "active")

    def get_price(self, course):
        return f'₹ {course.price}'
    def get_discount(self, course):
        return f'{course.discount} %'
    
    get_price.short_description = "Price"
    get_discount.short_description = "Discount"



class usercourseadmin(admin.ModelAdmin):
    list_display = ['Click','get_user', 'get_course', 'date']
    #list_filter = ("get_course")

    def get_user(self, usercourse):
        return format_html(f"<a href='/admin/courses/course/{usercourse.user.id}'>{usercourse.user}<a>")
    
    def Click(self, usercourse):
        return "Click open"
    
    def get_course(self, usercourse):
        return format_html(f"<a href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}<a>")
    
    get_user.short_description = "user"
    get_course.short_descriptin = "course"
    


class paymentadmin(admin.ModelAdmin):
    list_display = ['order_id', 'payment_id', 'user_course', 'get_user', 'get_course', 'date', 'status']
    list_filter = ("status", "course")

    def get_user(self, Payment):
        return format_html(f"<a href='/admin/auth/user/{Payment.user.id}'>{Payment.user}</>")

    def get_course(self, Payment):
        return format_html(f"<a href='/admin/courses/course/{Payment.course.id}'>{Payment.course}</>")
    
    get_user.short_description = "user"
    get_course.short_description = "course"
    
class customeradmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'phone', 'email', 'password']
admin.site.register(Course,Courseadmin)
admin.site.register(UserCourse,usercourseadmin)
admin.site.register(Payment,paymentadmin)
admin.site.register(CouponCode)
admin.site.register(Customer, customeradmin)
