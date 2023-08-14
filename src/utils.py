import json
from datetime import datetime


def load_card_transactions():
    """Считывает данные из файла, возвращает список всех операций по карте"""

    with open('operations.json', 'r', encoding='utf-8') as file:
        transactions = json.loads(file.read())
    return transactions


def format_date(transaction):
    """Принимает словарь и преобразует по ключу формат даты в 'дд-мм-гггг'"""
    date_str = transaction["date"]
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
    formatted_date = date_obj.strftime('%d.%m.%Y')
    return formatted_date


def masked_card_number(transaction):
    """
    Принимаеи словарь и преобразует по ключу 'from' номер карты/счёта отправителя
    в соответствии с заданным форматом
    """

    card_parts = transaction['from'].split(' ')
    card_number = card_parts[-1]

    if card_parts[0] == 'Счет':
        masked_card = 'Счет **' + card_number[-4:]
    else:
        masked_number = f'{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}'
        masked_card = ' '.join(card_parts[:-1]) + ' ' + masked_number
    return masked_card


def masked_account_number(transaction):
    """
    Принимаеи словарь и преобразует по ключу 'to' номер счёта получателя
    в соответствии с заданным форматом
    """

    account_parts = transaction['to'].split(' ')
    account_number = account_parts[1]
    masked_account = 'Счет **' + account_number[-4:]

    return masked_account


def date_key(dictionary):
    """
    Извлекает дату из словаря и преобразует её в объект datetime.
    Возвращает компаратор для сортировки по дате.
    """
    return datetime.strptime(dictionary["date"], '%d.%m.%Y')


def sorted_transactions_with_formatted_data():
    """Заменяет формат данных на требуемый, сортирует и возвращает изменённый список"""
    data = load_card_transactions()
    transactions = []

    for transaction in data:

        if 'date' in transaction:
            transaction['date'] = format_date(transaction)
        if 'from' in transaction:
            transaction['from'] = masked_card_number(transaction)
        if 'to' in transaction:
            transaction['to'] = masked_account_number(transaction)

            transactions.append(transaction)

    sorted_data = sorted(transactions, key=date_key, reverse=True)
    return sorted_data


def executed_transactions():
    """Возвращает список исполненных операций"""

    sorted_data = sorted_transactions_with_formatted_data()
    executed = []

    for item in sorted_data:
        if item['state'] == 'EXECUTED':
            executed.append(item)
    return executed


def format_and_print_transaction(transaction):
    """Принимает словарь и печатает данные по требуемому шаблону"""

    date = transaction['date']

    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["name"]

    description = transaction["description"]

    from_account = transaction["from"]
    to_account = transaction["to"]

    output = f"{date} {description}\n{from_account} -> {to_account}\n{amount:.2f} {currency}"
    print(output)
