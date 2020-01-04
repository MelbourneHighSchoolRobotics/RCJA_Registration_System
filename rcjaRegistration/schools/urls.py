from django.urls import path

from . import views
app_name = 'schools'
urlpatterns = [
    path('schools/createSchool',views.schoolCreation,name='createSchool'),
    path('accounts/signup',views.signup,name="signup"),
    path('accounts/profile',views.editProfile,name="profile"),
    path('schools/createSchoolAJAX',views.createSchoolAJAX,name="createAJAX")
]
