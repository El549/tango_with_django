from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) # 隐藏字段，初始值为 0
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0) # 隐藏字段，初始值为 0
    slug = forms.CharField(widget=forms.HiddenInput(), required=False) # 隐藏字段，不是必需的
    
    # 内嵌类，提供表单的额外信息
    class Meta:
        # 为 ModelForm 做关联
        model = Category
        fields = ('name',) # 只有 name 字段是可见的

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='Please enter the title of the page.')
    url = forms.URLField(max_length=200, help_text='Please enter the URL of the page.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) # 隐藏字段，初始值为 0
    
    class Meta:
        # 为 ModelForm 做关联
        model = Page
        # 为表单提供需要的字段
        # 不包含外键字段，因为我们可以在表单中排除这些字段
        # 有些字段可能不想在表单中显示
        # 这些字段可以在 exclude 中指定
        # 或者指定 fields，而不是 exclude
        exclude = ('category',)
        # 或者指定 fields，而不是 exclude
        # fields = ('title', 'url', 'views')

    # 重写 clean() 方法，以便对 url 字段进行验证
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # 如果 url 字段不为空，且不以 'https://' 开头
        # 则在 url 字段前面加上 'https://'
        if url and not url.startswith('https://'):
            url = f'https://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class UserProfileFormModelForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)