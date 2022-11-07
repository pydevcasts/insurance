from django import forms
from category.models import Category
from django.utils.translation import gettext_lazy as _

        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ("slug",)


# class SubCategoryForm(forms.ModelForm):
#     class Meta:
#         model = SubCategory
#         exclude = ("slug",)

     