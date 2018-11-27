from django.conf.urls import url

from app import views

urlpatterns = [
    # 导航栏分类内容
    url(r'^home/', views.home, name='home'),

]