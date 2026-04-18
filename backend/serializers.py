from rest_framework import serializers
from .models import Craft, Region, Master, Booking, Profile

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"

class CraftSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Craft
        fields = "__all__"

class MasterSerializer(serializers.ModelSerializer):
    craft = serializers.StringRelatedField()

    class Meta:
        model = Master
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    craft = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = "__all__"
