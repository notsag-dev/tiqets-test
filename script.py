import csv
import operator

def process_orders(file_name, key_ind):
    """Process the orders csv file and return a dictionary whose
    keys are order ids and values are customer ids
    """
    res = {}
    with open(file_name, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            res[row[0]] = row[1]
    return res

def process_barcodes(file_name, key_ind):
    """Process the barcodes csv file and return:
        - a dictionary whose keys are order ids and values arrays of barcode ids
        - the number of unused barcode ids
        - an array of duplicated barcode ids
    """
    res = {}
    unused_barcodes = 0
    barcodes_set = set()
    duplicated_barcodes = []
    with open(file_name, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for barcode in reader:
            if not barcode[1]:
                unused_barcodes += 1
                continue
            barcode_id, order_id = barcode
            if barcode_id in barcodes_set:
                duplicated_barcodes.append(barcode_id)
                continue
            barcodes_set.add(barcode_id)
            if not order_id in res:
                res[order_id] = []
            res[order_id].append(barcode_id)
    return [res, unused_barcodes, duplicated_barcodes]

def get_order_csv_str(customer_id, order_id, barcodes):
    """Generate output's line for an specific order"""
    name_arr = [customer_id, order_id, ','.join(barcodes)]
    return ','.join(name_arr) + '\n'

def print_results(customer_purchases, num, unused_barcodes):
    print("RESULTS REPORT")
    # Print top customers
    customers_sorted = sorted(customer_purchases.items(), key=operator.itemgetter(1), reverse=True)
    print("Top", num, "customers:")
    for i in range(0, num):
        print(customers_sorted[i][0] + ',', customers_sorted[i][1])
    print()

    # Print unused barcodes
    print("Unused barcodes:", unused_barcodes)
    print("------")

def print_errors(orders_no_barcodes, duplicated_barcodes):
    print("ERRORS REPORT")
    print("Orders with no barcodes:", orders_no_barcodes)
    print("Duplicated barcodes:", duplicated_barcodes)

def main():
    orders = process_orders('orders.csv', 0)
    barcodes, unused_barcodes, duplicated_barcodes = process_barcodes('barcodes.csv', 1)
    output = open('output.csv','w+')
    customer_purchases = {}
    orders_no_barcodes = []
    for order_id in orders:
        if order_id not in barcodes:
            orders_no_barcodes.append(order_id)
            continue
        customer_id = orders[order_id]
        if customer_id not in customer_purchases:
            customer_purchases[customer_id] = 0
        customer_purchases[customer_id] += len(barcodes[order_id])
        output.write(get_order_csv_str(customer_id, order_id, barcodes[order_id]))
    output.close()
    print_results(customer_purchases, 5, unused_barcodes)
    print_errors(orders_no_barcodes, duplicated_barcodes)

if __name__ == "__main__":
    main()
