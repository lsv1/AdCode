#!/usr/bin/python
# -*- coding: utf-8 -*-
# I'm dropping all non ascii characters from product names because it's easy, this isn't great if you're a non-American DFP user.
# You may have to consider encoding fixes if you need special characters in your product names.

from googleads import dfp
import csv

def main(client):
    product_service = client.GetService('ProductService', version='v201702')

    statement = dfp.FilterStatement()

    with open('dfp_products.csv', 'wb') as csvfile:
        fieldnames = ['product_id', 'product_status', 'product_name', 'targetedPlacementIds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print ', '.join(fieldnames)  # Stupid way to print this IMO. Seems unpythonic.

    while True:
        response = product_service.getProductsByStatement(statement.ToStatement())
        with open('dfp_products.csv', 'ab') as csvfile:
            if 'results' in response:
                for product in response['results']:
                    try:
                        for placement_id in product.builtInTargeting.inventoryTargeting.targetedPlacementIds:
                            print('%d,%s,%s,%s') % (product.id, product.status, product.name.encode('ascii', 'ignore'), placement_id)
                            csv_writer = csv.writer(csvfile, delimiter=',')
                            csv_writer.writerow([product.id, product.status, product.name.encode('ascii', 'ignore'), placement_id])

                    except:
                        print('%d,%s,%s,%s') % (product.id, product.status, product.name.encode('ascii', 'ignore'), 'N/A')
                        csv_writer = csv.writer(csvfile, delimiter=',')
                        csv_writer.writerow([product.id, product.status, product.name.encode('ascii', 'ignore'), 'N/A'])
                        pass
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
                break

if __name__ == '__main__':
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
