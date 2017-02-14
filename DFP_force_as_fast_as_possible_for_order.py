# This script sets line items to serve as fast as possible and bypasses all DFP checks by disabling line item checks. This is needed at the end of the year when sales wants to squeeze as much inventory as possible out of the fiscal year.
#!/usr/bin/python
from googleads import dfp

ORDER_ID = 'ORDER_ID'

def main(client, order_id):
  # Initialize appropriate service.
  line_item_service = client.GetService('LineItemService', version='v201702')

  # Find line items with even delivery, the new value is down in the update_line_items object.
  values = [{
      'key': 'deliveryRateType',
      'value': {
          'xsi_type': 'TextValue',
          'value': 'EVENLY'
      }
  },{
      'key': 'orderId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': order_id
      }
  }]

  query = 'WHERE deliveryRateType = :deliveryRateType and orderId = :orderId'

  statement = dfp.FilterStatement(query, values, 500)

  response = line_item_service.getLineItemsByStatement(
      statement.ToStatement())

  if 'results' in response:
    updated_line_items = []
    for line_item in response['results']:
      if not line_item['isArchived']:
        line_item['deliveryRateType'] = 'AS_FAST_AS_POSSIBLE'
        # Override reservation blocks - F'ing life saver.
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
