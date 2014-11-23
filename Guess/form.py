# -*- coding: utf-8 -*-
from django import forms

class ImageForm(forms.Form):
    image = forms.FileField(
        label='选择一张图片',
        help_text='图片不能大于2M'
    )