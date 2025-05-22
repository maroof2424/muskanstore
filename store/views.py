from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Feedback
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


def home(request):
    categories = Product._meta.get_field('category').choices
    products_by_category = {}

    # Fetch only 4 products per category
    for key, label in categories:
        products_by_category[label] = Product.objects.filter(category=key)[:4]  # Show only 4 per category

    return render(request, 'store/home.html', {'products_by_category': products_by_category})


def product_list(request):
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', 'all')

    # Start with all products
    products = Product.objects.all()

    # Filter by selected category if available
    if selected_category and selected_category != 'all':
        products = products.filter(category=selected_category)

    # Filter by search query if available
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Get category choices from model
    category_choices = Product._meta.get_field('category').choices

    return render(request, 'store/product.html', {
        'products': products,
        'search_query': search_query,
        'selected_category': selected_category,
        'categories': category_choices,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def feedback_view(request):
    products = Product.objects.all()
    feedbacks = Feedback.objects.all()

    if request.method == 'POST':
        if 'delete_id' in request.POST:
            # Deleting feedback
            feedback_id = request.POST.get('delete_id')
            feedback = get_object_or_404(Feedback, id=feedback_id)

            # Optional: Check if email matches before deleting
            input_email = request.POST.get('confirm_email')
            if input_email == feedback.email:
                feedback.delete()
                messages.success(request, "Feedback deleted successfully.")
            else:
                messages.error(request, "Email does not match. Cannot delete feedback.")

            return redirect('feedback')

        else:
            # Submitting new feedback
            name = request.POST.get('name')
            email = request.POST.get('email')
            product_id = request.POST.get('product')
            message = request.POST.get('message')
            rating = request.POST.get('rating')

            try:
                product = Product.objects.get(id=product_id)
                feedback = Feedback(
                    name=name,
                    email=email,
                    product=product,
                    comment=message,
                    rating=rating
                )
                feedback.save()
                messages.success(request, "Thank you for your feedback!")
            except Exception as e:
                print("Error:", e)
                messages.error(request, "Something went wrong. Please try again.")

            return redirect('feedback')

    return render(request, 'store/feedback.html', {'products': products, 'feedbacks': feedbacks})
def about(request):
    return render(request, 'store/about.html')


def register_view(request):
    if request.method == 'POST':
        # Getting data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    
    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page or wherever you need
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')