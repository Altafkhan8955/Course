from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import logout , login
from django.views.generic.edit import FormView
from django.conf import settings
from django.contrib.staticfiles.urls import static
from sell.models import*
from django.views import View
from django.contrib.auth.hashers import make_password,check_password
from courses.settings import*
from random import randint
import razorpay
from django.views.decorators.csrf import csrf_exempt
from time import time
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView 
#from .constants import PaymentStatus
client = razorpay.Client(auth=(KEY_ID,KEY_SECRET ))

# Create your views here.
def index(request):
    course = Course.objects.all()
    #video = Video.objects.all()
   # data = {
     #   'course': course,
       # 'video': video,
   # }
    return render(request,"index.html",{'courses':course})

def course(request, slug):
    course = Course.objects.get(slug = slug)
    serial_number = request.GET.get('lecture')
    video = course.video_set.all().order_by("serial_number")
    next_lecture = 2
    prev_lecture = None
    if serial_number is None:
        serial_number = 1
    else:
        next_lecture = int(serial_number)+1
        if len(video) < next_lecture:
            next_lecture = None
        prev_lecture=int(serial_number)-1
        if len(video) < next_lecture :
            next_lecture = None
    video = Video.objects.get(serial_number = serial_number, course = course)
    if (video.is_preview is False):
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user=user, course=course)
            except:
                return redirect("checkout", slug=course.slug)
    context = {
        "course": course,
        "video": video,
        "next_lecture": next_lecture,
        "prev_lecture": prev_lecture,

    }
    return render(request,template_name="course.html",context=context)

class signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        firstname = postData.get('firstname')
        lastname = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        cpassword = postData.get('cpassword')    
        # validation
        value = {
            'firstname': firstname,
            'lastname': lastname,
            'phone': phone,
            'email': email
        }
        error_message = None
        if password == cpassword:
            user = Customer(firstname=firstname,
                            lastname=lastname,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateuser(user)

        if not error_message:
            user.password = make_password(user.password)
            user.save()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateuser(self, user):
        error_message = None
        if (not user.firstname):
            error_message = "First Name Required !!"
        elif len(user.firstname) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not user.lastname:
            error_message = 'Last Name Required'
        elif len(user.lastname) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not user.phone:
            error_message = 'Phone Number required'
        elif len(user.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(user.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(user.email) < 5:
            error_message = 'Email must be 5 char long'
        elif Customer.objects.filter(email=user.email):
            error_message = "Email already exist"
        #elif user.isExists():
           # error_message = 'Email Address Already Registered..'
        # saving

        return error_message
    
class login(View):
    def get(self, request):
        return render(request,"login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Customer.get_user_by_email(email)
        error_message = None
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['id'] = user.id
                request.session['firstname'] = user.firstname
                request.session['lastname'] = user.lastname
                request.session['phone'] = user.phone
                request.session['email'] = user.email
                request.session['password'] = user.password
                return redirect('index')
            else:
                error_message = "Email or password invalid"
        else:
            error_message = "Email or password invalid"
        return render(request,"login.html",{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect('login')




#@login_required(login_url='/login')
def checkout(request,slug):
    course = Course.objects.get(slug = slug)
    #user = User.objects.all()
    user = request.user
    action = request.GET.get('action')
    couponcode = request.GET.get('couponcode')
    couponcode_message = None
    order = None
    payment = None
    error = None
    coupon = None
    try:
        user_course = UserCourse.objects.get( user = user, course = course)
        error = "You are Already Enrolled in this course"
    except:
        pass
    amount = None
    if error is None:
           amount = int((course.price - ( course.price * course.discount * 0.01 )) * 100)
           # if amount is zero don't create payment only save enrolled course
    """if couponcode:
        try:
          coupon =  CouponCode.objects.get(course = course, code = couponcode)
          amount = course.price - (course.price * course.discount * 0.01)
          amount = int(amount) * 100
        except:
            couponcode_message = 'invalid Coupon Code'
            print("code invalid") 
    if amount == 0:
        userCourse = UserCourse(user = user, course = course)
        userCourse.save()
        return redirect("mycourse")"""
    if action == 'create_payment':
           currency = "INR"
           notes = {
               "email" : user.email,
             # "name" : f'{Customer.firstname} {Customer.lastname}'
         } 
           reciept = f"codetech-{int(time())}"
           order = client.order.create(
               { 
               "receipt": reciept , 
               "notes": notes,
               "amount": amount,
               "currency": currency
            }
           )
           payment = Payment()
           payment.user = user
           payment.course = course
           payment.order_id = order.get('id')
           payment = payment.save()  
    context = {
        "course" : course,
        "order" : order,
        "payment" : payment,
        "user" : user,
        "error" : error,
        "coupon": coupon,
        "couponcode_message": couponcode_message
    }
    return render(request,template_name="checkout.html", context=context)

@csrf_exempt
def verifypayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCourse(user = payment.user, course = payment.course)
            usercourse.save()

            payment.user_course = UserCourse
            payment.save()
            return render(request,template_name="verify.html", context=context)
        except:
            return HttpResponse("Invalid Payment details")

@method_decorator(login_required(login_url='login'), name="dispatch")
class mycourse(ListView):
    template_name = "verify.html"
    context_object_name = 'verify'
    
    def  get_queryset(self):
        return UserCourse.objects.filter(user = self.request.user)
    
"""
@login_required(login_url="login")
def mycourse(request):
    user = request.user
    print(user)
    user_course = UserCourse.objects.filter(user = user)
    context = {
        "user_course" : user_course
    }
    return render(request=request, template_name="verify.html",context=context)
"""

    
