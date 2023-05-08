import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # 首先创建一些字典，列出想添加到各分类的网页
    # 然后创建一个嵌套字典，设置各分类
    # 这么做看起来不易理解，但是便于迭代，方便为模型添加数据
    python_pages = [
        {'title': 'Official Python Tutorial',
            'url':'http://docs.python.org/3/tutorial/',
            'views': 128},
        {'title':'How to Think like a Computer Scientist',
            'url':'http://www.greenteapress.com/thinkpython/',
            'views': 64},
        {'title':'Learn Python in 10 Minutes',
            'url':'http://www.korokithakis.net/tutorials/python/',
            'views': 32} ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
            'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
            'views': 128},
        {'title':'Django Rocks',
            'url':'http://www.djangorocks.com/',
            'views': 64},
        {'title':'How to Tango with Django',
            'url':'http://www.tangowithdjango.com/',
            'views': 32} ]
    
    other_pages = [
        {'title':'Bottle',
            'url':'http://bottlepy.org/docs/dev/',
            'views': 128},
        {'title':'Flask',
            'url':'http://flask.pocoo.org',
            'views': 64} ]
    
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }
    
    # 如果想添加更多分类或网页，添加到前面的字典中即可

    # 下述代码迭代 cats 字典，添加各分类，并把相关的网页添加到分类中
    # 如果使用的是 Python 2.x，要使用 cats.iteritems() 迭代
    # 迭代字典时，使用 items() 方法返回一个键-值对列表
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # 打印添加的分类
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

# 程序从这里开始执行
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()