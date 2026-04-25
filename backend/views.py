from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .forms import RegisterForm, ReviewForm
from .models import Craft, Booking, Profile, Review
from .serializers import CraftSerializer

# Главная
def home_view(request):
    crafts_count = Craft.objects.count()
    regions_count = Craft.objects.values("region").distinct().count()
    masters_count = Profile.objects.count()

    return render(request, "backend/home.html", {
        "crafts_count": crafts_count,
        "regions_count": regions_count,
        "masters_count": masters_count,
    })

# Список ремёсел с фильтрацией
def craft_list_view(request):
    crafts = Craft.objects.all()

    # фильтрация по названию
    search_query = request.GET.get("search")
    if search_query:
        crafts = crafts.filter(name__icontains=search_query)

    # фильтрация по категории ремесла
    craft_category = request.GET.get("craft_category")
    if craft_category and craft_category != "Все категории":
        crafts = crafts.filter(craft_category=craft_category)

    # фильтрация по типу ремесла
    craft_type = request.GET.get("craft_type")
    if craft_type and craft_type != "Все типы":
        crafts = crafts.filter(craft_type=craft_type)

    # фильтрация по региону
    region = request.GET.get("region")
    if region and region != "Все регионы":
        crafts = crafts.filter(region__name=region)

    # для выпадающих списков
    categories = Craft.objects.values_list("craft_category", flat=True).distinct()
    types = Craft.objects.values_list("craft_type", flat=True).distinct()
    regions = Craft.objects.values_list("region__name", flat=True).distinct()

    return render(request, "backend/crafts.html", {
        "crafts": crafts,
        "categories": categories,
        "types": types,
        "regions": regions,
    })

# Детали ремесла + отзывы
def craft_detail_view(request, pk):
    craft = get_object_or_404(Craft, pk=pk)
    reviews = craft.reviews.all()  # все отзывы для этого ремесла
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.craft = craft
            review.user = request.user
            review.save()
            return redirect("backend:craft_detail", pk=craft.pk)

    return render(request, "backend/craft_detail.html", {
        "craft": craft,
        "reviews": reviews,
        "form": form,
    })

# Заявка на мастер-класс
@login_required
def leave_request_view(request, pk):
    craft = get_object_or_404(Craft, pk=pk)
    if request.method == "POST":
        booking = Booking.objects.create(
            craft=craft,
            user=request.user,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("comment"),
        )
        return redirect("backend:profile")
    return render(request, "backend/leave_request.html", {"craft": craft})

# Карта
def map_view(request):
    return render(request, "backend/map.html")

# Регистрация
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role="visitor")
            login(request, user)
            return redirect("backend:home")
    else:
        form = RegisterForm()
    return render(request, "backend/register.html", {"form": form})

# Вход
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("backend:home")
    else:
        form = AuthenticationForm()
    return render(request, "backend/login.html", {"form": form})

# Выход
def logout_view(request):
    logout(request)
    return redirect("backend:home")

# Профиль с заявками
@login_required
def profile_view(request):
    status_filter = request.GET.get("status")
    bookings = request.user.bookings.all()

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, "backend/profile.html", {
        "bookings": bookings,
        "status_filter": status_filter,
    })

# --- API для ремёсел ---
class CraftViewSet(viewsets.ModelViewSet):
    queryset = Craft.objects.all()
    serializer_class = CraftSerializer
