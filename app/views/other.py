from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from app.form import ProductModelForm, FeedbackModelForm, PostModelForm
from app.models import Product, Blog, Post, Category, User


def index_view(request):
    products = Product.objects.order_by('-price')[:3]
    blogs = Blog.objects.all()
    return render(request=request,
                  template_name='app/main/index.html',
                  context={"products": products,
                           'blogs': blogs})


def shop_view(request):
    products = Product.objects.all()
    paginator = Paginator(object_list=products,
                          per_page=4)
    products_right = Product.objects.all()[:3]
    page_number = request.GET.get('page')
    product_list = paginator.get_page(number=page_number)
    query = request.GET.get('query', '')
    if request.GET.get("sort_by") == 'title':
        product_list = Product.objects.order_by('title')[:5]

    if request.GET.get("sort_by") == 'price':
        product_list = Product.objects.order_by('-price')[:5]

    if query:
        product_list = Product.objects.filter(Q(title__icontains=query) |
                                              Q(category__title__icontains=query))

    return render(request=request,
                  template_name='app/shop_main/shop.html',
                  context={"product_list": product_list,
                           "query": query,
                           'products_right': products_right})


def product_blog_details_page(request, blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    post_list = Post.objects.all().order_by('-created_at')[:3]
    blogs = Blog.objects.all()[:3]
    blog_list = Blog.objects.all()
    query = request.GET.get('query', '')
    if query:
        blog_list = Blog.objects.filter(title__icontains=query)

    if request.method == "POST":
        form = PostModelForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('product-blog-details-page', blog_id=blog.id)
    form = PostModelForm()

    return render(request=request,
                  template_name='app/blog_main/blog-details.html',
                  context={'blog': blog,
                           "form": form,
                           "post_list": post_list,
                           'blogs': blogs,
                           'blog_list': blog_list
                           })


def product_blog(request):
    blog_ = Blog.objects.all()
    products_right = Product.objects.all()[:3]
    paginator = Paginator(object_list=blog_,
                          per_page=4)
    page_number = request.GET.get('page')
    blog_list = paginator.get_page(number=page_number)
    query = request.GET.get('query', '')
    if request.GET.get('sort_by') == 'title':
        blog_list = Product.objects.order_by('title')

    if query:
        blog_list = Blog.objects.filter(title__icontains=query)

    return render(request=request,
                  template_name='app/blog_main/blog.html',
                  context={
                      "blog_list": blog_list,
                      'products_right': products_right})


def product_details_view(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    products = Product.objects.all()

    return render(request=request,
                  template_name='app/shop_main/product_details.html',
                  context={'product': product,
                           "products": products})


def add_product_view(request):
    categories = Category.objects.all()
    users = User.objects.all()
    if request.method == "POST":
        form = ProductModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('shop_main')
    form = ProductModelForm()
    return render(request=request,
                  template_name='app/add_product.html',
                  context={"form": form,
                           "categories": categories,
                           "users": users})


def edit_product(request, product_id):
    categories = Category.objects.all()
    users = User.objects.all()
    product = Product.objects.filter(id=product_id).first()
    if request.method == "POST":
        form = ProductModelForm(data=request.POST,
                                files=request.FILES,
                                instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if request.user.is_authenticated:
                product.user = request.user
            product.save(update_fields=['title', 'description', 'price', 'rank', 'image', 'category'])

            return redirect('product-details', product.id)

    form = ProductModelForm(instance=product)
    return render(request=request,
                  template_name='app/edit_product.html',
                  context={"form": form,
                           'users': users,
                           "categories": categories})


def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if product:
        product.delete()
        return redirect('shop_main')


def product_error404(request):
    return render(request=request,
                  template_name='app/shop_main/error404.html')


def product_compare_page(request):
    return render(request=request,
                  template_name='app/shop_main/compare_page.html')


def product_checkout_page(request):
    return render(request=request,
                  template_name='app/shop_main/checkout_page.html')


def product_frequently_questions(request):
    return render(request=request,
                  template_name='app/pages_main/frequently-questions.html')


def about_page(request):
    return render(request=request,
                  template_name='app/about.html')


def contact_page(request):
    if request.method == "POST":
        form = FeedbackModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = ProductModelForm()
    return render(request=request,
                  template_name='app/contact.html',
                  context={"form": form})


