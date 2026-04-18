from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .forms import RegisterForm
from .models import Craft, Booking
from .serializers import CraftSerializer

# Главная
def home_view(request):
    return render(request, "backend/home.html")

# Список ремёсел
def craft_list_view(request):
    crafts = Craft.objects.all()
    return render(request, "backend/crafts.html", {"crafts": crafts})

# Детали ремесла
def craft_detail_view(request, pk):
    craft = get_object_or_404(Craft, pk=pk)
    return render(request, "backend/craft_detail.html", {"craft": craft})

# Заявка на мастер-класс
@login_required
def leave_request_view(request, pk):
    craft = get_object_or_404(Craft, pk=pk)
    if request.method == "POST":
        booking = Booking.objects.create(
            craft=craft,
            user=request.user,  # 🔥 сохраняем пользователя
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("comment"),
        )
        return redirect("backend:profile")  # после заявки → профиль
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
