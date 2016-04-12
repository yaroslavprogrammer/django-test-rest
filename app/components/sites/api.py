from rest_framework import viewsets, permissions
from rest_framework import serializers

from .models import Site


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = ['url', 'is_private']


class SiteAPIViewSet(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.none()
    # permissions = (permissions.DjangoModelPermissioznsOrAnonReadOnly,)

    def get_queryset(self):
        sites = Site.objects.all()

        if not self.request.user.is_authenticated():
            return sites.filter(is_private=False)

        return sites
