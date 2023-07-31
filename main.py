import asyncio
import time

import telegram
import requests
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def ask_for_tickets():
    url = "https://ticket.vanillasky.ge/en/tickets"
    date = "08%2F01%2F2023"
    person_count = "1"
    payload = f'types=0&departure=6&date_picker={date}&arrive=7&date_picker_arrive={date}&person_count={person_count}&person_types%5Badult%5D={person_count}&person_types%5Bchild%5D=0&person_types%5Binfant%5D=0&op=&form_build_id=form-K6gjO3mMnfAOnbkoH4E8UckLTUCVMnFflaqe3etKYfQ&form_id=form_select_date'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'SSESS19ed0dfa54df7b3399e8497846ea071f=OCJRSz9ON3qhogM0P5lv3jHC-wITI7vmFHEpQMtiBmU',
        'Origin': 'https://ticket.vanillasky.ge',
        'Referer': 'https://ticket.vanillasky.ge/en/tickets',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    no_tickets_string = "There are no available tickets. Please choose different dates."
    result = ''
    if no_tickets_string not in response.text:
        result = 'Mestia-Natakhari tickets found! Go to https://ticket.vanillasky.ge/en/tickets'

    if result:
        asyncio.run(
            telegram_send_msg(result)
        )


async def telegram_send_msg(message):
    bot = telegram.Bot("6411070462:AAEqo0pv54mnXTBfId5ClBD6YOHY5iQrhgA")
    async with bot:
        await bot.send_message(text=str(message), chat_id=415205954)


async def bot_updates():
    bot = telegram.Bot("6411070462:AAEqo0pv54mnXTBfId5ClBD6YOHY5iQrhgA")
    async with bot:
        print(
            await bot.get_updates()
        )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        ask_for_tickets()
        time.sleep(180)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

