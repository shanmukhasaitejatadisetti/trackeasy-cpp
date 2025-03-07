from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class OrderForm(forms.ModelForm):
#     preferred_delivery_date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         help_text='Select your preferred delivery date'
#     )
#     delivery_requirements = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 3}),
#         required=False,
#         help_text='Optional: Specify any special delivery requirements (e.g., temperature control)'
#     )

#     class Meta:
#         model = Order
#         fields = ['destination', 'goods_type', 'delivery_requirements', 'preferred_delivery_date']
#         widgets = {
#             'destination': forms.TextInput(attrs={'class': 'form-control'}),
#             'goods_type': forms.TextInput(attrs={'class': 'form-control'}),
#         }

class OrderForm(forms.ModelForm):
    preferred_delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select your preferred delivery date'
    )
    delivery_requirements = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text='Optional: Specify any special delivery requirements (e.g., temperature control)'
    )
    # image = forms.ImageField(
    #     required=False,
    #     help_text='Optional: Upload an image for delivery instructions'
    # )

    class Meta:
        model = Order
        # fields = ['destination', 'goods_type', 'delivery_requirements', 'preferred_delivery_date', 'image']
        fields = ['destination', 'goods_type', 'delivery_requirements', 'preferred_delivery_date']
        widgets = {
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'goods_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VehicleAssignmentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['assigned_vehicle', 'driver_name', 'driver_contact']
        widgets = {
            'assigned_vehicle': forms.Select(attrs={'class': 'form-control'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter driver name'}),
            'driver_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter driver contact number'}),
        }