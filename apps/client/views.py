from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Client, Bill
from .utils import get_data_from_xls, get_data_from_client_xls
from .tasks import upload_bill_xls, upload_client_xls
from .serializers import (BillSerializer,
                          ClientSerializer,
                          )


class BillsViewSet(GenericViewSet, ListModelMixin):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client_name', 'client_org']


class BillUploadView(APIView):

    def post(self, request):
        file = request.FILES['file']
        data = get_data_from_xls(file)
        upload_bill_xls.delay(data)
        return Response(status=status.HTTP_200_OK)


class ClientViewSet(GenericViewSet, ListModelMixin):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientOrganizationUploadView(APIView):

    def post(self, request):
        file = request.FILES['file']
        data = get_data_from_client_xls(file)
        upload_client_xls.delay(data)
        return Response(status=status.HTTP_200_OK)