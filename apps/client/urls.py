from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import BillsViewSet, BillUploadView, ClientOrganizationUploadView, ClientViewSet

router = SimpleRouter()
router.register('bill', BillsViewSet)
router.register('client', ClientViewSet)

urlpatterns = [
    path('upload_bill/', BillUploadView.as_view(), name='upload_bill'),
    path('upload_client/', ClientOrganizationUploadView.as_view(), name='upload_client'),
] + router.urls
