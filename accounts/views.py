from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
import boto3
import json
import uuid
from .forms import UserRegistrationForm, OrderForm
from .models import Order
from .utils import trigger_order_alert
from sqs_handler import SQSHandler

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now login with your credentials.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

@login_required
def home(request):
    if request.user.is_superuser:
        # Admin sees all orders
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Regular users see only their orders
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'home.html', context)

# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()
            
#             # Trigger the Lambda API alert
#             success, message = trigger_order_alert(order)
#             if success:
#                 messages.success(request, 'Order created successfully and alert triggered!')
#             else:
#                 messages.warning(request, f'Order created but alert failed: {message}')
            
#             return redirect('home')
#     else:
#         form = OrderForm()
#     return render(request, 'accounts/create_order.html', {'form': form})


# Initialize the SQS client
# sqs = boto3.client('sqs', region_name='us-east-1')

# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST, request.FILES)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user

#             # Upload image to S3 if provided
#             image_file = request.FILES.get('image')
#             if image_file:
#                 s3 = boto3.client('s3', region_name='us-east-1')
#                 image_key = f"orders/{uuid.uuid4()}_{image_file.name}"
#                 try:
#                     s3.upload_fileobj(
#                         image_file,
#                         'trackeasy',  # S3 bucket name
#                         image_key
#                     )
#                     order.image_url = f"https://trackeasy.s3.amazonaws.com/{image_key}"
#                 except Exception as e:
#                     messages.error(request, f"Failed to upload image: {str(e)}")
#                     return render(request, 'accounts/create_order.html', {'form': form})

#             order.save()

#             # Send message to SQS with order details
#             try:
#                 queue_url = "https://sqs.us-east-1.amazonaws.com/975049962424/vehicle-orders-queue"
#                 message_body = {
#                     "order_id": order.id,
#                     "user": order.user.username,
#                     "destination": order.destination,
#                     "goods_type": order.goods_type,
#                     "status": order.status,
#                     "image_url": order.image_url,
#                     "created_at": str(order.created_at),
#                 }
#                 sqs_response = sqs.send_message(
#                     QueueUrl=queue_url,
#                     MessageBody=json.dumps(message_body),
#                     MessageAttributes={
#                         "OrderId": {
#                             "DataType": "String",
#                             "StringValue": str(order.id)
#                         },
#                         "User": {
#                             "DataType": "String",
#                             "StringValue": order.user.username
#                         },
#                         "Status": {
#                             "DataType": "String",
#                             "StringValue": order.status
#                         },
#                     }
#                 )
#                 print("SQS Send Message Response:", sqs_response)
#                 messages.success(request, 'Order created successfully and sent to the queue!')
#             except Exception as e:
#                 messages.warning(request, f"Order created, but failed to send to SQS: {str(e)}")

#             return redirect('home')
#     else:
#         form = OrderForm()
#     return render(request, 'accounts/create_order.html', {'form': form})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Upload image to S3 if provided
            image_file = request.FILES.get('image')
            if image_file:
                s3 = boto3.client('s3', region_name='us-east-1')
                image_key = f"orders/{uuid.uuid4()}_{image_file.name}"
                try:
                    s3.upload_fileobj(
                        image_file,
                        'trackeasy',  # S3 bucket name
                        image_key
                    )
                    order.image_url = f"https://trackeasy.s3.amazonaws.com/{image_key}"
                except Exception as e:
                    messages.error(request, f"Failed to upload image: {str(e)}")
                    return render(request, 'accounts/create_order.html', {'form': form})

            order.save()

            # Use SQSHandler to send message to SQS
            sqs = SQSHandler(region_name='us-east-1')  # Initialize the SQSHandler
            queue_url = "https://sqs.us-east-1.amazonaws.com/975049962424/vehicle-orders-queue"
            message_body = {
                "order_id": order.id,
                "user": order.user.username,
                "destination": order.destination,
                "goods_type": order.goods_type,
                "status": order.status,
                "image_url": order.image_url,
                "created_at": str(order.created_at),
            }

            try:
                sqs_response = sqs.send_message(
                    queue_url=queue_url,
                    message_body=message_body,
                    message_attributes={
                        "OrderId": {
                            "DataType": "String",
                            "StringValue": str(order.id)
                        },
                        "User": {
                            "DataType": "String",
                            "StringValue": order.user.username
                        },
                        "Status": {
                            "DataType": "String",
                            "StringValue": order.status
                        },
                    }
                )
                print("SQS Send Message Response:", sqs_response)
                messages.success(request, 'Order created successfully and sent to the queue!')
            except RuntimeError as e:
                messages.warning(request, f"Order created, but failed to send to SQS: {str(e)}")

            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'accounts/create_order.html', {'form': form})


@login_required
def view_order(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
    if request.method == 'POST' and request.user.is_superuser:
        form_type = request.POST.get('form_type')
        
        if form_type == 'vehicle_assignment':
            # Handle vehicle and driver assignment
            assigned_vehicle = request.POST.get('assigned_vehicle')
            driver_name = request.POST.get('driver_name')
            driver_contact = request.POST.get('driver_contact')
            
            if assigned_vehicle and driver_name and driver_contact:
                order.assigned_vehicle = assigned_vehicle
                order.driver_name = driver_name
                order.driver_contact = driver_contact
                order.save()
                messages.success(request, 'Vehicle and driver assigned successfully!')
            else:
                messages.error(request, 'Please fill in all fields for vehicle and driver assignment.')
        else:
            # Handle status update
            new_status = request.POST.get('status')
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                messages.success(request, f'Order status updated to {order.get_status_display()}')
        
        return redirect('view_order', order_id=order.id)
    
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES
    }
    return render(request, 'accounts/view_order.html', context)

@user_passes_test(lambda u: u.is_superuser)
def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Handle search and filtering
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        orders = orders.filter(
            Q(user__username__icontains=search_query) |
            Q(destination__icontains=search_query) |
            Q(goods_type__icontains=search_query)
        )
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_search': search_query,
        'current_status': status_filter
    }
    return render(request, 'accounts/manage_orders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status selected')
            
    return redirect('manage_orders')

@login_required
def delete_order(request, order_id):
    # Get the order object for the current user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if the order status is pending
    if order.status == 'pending':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
    else:
        messages.error(request, f'Order cannot be deleted as it is already {order.get_status_display()}')
    
    return redirect('home')
