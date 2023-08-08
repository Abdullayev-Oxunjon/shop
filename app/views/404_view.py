from django.shortcuts import render


# custom 404 view
def custom_404(request, exception):
    return render(request, 'app/shop_main/error404.html', status=404)
