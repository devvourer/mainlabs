import random

choices = {1: 'консультация',
           2: 'лечение',
           3: 'стационар',
           4: 'диагностика',
           5: 'лаборатория'}


def classifier(data: str) -> dict:
    service_class, service_name = random.choice(list(choices.items()))
    return {service_class: service_name}
