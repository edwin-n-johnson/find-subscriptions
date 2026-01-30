import loader
import sys


def is_likely_subscription(transactions, debug=False):
    likely = False
    transactions.sort(key=lambda x: x['date'])

    # Look for same frequency
    for i in range(len(transactions)):
        current_txn = transactions[i]
        current_txn['count'] = 0
        for j in range(i+1, len(transactions)):
            # td = transactions[j]['date'] - current_txn['date']
            years = transactions[j]['date'].year - current_txn['date'].year
            months = 12 * years + transactions[j]['date'].month - current_txn['date'].month
            days = transactions[j]['date'].day - current_txn['date'].day
            if debug:
                print(f"({i}, {j}) == {years}, {months}, {days}")
            if days == 0:
                current_txn['count'] += 1

    # Sort and see if the first one has high freq
    transactions.sort(key=lambda x: x['count'], reverse=True)
    subscription = None
    highest_txn = transactions[0]
    if highest_txn['count'] > 2 and (float(highest_txn['count']) / len(transactions)) > .5:
        likely = True
        subscription = {
            'description': highest_txn['description'],
            'count': highest_txn['count'],
            'start_date': highest_txn['date'],
            'category': highest_txn['category'],
        }
    else:
        if debug:
            print(f"{highest_txn['description']} ignored: {highest_txn['count']} || {len(transactions)}")

    return likely, subscription


def main():
    transactions = loader.load_quicken_transactions(sys.argv[1])
    subscription_count = 0
    for payee, txns in transactions.items():
        if payee != "Roll20.Net":
            pass
        if len(txns) > 1:
            result, sub = is_likely_subscription(txns, False)
            if result:
                subscription_count += 1
                print(f"{payee} has {sub['count']} txns starting {sub['start_date']} cat {sub['category']}")
    print(f"{subscription_count} payees")


if __name__ == "__main__":
    main()
