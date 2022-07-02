from core.celery import app

from .models import Bill, models, Client, Organization
from .services.fraud_detector import fraud_detector
from .services.classifier_of_services import classifier


@app.task(name='upload_bill_xls')
def upload_bill_xls(data: list) -> None:
    rows = []

    queryset = Bill.objects.all()

    data.pop(0)
    for row in data:
        classifier_data = classifier(row[5])
        service_class = list(classifier_data.keys())[0]  # в тз указано-что классификатор должен возвращать словарь
        service_name = list(classifier_data.values())[0]

        if not queryset.filter(
                models.Q(client_org=row[1]) | models.Q(number=row[2])
        ).exists():

            Bill.objects.create(client_name=row[0],
                                client_org=row[1],
                                number=row[2],
                                amount=row[3],
                                date=row[4],
                                service=row[5],
                                fraud_score=fraud_detector(row[5]),
                                service_class=service_class,
                                service_name=service_name,
                                )

        # Bill.objects.bulk_create(rows)


@app.task()
def upload_client_xls(data: tuple) -> None:
    client, organization = data[0], data[1]

    client.pop(0)
    organization.pop(0)

    for row in client:
        try:
            Client.objects.create(name=row[0])
        except Exception:
            continue

    for row in organization:
        try:

            Organization.objects.create(
                client_name=row[0],
                name=row[1],
                address=f'Адрес: {row[2]}' if row[2] else row[2],
            )
        except Exception:
            continue



