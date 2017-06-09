from rest_framework import serializers


class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=15, required=False,
                                       allow_blank=True)
    last_name = serializers.CharField(max_length=15, required=False,
                                      allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(max_length=10, required=False,
                                   allow_blank=True)

    def update(self, instance, validated_data):
        if validated_data.get('first_name', instance.first_name) != '':
            instance.first_name = validated_data.get('first_name',
                                                     instance.first_name)
        if validated_data.get('last_name', instance.last_name) != '':
            instance.last_name = validated_data.get('last_name',
                                                    instance.last_name)
        if validated_data.get('phone', instance.phone) != '':
            instance.phone = validated_data.get('phone', instance.phone)
        if validated_data.get('gender', instance.gender) != '':
            instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance
