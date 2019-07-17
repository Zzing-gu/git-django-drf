from rest_framework import serializers




class TreeSerializer(serializers.Serializer):
    Name = serializers.CharField(max_length=200)
    Mode = serializers.CharField(max_length=200)
    Hash = serializers.CharField(max_length=200)
    