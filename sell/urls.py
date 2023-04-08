from django.contrib import admin
from django.urls import path
from .import views
#from views import view
from django.conf.urls.static import static
from django.conf import settings
from .views import signup
from .views import login,mycourse


urlpatterns = [
    #path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path("course/<str:slug>",views.course,name='course'),
    path("signup",signup.as_view(),name="signup"),
    path("login",login.as_view(),name="login"),
    path("logout",views.logout,name="logout"),
    path("checkout/<str:slug>",views.checkout,name="checkout"),
    path("verifypayment",views.verifypayment,name="verifypayment"),
    path("mycourse",mycourse.as_view(),name="mycourse"),
]
