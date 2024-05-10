from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.Homepage, name='home'),
    path('About', views.Aboutpage, name='About'),
    path('Contact', views.Contactpage, name='Contact'),
    path('Error', views.Errorpage, name='Error'),
    path('AddPost', views.AddPostpage, name='Addpost'),
    path('Job_Page/edit/<int:id>', views.AddPost_Edit_Process, name='Addpost'),
    path('Job_Page/update', views.AddPost_update_Process, name='Addpost'),
    path('Job_Page/delete/<int:id>', views.AddPost_delete, name='Addpost'),
    path('AddPost/inserted', views.AddPost_Add_Process, name="Post Add Process"),
    path('Login', views.Loginpage, name='Login'),
    path('Company_Login', views.Loginpage_company, name='Login'),
    path('Register', views.Registerpage, name='Register'),
    path('Register/user/inserted', views.Register_User_Add, name="Register user"),
    path('Register/company/inserted', views.Register_Company_Add, name="Register"),
    path('Job', views.Jobpage, name='Job'),
    path('ForgetPassword', views.Forgetpage, name='ForgetPassword'),
    path('ForgetPasswordAction', views.ForgetPasswordAction, name='ForgetPassword1'),
    path('Pricing', views.Pricingpage, name='Pricing'),
    path('Payment', views.Payment, name='Payment'),
    path('Applied_user', views.Applied_user, name='Applied_user'),
    path('Applied_company', views.Applied_company, name='Applied_company'),
    path('ChangePassword', views.Changepage, name='ChangePassword'),
    path('ConfirmPassword', views.Changepage, name='ChangePassword'),
    #path('Job_Page', views.Job_single, name='Job_single'),
    path('Job_Page/inserted', views.Applied_Add_Process, name='Job_applied'),
    path('Candidate/<int:id>', views.Candidate_single, name='Candidate_single'),
    path('Company/<int:id>', views.Company_single, name='Company_single'),
    path('Register_Company', views.Register_company, name='Register_comp_Page'),
    path('Job_Page/<int:id>', views.Job_single_Page, name='Job_single'),
    path('Search', views.Search_job, name='Job Search'),
    path('logout', views.logout, name='Job Search1'),
    path('logout_comp', views.logout_company, name='Job Search1'),
    path('JobFilter', views.job_filter, name='Job Filter'),
    path('Job/Category/<int:id>',views.job_by_category, name='Job'),
    path('Job/Location/<int:id>',views.job_by_location, name='Job'),
    path('JobSeekers/edit/<int:id>', views.JobSeeker_Edit, name="JobSeekers Edit"),
    path('JobSeekers/update', views.JobSeeker_Update, name="JobSeekers Update"),
    path('Company/edit/<int:id>', views.Company_Edit, name="Company Edit"),
    path('Company/update', views.Company_Update, name="Company Update"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)