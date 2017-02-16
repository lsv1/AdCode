#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleads import dfp
import csv
# Unicode might spit out errors if you have none-breaking spaces in your product or inventory names, I recommend fixing this at the source instead of hackery, but whatever.
#import unicodecsv as csv

def main(client):

    product_service = client.GetService('ProductService',version='v201702')

    statement = dfp.FilterStatement()


    with open('dfp_products.csv', 'wb') as csvfile:
        fieldnames = ['product_status', 'product_id', 'product_name', 'product_rate','targetedPlacementIds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print ', '.join(fieldnames)  # Stupid way to print arrays.

    while True:
        response = product_service.getProductsByStatement(statement.ToStatement())
        if 'results' in response:
            for product in response['results']:
                try:
                    for item in product.builtInTargeting.inventoryTargeting.targetedPlacementIds:
                        if product.productType == "DFP" and product.status == "ACTIVE":
                            print('%s,%d,%s,%s') % (product.status, product.id, product.name, item)
                            with open('dfp_products.csv', 'ab') as csvfile:
                                csv_writer = csv.writer(csvfile, delimiter=',')
                                csv_writer.writerow([product.status, product.id, product.name, item])
                except:
                    pass

            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

if __name__ == '__main__':

    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
