from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from django.http import JsonResponse
from product_app.models import Product
from rest_framework.response import Response
from product_app.serializers import ProductSerializer
from django.urls import reverse
from rest_framework import viewsets
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from product_app.forms import AddProductForm

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def by_id(self, request):
        product_id = request.query_params.get('id')
        product = get_object_or_404(Product, id=product_id)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def product_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


@csrf_exempt
@login_required(login_url='/login/')
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']

            # Create the product
            product = Product.objects.create(name=name, quantity=quantity, price=price)

            # Return success response
            return JsonResponse({'success': True, 'url': reverse('products')})

        # Return form errors
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})

    form = AddProductForm()
    return render(request, 'products.html')


@login_required(login_url='/login/')
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        if request.method == 'POST':
            product.delete()
            return redirect('products')
    except Product.DoesNotExist:
        return redirect('products')

    return render(request, 'delete_product.html')


@login_required(login_url='/login/')
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(instance=product, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('products')
        return JsonResponse(serializer.errors, status=400)
