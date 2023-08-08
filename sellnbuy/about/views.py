from django.shortcuts import render


def author_page(request):
    return render(request, 'about/about-author.html')


def techs(request):
    return render(request, 'about/techs.html')
