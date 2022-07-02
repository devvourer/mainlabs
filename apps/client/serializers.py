from rest_framework import serializers

from .models import Client, Organization, Bill

from functools import reduce


class OrganizationSerializer(serializers.ModelSerializer):
    fraud_weight = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    def get_fraud_weight(self, obj):
        weight = 0
        queryset = Bill.objects.filter(client_org=obj.name)

        for i in queryset:
            if float(i.fraud_score) >= 0.9:
                weight += 1


class ClientSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_organizations(self, obj):
        return Organization.objects.filter(client_name=obj.name).count() or 0

    def get_income(self, obj):
        organizations = Organization.objects.filter(client_name=obj.name)
        income: float = 0
        for i in organizations:
            bills = Bill.objects.filter(client_org=i.name).values_list('amount').distinct()
            income += float(reduce(lambda x, y: float(x) + float(y), bills)[0])

        return income


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'