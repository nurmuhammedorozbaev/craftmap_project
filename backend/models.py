from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Region(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Craft(models.Model):
    CRAFT_TYPES = [
        ("wood", "Резьба по дереву"),
        ("metal", "Кузнечное дело"),
        ("felt", "Шырдак"),
        ("textile", "Ткачество"),
        ("jewelry", "Ювелирное дело"),
        ("ceramics", "Керамика"),
        ("embroidery", "Вышивка"),
        ("leather", "Кожевенное ремесло"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    history = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="crafts/", blank=True, null=True)
    craft_type = models.CharField(max_length=50, choices=CRAFT_TYPES, default="wood")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(default=42.8746)
    longitude = models.FloatField(default=74.5698)

    # 🔥 новые поля для отображения
    language = models.CharField(max_length=200, blank=True, null=True)   # Язык
    schedule = models.CharField(max_length=200, blank=True, null=True)   # Время работы
    price = models.CharField(max_length=200, blank=True, null=True)      # Стоимость
    experience = models.CharField(max_length=200, blank=True, null=True) # Опыт мастера
    craft_category = models.CharField(max_length=200, blank=True, null=True) # Тип ремесла

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(max_length=100)
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name="masters")
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.craft.name})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидание"),
        ("approved", "Одобрено"),
        ("completed", "Завершено"),
    ]

    craft = models.ForeignKey(Craft, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")  # 🔥 связь с профилем
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  # 🔥 статус

    def __str__(self):
        return f"Бронь {self.craft.name} от {self.name}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ("master", "Мастер ремесла"),
        ("visitor", "Посетитель"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="visitor")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    # 🔥 Методы для статистики заявок
    def bookings_all(self):
        return self.user.bookings.all()

    def bookings_pending(self):
        return self.user.bookings.filter(status="pending")

    def bookings_approved(self):
        return self.user.bookings.filter(status="approved")

    def bookings_completed(self):
        return self.user.bookings.filter(status="completed")

    def bookings_today(self):
        return self.user.bookings.filter(created_at__date=timezone.now().date())
