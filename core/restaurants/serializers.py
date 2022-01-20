from rest_framework import serializers

from restaurants.models import Domain


class DomainSerializer(serializers.Serializer):
    domain = serializers.CharField(required=True)

    def validate_domain(self, domain):
        new_domain = f'{domain}.{self.context.get("host")}'
        if not Domain.objects.filter(domain=new_domain).exists():
            return new_domain
        raise serializers.ValidationError()

    class Meta:
        model = Domain
        fields = ['domain']
