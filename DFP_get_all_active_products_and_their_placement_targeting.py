#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleads import dfp


def main(client):
    # Initialize appropriate service.

    product_service = client.GetService('ProductService',version='v201611')

    # Create a statement to select products.

    statement = dfp.FilterStatement()

    # Retrieve a small amount of products at a time, paging
    # through until all products have been retrieved.

    print('product.status,product.id,product.name,targetedPlacementIds')
    while True:
        response = product_service.getProductsByStatement(statement.ToStatement())
        if 'results' in response:
            for product in response['results']:
                try:
                    for item in product.builtInTargeting.inventoryTargeting.targetedPlacementIds:
                        if product.productType == "DFP" and product.status == "ACTIVE":
                            print('%s,%d,%s,%s') % (product.status, product.id, product.name, item)
                except:
                    pass

            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

if __name__ == '__main__':
    # Initialize client object.

    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
