import django.forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, ItemDetail


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateItemForm(ModelForm):
    class Meta:
        model = ItemDetail
        fields = ['name', 'image', 'location', 'item_status', 'dateFL', 'description']

    def __init__(self, *args, **kwargs):
        super(CreateItemForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

