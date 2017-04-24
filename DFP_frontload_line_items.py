#!/usr/bin/python
from googleads import dfp

'''
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
'''

LINE_ITEMS_TO_UPDATE = []


def main(client, order_id):
    for line_item_id in LINE_ITEMS_TO_UPDATE:

        line_item_service = client.GetService('LineItemService', version='v201702')

        values = [{
            'key': 'deliveryRateType',
            'value': {
                'xsi_type': 'TextValue',
                'value': 'EVENLY'
            }
        }, {
            'key': 'id',
            'value': {
                'xsi_type': 'NumberValue',
                'value': line_item_id
            }
        }]

        query = 'WHERE deliveryRateType = :deliveryRateType and id = :id'
        statement = dfp.FilterStatement(query, values, 500)

        response = line_item_service.getLineItemsByStatement(
            statement.ToStatement())

        if 'results' in response:
            updated_line_items = []
            for line_item in response['results']:
                if not line_item['isArchived']:
                    line_item['deliveryRateType'] = 'FRONTLOADED'
                    line_item['allowOverbook'] = True
                    line_item['skipInventoryCheck'] = True
                    updated_line_items.append(line_item)

            line_items = line_item_service.updateLineItems(updated_line_items)

            if line_items:
                for line_item in line_items:
                    print ('Line item with id \'%s\', belonging to order id \'%s\', named '
                           '\'%s\', and delivery rate \'%s\' was updated.'
                           % (line_item['id'], line_item['orderId'], line_item['name'],
                              line_item['deliveryRateType']))
            else:
                print 'No line items were updated.'
        else:
            print 'No line items found to update.'


if __name__ == '__main__':
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client, ORDER_ID)
