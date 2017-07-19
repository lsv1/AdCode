#!/usr/bin/env python
# Remove Ad Unit Targeting and apply a Placement instead

from googleads import dfp

ORDER_ID = ''
PLACEMENTS_TO_TARGET = ['']


def main(client, order_id):
    # Initialize appropriate service.
    line_item_service = client.GetService('LineItemService', version='v201705')

    # Create statement object to only select line items with even delivery rates.
    values = [{
        'key': 'orderId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': order_id
        }
    }]

    query = 'WHERE orderId = :orderId'
    statement = dfp.FilterStatement(query, values, 500)

    response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())

    if 'results' in response:
        updated_line_items = []
        for line_item in response['results']:
            if not line_item['isArchived']:
                del line_item['targeting']['inventoryTargeting'].targetedAdUnits
                line_item['targeting']['inventoryTargeting']['targetedPlacementIds'] = PLACEMENT_TO_TARGET
                updated_line_items.append(line_item)

        line_items = line_item_service.updateLineItems(updated_line_items)

        if line_items:
            for line_item in line_items:
                print ('Line item with id "%s", belonging to order id "%s", named ''"%s" was updated.' % (
                    line_item['id'], line_item['orderId'], line_item['name']))
        else:
            print 'No line items were updated.'
    else:
        print 'No line items found to update.'


if __name__ == '__main__':
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client, ORDER_ID)
