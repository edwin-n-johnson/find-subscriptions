import csv
import json
import datetime
import locale


def load_quicken_transactions(txn_fname):
    transactions = {}
    line_count = 0
    txn_count = 0
    with open(txn_fname) as txn_file:
        txn_reader = csv.reader(txn_file, delimiter="\t")
        for row in txn_reader:
            line_count += 1
            # print(f"Line {line_count}, length {len(row)}")
            if len(row) == 11:
                (unused, Date, Account, Num, Description, Memo, Category, Tag, Clr, Amount, x) = row
                if not Date or not Description or Description == "Description":
                    # Skip this row as it is a header
                    continue
                txn_count += 1
                txn = {
                    'date': datetime.datetime.strptime(Date, "%m/%d/%Y"),
                    'account': Account,
                    'num': Num,
                    'description': Description,
                    'memo': Memo,
                    'category': Category,
                    'tag': Tag,
                    'clr': Clr,
                    'amount': float(Amount.replace(',', '')),
                }
                if txn['description'] not in transactions:
                    transactions[txn['description']] = []
                transactions[txn['description']].append(txn)

    print(f"Num of transactions: {txn_count}")
    return transactions


def serialize_helper(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def save_json_transactions(json_fname, transactions):
    with open(json_fname, "w") as json_file:
        json.dump(transactions, json_file, indent=4, default=serialize_helper)


def load_json_transactions(json_fname):
    transactions = None
    with open(json_fname) as json_file:
        transactions = json.load(json_file)
    # Process transactions to convert data types
    for description, txns in transactions.items():
        for t in txns:
            t['date'] = datetime.datetime.fromisoformat(t['date'])
    return transactions


def main():
    tsv_fname = "txn-2020-2023.TXT"
    json_fname = tsv_fname.replace(".TXT", ".json")
    transactions = load_quicken_transactions(tsv_fname)
    save_json_transactions(json_fname, transactions)
    transactions2 = load_json_transactions(json_fname)
    save_json_transactions(json_fname.replace(".json", "-2.json"), transactions2)


if __name__ == "__main__":
    main()
