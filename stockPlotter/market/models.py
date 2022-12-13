from django.db import models


class API(models.Model):
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    website = models.CharField(max_length=200)


class Security(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=100)

    STOCKS = 'ST'
    FUTURES = 'FU'
    FOREX = 'FO'
    CRYPTO = 'CR'
    INDICES = 'IN'
    BONDS = 'BO'
    ECONOMY = 'EC'

    type_choices = [
        (STOCKS, 'STOCKS'),
        (FUTURES, 'FUTURES'),
        (FOREX, 'FOREX'),
        (CRYPTO, 'CRYPTO'),
        (INDICES, 'INDICES'),
        (BONDS, 'BONDS'),
        (ECONOMY, 'ECONOMY')
    ]

    type = models.CharField(
        max_length=2,
        choices=type_choices,
        default='ST',
    )

    api_in_use = models.ForeignKey(API, on_delete=models.CASCADE, default=1)


# AK7RILN05QJRJBHV