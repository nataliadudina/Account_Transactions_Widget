from src.utils import format_date, masked_card_number, masked_account_number, date_key, \
    format_and_print_transaction, sorted_transactions_with_formatted_data

import pytest


@pytest.fixture
def example_transaction():
    return [{
        "id": 509645757,
        "state": "EXECUTED",
        "date": "2019-10-30T01:49:52.939296",
        "operationAmount": {
            "amount": "23036.03",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод с карты на счет",
        "from": "Visa Gold 7756673469642839",
        "to": "Счет 48943806953649539453"
    },
        {
            "id": 811920303,
            "state": "EXECUTED",
            "date": "2019-06-14T19:37:49.044089",
            "operationAmount": {
                "amount": "63150.74",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 73222753239048295679",
            "to": "Счет 78544755774551298747"
        },
        {
            "id": 608117766,
            "state": "CANCELED",
            "date": "2018-10-08T09:05:05.282282",
            "operationAmount": {
                "amount": "77302.31",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на счет",
            "from": "Visa Gold 6527183396477720",
            "to": "Счет 38573816654581789611"
        }]


def test_format_date(example_transaction):
    assert format_date(example_transaction[0]) == '30.10.2019'


def test_masked_card_number(example_transaction):
    assert masked_card_number(example_transaction[0]) == "Visa Gold 7756 67** **** 2839"
    assert masked_card_number(example_transaction[1]) == "Счет **5679"


def test_masked_account_number(example_transaction):
    assert masked_account_number(example_transaction[0]) == "Счет **9453"


def test_date_key():
    test_data = [
        {'date': '19.11.2019'},
        {'date': '07.12.2019'},
        {'date': '13.11.2019'}
    ]

    # Ожидаемый результат после сортировки
    expected_sorted_data = [
        {'date': '13.11.2019'},
        {'date': '19.11.2019'},
        {'date': '07.12.2019'}
    ]

    sorted_data = sorted(test_data, key=date_key)

    assert sorted_data == expected_sorted_data


def test_format_and_print_transaction(example_transaction, capsys):
    expected_output = '2019-10-30T01:49:52.939296 Перевод с карты на счет\n' \
                      'Visa Gold 7756673469642839 -> Счет 48943806953649539453\n' \
                      '23036.03 руб.\n'

    format_and_print_transaction(example_transaction[0])
    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_sorted_transactions_with_formatted_data(example_transaction, capsys):
    assert type(sorted_transactions_with_formatted_data(data=example_transaction)) == list
    res = sorted_transactions_with_formatted_data(data=[{
        "id": 811920303,
        "state": "EXECUTED",
        "date": "2019-05-14T19:37:49.044089",
        "operationAmount": {
            "amount": "63150.74",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 73222753239048295679",
        "to": "Счет 78544755774551298747"
    }, {
        "id": 811920303,
        "state": "EXECUTED",
        "date": "2019-06-14T19:37:49.044089",
        "operationAmount": {
            "amount": "63150.74",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 73222753239048295679",
        "to": "Счет 78544755774551298747"
    }])
    for i in res:
        assert i.keys() == {
            "id",
            "state",
            "date",
            "operationAmount",
            "description",
            "from",
            "to"
        }

    assert res == [{'date': '14.06.2019',
                    'description': 'Перевод со счета на счет',
                    'from': 'Счет **5679',
                    'id': 811920303,
                    'operationAmount': {'amount': '63150.74',
                                        'currency': {'code': 'USD', 'name': 'USD'}},
                    'state': 'EXECUTED',
                    'to': 'Счет **8747'},
                   {'date': '14.05.2019',
                    'description': 'Перевод со счета на счет',
                    'from': 'Счет **5679',
                    'id': 811920303,
                    'operationAmount': {'amount': '63150.74',
                                        'currency': {'code': 'USD', 'name': 'USD'}},
                    'state': 'EXECUTED',
                    'to': 'Счет **8747'}]
