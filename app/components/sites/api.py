from rest_framework import viewsets, permissions
from rest_framework import serializers

from .models import Site


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = ['url', 'is_private']


class SitePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated() and \
                request.user.username == 'manager':
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated() and obj.is_private:
            return False

        return True


class SiteAPIViewSet(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.none()
    permission_classes = (SitePermissions,)

    def get_queryset(self):
        sites = Site.objects.all()

        if not self.request.user.is_authenticated():
            return sites.filter(is_private=False)

        return sites
