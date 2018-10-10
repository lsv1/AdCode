#!/usr/bin/env python

# This script will add key-value targeting to existing targeting.
# This is probably most useful for publishers which have added Prebid (or Header Bidding) line items in their AdManager and at a later date need to globally add or exclude key-values.

from googleads import ad_manager

ORDER_ID = 'ORDER_ID'
KEY_ID = 'KEY_ID
VALUE_ID = 'VALUE_ID'
OPERATOR = 'IS_NOT'  # API values should be "AND", "OR, "IS", "IS_NOT", similar to => https://support.google.com/admanager/answer/177381?hl=en


def main(client, order_id, key_id, value_id, operator):
    line_item_service = client.GetService('LineItemService', version='v201808')

    statement = (ad_manager.StatementBuilder()
                 .Where(('orderId = :orderId'))
                 .WithBindVariable('orderId', long(order_id))
                 .Limit(500))

    response = line_item_service.getLineItemsByStatement(statement.ToStatement())

    if 'results' in response and len(response['results']):
        for line_item in response['results']:
            line_item_service = client.GetService('LineItemService', version='v201808')

            custom_criteria = {
                'xsi_type': 'CustomCriteria',
                'keyId': key_id,
                'valueIds': [value_id],
                'operator': operator
            }

            sub_set = {
                'xsi_type': 'CustomCriteriaSet',
                'logicalOperator': 'AND',
                'children': [custom_criteria]
            }

            statement = (ad_manager.StatementBuilder()
                         .Where('id = :lineItemId')
                         .WithBindVariable('lineItemId', long(line_item['id']))
                         .Limit(1))

            line_item = line_item_service.getLineItemsByStatement(
                statement.ToStatement())['results'][0]
            top_set = {
                'xsi_type': 'CustomCriteriaSet',
                'logicalOperator': 'AND',
                'children': [line_item['targeting']['customTargeting'], sub_set]
            }
            line_item['targeting']['customTargeting'] = top_set

            line_item = line_item_service.updateLineItems([line_item])[0]

            if line_item:
                print ('Line item with id "%s" updated with custom criteria targeting.'
                       % line_item['id'])
            else:
                print ('No line items were updated.')

        else:
            print('No line items found.')


if __name__ == '__main__':
    ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
    main(ad_manager_client, ORDER_ID, KEY_ID, VALUE_ID, OPERATOR)
