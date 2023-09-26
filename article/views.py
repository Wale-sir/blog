from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
# 导入数据模型Article
from .models import Article
from comment.models import Comment
# 引入redirect用于重定向地址
from django.shortcuts import render, redirect
# 引入刚才定义的ArticleForm表单类
from .forms import ArticleForm


#查看全部文章
def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        article_list = Article.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = Article.objects.all().order_by('created')
        order = 'created'

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 修改此行
    context = { 'articles': articles, 'order': order }

    return render(request, 'article/list.html', context)

def index(request):
    return render(request,'index.html')

# 文章详情

# 文章详情
def article_detail(request,id):
    # 取出相应的文章
    article = Article.objects.get(id=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 需要传递给模板的对象
    context = {'article': article, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)
# 删文章
def article_delete(request, id):
    print(request.method)
    if request.method == 'POST':
        # 根据 id 获取需要删除的文章
        article = Article.objects.get(id=id)
        # 调用.delete()方法删除文章
        article.delete()
        return redirect("list")
    else:
        return HttpResponse("仅允许post请求")

# 写文章的视图
def article_create(request):
    try:
        # 判断用户是否提交数据
        if request.method == "POST":
            # 将提交的数据赋值到表单实例中
            article_post_form = ArticleForm(data=request.POST)
            # 判断提交的数据是否满足模型的要求
            if article_post_form.is_valid():
                # 保存数据，但暂时不提交到数据库中
                new_article = article_post_form.save(commit=False)
                # 作者为当前请求的用户名
                new_article.author = request.user
                # 将新文章保存到数据库中
                new_article.save()
                # 完成后返回到文章列表
                return redirect("list")
            # 如果数据不合法，返回错误信息
            else:
                return HttpResponse("表单内容有误，请重新填写。")
        # 如果用户请求获取数据
        else:
            # 创建表单类实例
            article_post_form = ArticleForm()
            # 赋值上下文
            context = { 'article_post_form': article_post_form }
            # 返回模板
            return render(request, 'article/create.html', context)
    except ValueError:
        return HttpResponse("用户不能为空,请返回登录")
# 更新文章
def article_update(request, id):

    # 获取需要修改的具体文章对象
    article = Article.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticleForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)