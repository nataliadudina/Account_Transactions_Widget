from src.utils import executed_transactions, format_and_print_transaction


def main():

    last_transactions = executed_transactions()[:5]

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
