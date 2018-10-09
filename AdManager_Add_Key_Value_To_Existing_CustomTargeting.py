#!/usr/bin/env python

# Test script for the 201808 API.

from googleads import ad_manager
import pprint

LINE_ITEM_ID = 'LINE_ITEM_ID'

KEY_ID1 = 'KEY_ID'
VALUE_ID1 = 'VALUE_ID'


def main(client, line_item_id, key_id1, value_id1):
    line_item_service = client.GetService('LineItemService', version='v201808')

    custom_criteria1 = {
        'xsi_type': 'CustomCriteria',
        'keyId': key_id1,
        'valueIds': [value_id1],
        'operator': 'IS_NOT'
    }

    sub_set = {
        'xsi_type': 'CustomCriteriaSet',
        'logicalOperator': 'AND',
        'children': [custom_criteria1]
    }

    statement = (ad_manager.StatementBuilder()
                 .Where('id = :lineItemId')
                 .WithBindVariable('lineItemId', long(line_item_id))
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
        print ('Line item with id "%s" updated with custom criteria targeting:'
               % line_item['id'])
        pprint.pprint(line_item['targeting']['customTargeting'])
    else:
        print ('No line items were updated.')


if __name__ == '__main__':
    ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
    main(ad_manager_client, LINE_ITEM_ID, KEY_ID1, VALUE_ID1)
