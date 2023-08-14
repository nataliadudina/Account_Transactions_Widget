from src.utils import executed_transactions, format_and_print_transaction, load_card_transactions


def main():
    data = load_card_transactions()
    last_transactions = executed_transactions(data=data)[:5]

    # Вывод пяти последних исполненных операций
    for item in last_transactions:
        if 'from' not in item:
            item['from'] = ''
        elif 'to' not in item:
            item['to'] = ''
        format_and_print_transaction(item)
        print()


if __name__ == '__main__':
    main()
