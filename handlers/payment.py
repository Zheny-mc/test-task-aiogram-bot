import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from common.messages import MESSAGES

pay_route = Router()


PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
item_url = os.getenv('ITEM_URL')

PRICES = [
    LabeledPrice(label='Ноутбук', amount=1000),
    LabeledPrice(label='Прочная упаковка', amount=1000)
]

SUPERSPEED_SHIPPING_OPTION = ShippingOption(
    id='superspeed',
    title='Супер быстрая!',
    prices=[LabeledPrice(label='Лично в руки!', amount=1000)])

POST_SHIPPING_OPTION = ShippingOption(
    id='post',
    title='Почта России',
    prices=[
        LabeledPrice(label='Кортонная коробка', amount=1000),
        LabeledPrice(label='Срочное отправление!', amount=1000)
    ]
)


PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title='Самовывоз',
    prices=[
        LabeledPrice(label='Самовывоз в Сантк-Петербурге', amount=1000)
    ]
)

@pay_route.message(Command('payment'))
async def buy_process(message: Message):
    await message.answer_invoice(
                           title=MESSAGES['item_title'],
                           description=MESSAGES['item_description'],
                           provider_token=PAYMENTS_TOKEN,
                           currency='rub',
                           photo_url=item_url,
                           photo_height=512,
                           photo_width=512,
                           photo_size=512,
                           need_email=True,
                           need_phone_number=True,
                           is_flexible=True,
                           prices=PRICES,
                           example='gfhgfhfgh',
                           payload='some_invoice')

@pay_route.shipping_query(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery, bot: Bot):
    if shipping_query.shipping_address.country_code == 'AU':
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message=MESSAGES['AU_error']
        )

    shipping_options = [SUPERSPEED_SHIPPING_OPTION]

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(POST_SHIPPING_OPTION)

        if shipping_query.shipping_address.city == 'Санкт-Петербург':
            shipping_options.append(PICKUP_SHIPPING_OPTION)

    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )

@pay_route.pre_checkout_query(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@pay_route.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    print("SUCCESSFUL PAYMENT:")

    payment_info = message.successful_payment
    print(payment_info.currency)
    print(payment_info.total_amount / 100)
    print(payment_info.json())

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")