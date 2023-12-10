from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
from dotenv import load_dotenv
import os
from functions import weiToUsdt, gweiToUsdt

load_dotenv()

router = Router()

@router.message(Command('choosechain'))
async def choosechain(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='BSC',
        callback_data='choosebsc')
    )
    builder.add(InlineKeyboardButton(
        text='Polygon',
        callback_data='choosepolygon')
    )
    builder.add(InlineKeyboardButton(
        text='Optimism',
        callback_data='chooseoptimism')
    )
    builder.add(InlineKeyboardButton(
        text='Base',
        callback_data='choosebase')
    )
    builder.add(InlineKeyboardButton(
        text='Etherium',
        callback_data='chooseeth')
    )
    await message.answer(
        'Выберите сеть из предложенных:',
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == 'choosebsc')
async def bscChoosed(message: Message):
    global currentChain
    currentChain = "BSC"
    global url
    url = "https://api.bscscan.com/api"
    global api_key
    api_key = os.getenv('BSC_API_KEY')
    global currentToken
    currentToken = "BNB"
    await message.answer(f"You are on {currentChain} now!")

@router.callback_query(F.data == 'choosepolygon')
async def bscChoosed(message: Message):
    global currentChain
    currentChain = "Polygon"
    global url
    url = "https://api.polygonscan.com/api"
    global api_key
    api_key = os.getenv('POL_API_KEY')
    global currentToken
    currentToken = "MATIC"
    await message.answer(f"You are on {currentChain} now!")

@router.callback_query(F.data == 'chooseeth')
async def bscChoosed(message: Message):
    global currentChain
    currentChain = "Etherium"
    global url
    url = "https://api.etherscan.io/api"
    global api_key
    api_key = os.getenv('ETH_API_KEY')
    global currentToken
    currentToken = "ETH"
    await message.answer(f"You are on {currentChain} now!")

@router.callback_query(F.data == 'chooseoptimism')
async def bscChoosed(message: Message):
    global currentChain
    currentChain = "Optimism"
    global url
    url = "https://api-optimistic.etherscan.io/api"
    global api_key
    api_key = os.getenv('OPT_API_KEY')
    global currentToken
    currentToken = "ETH"
    await message.answer(f"You are on {currentChain} now!")

@router.callback_query(F.data == 'choosebase')
async def bscChoosed(message: Message):
    global currentChain
    currentChain = "Base"
    global url
    url = "https://api.basescan.org/api"
    global api_key
    api_key = os.getenv('BASE_API_KEY')
    global currentToken
    currentToken = "ETH"
    await message.answer(f"You are on {currentChain} now!")

@router.message(Command('currentchain'))
async def currentChain(message: Message):
    global currentChain
    msg = "You are on " + currentChain + " now!"
    await message.answer(msg)

@router.message(Command('balance'))
async def balance(message: Message):
    action = "balance"
    address = list(message.text.split(' ')[1:])
    flag = True
    if len(address) != 1:
        action = "balancemulti"
        flag = False
    get = url + '?module=account&action=' + action + '&address=' + ",".join(address) + "&apikey=" + api_key
    response = requests.get(get)
    js = response.json()['result']
    if response.status_code != 200:
        await message.answer("Возникла ошибка! Проверьте правильность ввода команды: <code>/help balance</code>.")
    else:
        res = ""
        if not flag:
            for i in js:
                res += "Адрес: " + i["account"] + "\nБаланс: " + weiToUsdt(i["balance"]) + " " + currentToken + "\n\n"
        else:
            res = "Баланс: " + weiToUsdt(js) + " " + currentToken
        await message.answer(res)

@router.message(Command('range'))
async def _range(message: Message):
    params = message.text.split(' ')[1:]
    if len(params) != 3:
        await message.answer("Недостаточно параметров! Для просмотра необходимых параметров введите <code>/help range</code>.")
    else:
        get = url + f"?module=account&action=txlist&address={params[0]}&startblock={int(params[1])}&endblock={int(params[2])}&page=1&offset=10&sort=asc&apikey={api_key}"
        response = requests.get(get)
        js = response.json()['result']
        if response.status_code != 200:
            await message.answer("Возникла ошибка! Проверьте правильность ввода команды: <code>/help range</code>.")
        else:
            res = ""
            for i in js:
                res += f"Номер блока: {i['blockNumber']}\nХеш транзакции: {i['hash']}\nХеш блока: {i['blockHash']}\nОтправитель: {i['from']}\nПолучатель: {i['to']}\nКоличество: {weiToUsdt(i['value'])} {currentToken}\nГаз: {weiToUsdt(int(i['gasUsed']) * int(i['gasPrice']))} {currentToken}\n\n"
            if res == "":
                await message.answer("Транзакций по заданным параметрам не обнаружено! Попробуйте другой интервал блоков.")
            else:
                await message.answer(res)

@router.message(Command('smartbyhash'))
async def smartbyhash(message: Message):
    params = message.text.split(' ')[1:]
    if len(params) != 1:
        await message.answer("Введите пожалуйста только <b>ОДИН</b> хеш транзакции!")
    else:
        get = url + f"?module=account&action=txlistinternal&txhash={params}&apikey={api_key}"
        response = requests.get(get)
        if response.status_code != 200:
            await message.answer("Возникла ошибка! Проверьте правильность ввода команды: <code>/help range</code>.")
        else:
            js = response.json()['result']
            res = ""
            if len(js) != 1:
                for i in js:
                    if i['isError'] == '0':
                        res += "<b>Успешный смарт-контракт</b>\n"
                    else:
                        res += "<b>Провальный смарт-контракт</b>\n"
                    res += f"Номер блока: {i['blockNumber']}\nОтправитель: {i['from']}\nПолучатель: {i['to']}\n\n"
            else:
                if js['isError'] == '0':
                    res += "<b>Успешный смарт-контракт</b>\n"
                else:
                    res += "<b>Провальный смарт-контракт</b>\n"
                res += f"Номер блока: {js['blockNumber']}\nОтправитель: {js['from']}\nПолучатель: {js['to']}\n\n"
            if res == '':
                await message.answer("Смарт-контрактов по этой транзакции не существует. Попробуйте другую транзакцию.")
            else:
                await message.answer(res)

@router.message(Command('smartbyrange'))
async def smartbyrange(message: Message):
    params = message.text.split(' ')[1:]
    if len(params) != 2:
        await message.answer("Неверный формат ввода команды. Воспользуйтесь пожалуйста <code>/help smartbyhash</code> для просмотра формата команды.")
    else:
        get = url + f"?module=account&action=txlistinternal&startblock={params[0]}&endblock={params[1]}&page=1&offset=10&sort=asc&apikey={api_key}"
        response = requests.get(get)
        if response.status_code != 200:
            await message.answer("Ошибка, проверьте формат ввода команды. Используйте <code>/help smartbyrange</range> для просмотра.")
        else:
            res = ""
            js = response.json()['result']
            if len(js) != 1:
                for i in js:
                    res += f"Номер блока: {i['blockNumber']}\nХеш: {i['hash']}\nОтправитель: {i['from']}\nПолучатель: {i['to']}\nСумма: {weiToUsdt(i['value'])} {currentToken}\nТрейсID: {i['traceId']}\n\n"
            else:
                res += f"Номер блока: {js['blockNumber']}\nХеш: {js['hash']}\nОтправитель: {js['from']}\nПолучатель: {js['to']}\nСумма: {weiToUsdt(js['value'])} {currentToken}\nТрейсID: {js['traceId']}\n\n"
            if res == "":
                await message.answer("По данному диапазону смарт-контрактов не найдено!")
            else:
                await message.answer(res)

@router.message(Command('infosmart'))
async def infosmart(message: Message):
    params = message.text.split(' ')[1:]
    if params <= 0:
        await message.answer("Неверный ввод команды. Воспользуйтесь <code>/help infosmart</code> пожалуйста.")
    else:
        get = url + f"?module=contract&action=getcontractcreation&contractaddresses={','.join(params)}&apikey={api_key}"
        response = requests.get(get)
        if response.status_code != 200:
            await message.answer("Произошла ошибка. Повторите ещё раз через минуту, либо проверьте правильность ввода команды <code>/help infosmart</code>.")
        else:
            res = ""
            js = response.json()['result']
            if len(js) != 1:
                for i in js:
                   res += f"Адрес контракта: {i['contractAddress']}\nАдрес создателя: {i['contractCreator']}\nХеш транзакции: {i['txHash']}\n\n"
            else:
                res += f"Адрес контракта: {js['contractAddress']}\nАдрес создателя: {js['contractCreator']}\nХеш транзакции: {js['txHash']}"
            await message.answer(res)


@router.message(Command('transstatus'))
async def transstatus(message: Message):
    params = message.text.split(' ')[1:]
    if params >= 1:
        await message.answer("Статус возможно проверить для одной транзакции!")
    else:
        get = url + f"?module=transaction&action=getstatus&txhash={params}&apikey={api_key}"
        response = requests.get(get)
        if response.status_code != 200:
            await message.answer("Произошла ошибка. Повторите ещё раз через минуту, либо проверьте правильность ввода команды <code>/help transstatus</code>.")
        else:
            js = response.json()['result']
            res = ""
            if js['isError'] == '1':
                res = f"<b>Транзакция неуспешная.</b> Описание ошибки: \'{js['errDescription']}\'."
            else:
                res = "<b>Транзакция успешная.</b>"
            await message.answer(res)

@router.message(Command('totalbalanceoftoken'))
async def totalbalanceoftoken(message: Message):
    params = message.text.split(' ')[1:]
    get = url + f"?module=stats&action=tokensupply&contractaddress={params[0]}&apikey={api_key}"
    response = requests.get(get)
    if response.status_code != 200:
        await message.answer("Произошла ошибка. Повторите ещё раз через минуту, либо проверьте правильность ввода команды <code>/help transstatus</code>.")
    else:
        await message.answer(f"Баланс токена в сети: {response.json()['result'][:3]},{response.json()['result'][3:]}")

@router.message(Command('balanceoftoken'))
async def balanceoftoken(message: Message):
    params = message.text.split(' ')[1:]
    if len(params) != 2:
        await message.answer("Неверный формат ввода команды. Воспользуйтесь <code>/help balanceoftoken</code>")
    else:
        get = url + f"?module=account&action=tokenbalance&contactaddress={params[0]}&address={params[1]}&tag=latest&apikey={api_key}"
        response = requests.get(get)
        if response.status_code != 200:
            await message.answer("Произошла ошибка. Повторите ещё раз через минуту, либо проверьте правильность ввода команды <code>/help balanceoftoken</code>.")
        else:
            js = response.json()['result']
            await message.answer(f"Баланс токена: {js[:3]},{js[3:]}")

@router.message(Command('valueoftoken'))
async def valueoftoken(message: Message):
    get = url + f"?module=stats&action={currentToken.lower()}price&apikey={api_key}"
    response = requests.get(get)
    if response.status_code != 200:
        await message.answer("Произошла ошибка. Повторите ещё раз через минуту, либо проверьте правильность ввода команды <code>/help valueoftoken</code>.")
    else:
        await message.answer(f"Последняя цена токена {currentToken}: {response.json()['result']['ethusd']} $USD")

@router.message(Command('gas'))
async def gas(message: Message):
    get = url + f"?module=gastracker&action=gasoracle&apikey={api_key}"
    response = requests.get(get)
    if response.status_code != 200:
        await message.answer("Произошла ошибка. Повторите ещё раз через минуту, либо проверьте правильность ввода команды <code>/help gas</code>.")
    else:
        js = response.json()['result']
        await message.answer(f"<b>Цена безопасного газа:</b> {gweiToUsdt(js['SafeGasPrice'])} {currentToken}\n"
                             f"<b>Цена предлагаемого газа:</b> {gweiToUsdt(js['ProposeGasPrice'])} {currentToken}\n"
                             f"<b>Цена быстрого газа:</b> {gweiToUsdt(js['FastGasPrice'])} {currentToken}\n")

@router.message(F.text)
async def error(message: Message):
    await message.answer("Извините, я вас не понимаю. Пожалуйста воспользуйтесь командой /help, чтобы просмотреть что я умею!")


currentChain = "BSC"
url = "https://api.bscscan.com/api"
api_key = os.getenv('BSC_API_KEY')
currentToken = "BNB"