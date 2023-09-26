
from django.contrib import admin
from django.urls import path,re_path
import article.views
import user.views
import comment.views

urlpatterns = [
    path('',article.views.index),
    path('admin/', admin.site.urls),
    path('list/', article.views.article_list, name = "list"),
    path('detail/<int:id>/', article.views.article_detail,name="detail"),  # 文章详情
    path('delete/<int:id>/', article.views.article_delete,name="delete"),#删
    path('create/', article.views.article_create, name='create'),#写文章
    path('update/<int:id>/',article.views.article_update,name="update"),#更新
    path('login/',user.views.user_login,name='login'),
    path('logout/',user.views.user_logout,name='logout'),

    path('register/',user.views.user_register, name='register'),
    path('post-comment/<int:article_id>/', comment.views.post_comment, name='post_comment' ),
]

