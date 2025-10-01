from rest_framework import serializers

from openorganisatie.scim.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    scim_external_id = serializers.UUIDField(read_only=True)
    naam = serializers.CharField(source="name")
    beschrijving = serializers.CharField(source="description", allow_blank=True)
    is_active = serializers.BooleanField(source="active", read_only=True)

    class Meta:
        model = Group
        fields = ["scim_external_id", "naam", "beschrijving", "is_active"]
