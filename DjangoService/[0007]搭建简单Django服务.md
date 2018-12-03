---
title: [0007]搭建简单Django服务
tags: 
notebook: 【1000】Python
---

### 搭建Django服务
#### 安装相关依赖
```
    pip install requests 
```
#### 创建 DjangoService
```
    which django-admin
    cd Desktop
    /Library/Frameworks/Python.framework/Versions/3.5/bin/django-admin startproject DjangoService
```
#### 增加自定义模块
我们手动添加一个子模块 getAndPost 的文件夹，在其中创建三个文件
  - urls.py : http接口供外部调用
  - views.py : 内部对http请求的参数进行输出并返回
  - __init__.py : 空的文件，这样python才会将对应的文件夹识别为一个模块，允许对其进行调用

此时目录结构
```
    DjangoService
    │   db.sqlite3
    │   manage.py  
    │   README.md
    │   
    └───DjangoService
        │   __init__.py
        │   settings.py
        │   urls.py
        │   wsgi.py
        │   
        └───getAndPost
            │   __init__.py
            │   view.py
            │   urls.py
```

#### 在服务器增加一个请求入口，进入到创建的子模块
```py
    # DjangoService->DjangoService->urls.py
    from django.conf.urls import url, include
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
        url(r'^request', include('DjangoService.getAndPost.urls')),
    ]
```

#### 自定义子模块
```py
    # DjangoService->DjangoService->getAndPost->urls.py
    from django.conf.urls import url
    from . import views

    urlpatterns = [
            url('', views.sendRequest),
        ]
```

```py
    # DjangoService->DjangoService->getAndPost->view.py
    #!/usr/bin/env python
    # coding=utf-8
    import json
    import requests
    from django.views.decorators.csrf import csrf_exempt
    from django.http import HttpRequest, HttpResponse


    # 默认开启了csrf保护机制，本服务仅作自测使用，加上csrf_exempt去除掉csrf保护
    @csrf_exempt
    def sendRequest(request):
        print('get into get request')
        dct = {
                'GET': request.GET,
                'POST': request.POST,
                # 'Body': request.body,
                # 在Django的实现中，request.POST对象是用于存储包含表单数据的对象，而在request.body中则包含了content中的原始(raw)非表单数据
                }
        try:
            dct['json_parsed_body'] = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            print('json loads except:{}'.format(e))
        # return HttpResponse("Hello Django")
        return HttpResponse(HttpResponse(json.dumps(dct)), content_type='application/json')
```
### 启动服务器
```
    # 数据库迁移
    python3 manage.py migrate
    # 启动
    python3 manage.py runserver
```
### 发送请求
Get
```
    http://127.0.0.1:8000/request?getkey=getvalue
```

Post
```py
    http://127.0.0.1:8000/request
    Body{
      "bodykey":"bodyvalue"
    }
```


### 使用 REST framework
#### 添加依赖
```
    pip install djangorestframework
```
#### 创建一个 api 的应用
```
    python3 manage.py startapp api
```
在 api 项目下面创建 、urls.py 、serializers.py
  - urls.py : 路由接口
  - serializers.py : 序列化的功能工具

此时目录结构
```
    DjangoService
    │   db.sqlite3
    │   manage.py  
    │   README.md
    │   
    └───DjangoService
    │    │   __init__.py
    │    │   settings.py
    │    │   urls.py
    │    │   wsgi.py
    │    │   
    │    └───getAndPost
    │        │   __init__.py
    │        │   view.py
    │        │   urls.py
    │
    │        
    └───api
    │    │   __init__.py
    │    │   admin.py
    │    │   app.py
    │    │   models.py
    │    │   serializers.py
    │    │   test.py
    │    │   urls.py
    │    │   view.py
```

#### 注册 api 应用及添加依赖的 rest_framework 应用
```py
    # DjangoService->DjangoService->settings.py
    INSTALLED_APPS = [
    'api',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]
```
#### 创建模型
```py
    # DjangoService->api->models.py
    class Student(models.Model):
    name = models.CharField(u'姓名', max_length=100, default='no_name')
    sex = models.CharField(u'性别',max_length=50,default='male')
    sid = models.CharField(u'学号',max_length=100,default='0')
 
    def __unicode__(self):
        return '%d: %s' % (self.pk, self.name)
```
对数据库进行同步和迁移
```
    python3 manage.py makemigrations
    python3 manage.py migrate
```
注册到后台 admin 中
```py
    # DjangoService->api->admin.py
    from .models import Student #记得导包
    
    @admin.register(Student)
    class BlogTypeAdmin(admin.ModelAdmin):
        list_display = ('pk', 'name')    #在后台列表下显示的字段
```
#### 启动服务器
```
    python manage.py createsuperuser # 先创建管理员
    python manage.py runserver # 启动
```

#### 序列化
```py
    # DjangoService->api->serializers.py
    from .models import Student
    
    class StudentSerializers(serializers.ModelSerializer):
        class Meta:
            model = Student     #指定的模型类
            fields = ('pk', 'name', 'sex', 'sid',)   #需要序列化的属性
```

#### views.py 中编写视图
```py
    # DjangoService->api->view.py
    from rest_framework import viewsets
    from .models import Student
    from .serializers import StudentSerializers
    # Create your views here.
    
    class StudentViewSet(viewsets.ModelViewSet):
        # 指定结果集并设置排序 order_by是设置列表对主键的排序方式，可以把负号去掉采用升序
            queryset = Student.objects.all().order_by('-pk')
        # 指定序列化的类
            serializer_class = StudentSerializers
```
#### 设置 api 应用的路由
```py
    # DjangoService->api->urls.py
    from django.conf.urls import include,url
    from rest_framework import routers
    from api import views
    
    # 定义路由地址
    route = routers.DefaultRouter()
    
    # 注册新的路由地址
    route.register(r'student' , views.StudentViewSet)
    
    # 注册上一级的路由地址并添加
    urlpatterns = [
        url('api/', include(route.urls)),
    ]
```
#### 设置项目的路由
```py
    # DjangoService->DjangoService->urls.py
    from django.conf.urls import url, include
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
        url(r'^request', include('DjangoService.getAndPost.urls')),
        path('', include('api.urls')),    #添加的路由地址
    ]
```
#### 启动服务器
```
    python manage.py runserver # 启动
```
#### 测试
打开地址 http://127.0.0.1:8000/api/ 便可看到API的视图
```py
    http://127.0.0.1:8000/api/
```
#### 🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺🍺第一节完