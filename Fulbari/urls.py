from unicodedata import name
from django.urls import path
from Fulbari import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path("register",views.register, name='register'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('contact',views.contact, name='contact'),
    path('logout', views.logout, name="logout"),
    path('product', views.product, name="product"),
    path('blogform', views.blogform, name="blogform"),
    path('blog', views.showblog, name="blog"),
    path('<int:id>', views.blog_detail, name='blog_detail'),
    path('delete-blogs/<int:pk>', views.delete_blog_view,name='delete-blogs'),

    path('update-blog/<int:pk>', views.update_blog_view,name='update-blog'),

    path('profile/', views.profile, name='profile'),
    
    

    # Most important functon
    path('afterlogin', views.afterlogin_view, name="afterlogin"),
    path('admindashboard', views.admindashboard_view, name="admindashboard"),
    path('allblog', views.allblog, name="allblog"),
    path('view-customer', views.view_customer, name='view-customer'),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html'),
         name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    path('profile/', views.profile, name='profile'),

    path('edit-profile', views.edit_profile_view,name='edit-profile'),     
]

 