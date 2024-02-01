from django.test import Client, SimpleTestCase , TestCase
from django.urls import reverse, resolve
from Fulbari.views import home, product, about, blog_detail, dashboard ,login,delete_blog_view
from Product.views import admin_add_product_view, admin_products_view
from django.contrib.auth.models import User, auth 
from Product.models import Product



class TestUrls(SimpleTestCase):
    def test_resolve_to_home(self):
        url = reverse("home")
        resolver = resolve(url)
        self.assertEquals(resolver.func,home)


    def test_resolve_to_about(self):
        url = reverse("about")
        resolver = resolve(url)
        self.assertEquals(resolver.func,about)


    def test_resolve_to_product(self):
        url = reverse("product")
        resolver = resolve(url)
        self.assertEquals(resolver.func,product)

    
    def test_resolve_to_dashboard(self):
        url = reverse("dashboard")
        resolver = resolve(url)
        self.assertEquals(resolver.func,dashboard)    


class TestView(TestCase):
    def test_register_view(self):
        client = Client()
        response = client.get(reverse("register"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'pages/register.html')


    # def test_add_product_view(self):  
    #     client = Client()
    #     logged_in = client.login(username = 'admin',password ='admin')
    #     response = client.get(reverse("admin_products_view"))
    #     self.assertEquals(response.status_code,302)
    #     self.assertTemplateUsed(response,'adminControl/admin_product.html')        
       
    def test_case_registration_views(self):
            user=User.objects.create(username="testcase")
            user.set_password('123456')
            user.save()
 
            client=Client()
 
            logged_in=client.login(username='testcase',password="123456")
 
            url=reverse('register')
 
            response=client.post(url,{
            'username':'test name',
            'email' : 'test email',
            'password':'test pass',
            
        })
     
            self.assertEquals(response.status_code,302)
            self.assertRedirects(response,'/login')

    # def test_case_delete_views(self):
    #     user=User.objects.create(username="testcase")
    #     user.set_password('123456')
    #     user.save()
 
    #     client=Client()
 
    #     logged_in=client.login(username='testcase',password="123456")
 
    #     newlyCreated=User.objects.create(
    #         username='test name',
    #         email='test email',
    #         password='test pass',
        
    #     )
    #     print("here is customer id")
    #     print(newlyCreated.id)
    #     url=reverse('delete-blogs',args=[newlyCreated.id])
 
    
    #     response=client.delete(url)
    #     print(response)
    #     self.assertEquals(response.status_code,302)
    #     self.assertRedirects(response,"/blog")
    

    # def test_delete_product_view(self):
    #     client = Client()
    #     newProduct=Product.objects.create(name='shampoo',price=444)
    #     response = client.delete(reverse("delete-product"),args=[id])
    #     self.assertEquals(response.status_code,302)
    #     self.assertRedirects(response,'delete-product')    