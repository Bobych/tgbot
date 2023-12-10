from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('help'))
async def help(message: Message):
    str = message.text.split(' ')
    obj = ""
    if len(str) != 1:
        obj = str[1]
    if(obj == "balance"):
        await message.answer("Формат запроса баланса: <code>/balance ADDRESS ADDRESS</code>.")
    elif (obj == "range"):
        await message.answer("Формат запроса: <code>/range ADDRESS START END</code>, где START - начальный блок, END - конечный блок.")
    elif obj == "smartbyhash":
        await message.answer("Формат запроса: <code>/smartbyhash HASH</code>, где HASH - хеш смарт-конракта..")
    elif obj == "smartbyrange":
        await message.answer("Формат запроса: <code>/smartbyrange START END</code>, где START - начальный блок, END - конечный блок.")
    elif obj == "infosmart":
        await message.answer("Формат запроса: <code>/infosmart ADDRESS</code>, где ADDRESS - адрес контракта.")
    elif obj == 'transstatus':
        await message.answer("Формат запроса: <code>/transstatus HASH</code>, где HASH - хеш транзакции.")
    elif obj == 'totalbalanceoftoken':
        await message.answer("Формат запроса: <code>/totalbalanceoftoken CONTRACT</code>, где CONTRACT - адрес контракта токена.")
    elif obj == 'balanceoftoken':
        await message.answer("Формат запроса: <code>/balanceoftoken CONTRACT ADDRESS</code>, где CONTRACT - адрес конракта токена, ADDRESS - адрес для проверки токена в нём.")
    elif obj == 'valueoftoken':
        await message.answer("Формат запроса: <code>/valueoftoken</code>.")
    elif obj == 'gas':
        await message.answer("Формат запроса: <code>/gas</code>.")
    else:
        await message.answer("У меня есть следующие команды:\n"
                             "- <code>/choosechain</code> : выбрать сеть из предложенных;\n"
                             "- <code>/currentchain</code> : текущая сеть;\n"
                             "- <code>/balance</code> : баланс токена сети по адресу или адресам;\n"
                             "- <code>/range</code> : транзакции адреса в интервале блоков;\n"
                             "- <code>/smartbyhash</code> : смарт-конракты по хешу транзакции;\n"
                             "- <code>/smartbyrange</code> : смарт-контракты адреса в интервале блоков;\n"
                             "- <code>/infosmart</code> : создатель, хеш по адресу или адресам смарт-контрактов;\n"
                             "- <code>/transstatus</code> : проверить статус транзакции;\n"
                             "- <code>/totalbalanceoftoken</code> : баланс токена в сети по его контракту;\n"
                             "- <code>/balanceoftoken</code> : баланс токена на адресе по его контракту;\n"
                             "- <code>/valueoftoken</code> : цена токена сети;\n"
                             "- <code>/gas</code> : цена за газ;")