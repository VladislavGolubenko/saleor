import os

from celery import Celery
from django.conf import settings
# from saleor import settings as s

from .plugins import discover_plugins_modules
from celery.schedules import crontab

from product.models import (
    Category,
    ProductType,
    ProductVariant,
    ProductImage,
    VariantImage,
    Product,
)



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")

app = Celery("saleor")

app.conf.timezone = 'UTC'

app.config_from_object("django.conf:settings", namespace="CELERY")



app.autodiscover_tasks(lambda: discover_plugins_modules(settings.PLUGINS))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s(), name='generate xml every day')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

@app.task
def test():
    print(f'{settings.MEDIA_URL}parse.xml')


    all_products = Product.objects.all()

    path = f'{settings.MEDIA_URL}parse.xml'
    # os.path.isfile(path)
# W+t
    file = open(f'media/parse.xml', mode='w', encoding='utf-8')

    file.write("< Ads formatVersion = \"3\" target = \"Avito.ru\" >")

    for product in all_products:

        file.write(f"< Ad >< Id > {product.id} < / Id >")
        file.write("< DateBegin > 2015 - 11 - 27 < / DateBegin >") #Возможно тут нужно поставить сегоднешний день и дата через месяц
        file.write("< DateEnd > 2079 - 08 - 28 < / DateEnd >")
        file.write("< AdStatus > TurboSale < / AdStatus >")
        file.write("< AllowEmail > Да < / AllowEmail >")
        file.write("< ManagerName > Необходимо вписать имя мэнеджера< / ManagerName >")
        file.write("< ContactPhone > телефон менеджера < / ContactPhone >")
        file.write(
            " < Address >Адрес магазина< / Address >")
        file.write("< Category > Одежда, обувь, аксессуары < / Category >")
        file.write("< GoodsType > Женская одежда < / GoodsType >")
        file.write("< Condition > Новое < / Condition >")
        file.write("< AdType > Товар приобретен напродажу < / AdType >")
        file.write("< Apparel > Платья и юбки < / Apparel >")
        file.write("< Size > S < / Size >")
        # file.write(f"< Title > {product.name} < / Title >")
        # file.write(
        #     f"< Description > {product.description} < / Description >")
        # file.write(f"< Price > {product.minimal_variant_price_amount} < / Price >")
        # file.write(
        #     f"< Images >< Image url = \"{MEDIA_URL}{product.id__image}\" / >< "
        #     "Image url = \"http://img.test.ru/8F7B-4A4F3A0F2XA3.jpg\" / >< / Images >")
        file.write("< VideoURL < / VideoURL >< / Ad >")


    file.write("< / Ads >")

    file.close()
    return "файл записан успешно"
















# app.conf.beat_schedule = {
#
#     'qwerty':{
#         'task':'product.tasks.generate_xml',
#         'schedule': 60.0,
#     }
# }








