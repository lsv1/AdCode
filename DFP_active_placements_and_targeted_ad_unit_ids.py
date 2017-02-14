#!/usr/bin/python

from googleads import dfp

def main(client):

  placement_service = client.GetService('PlacementService', version='v201611')
  query = 'WHERE status = :status'
  values = [
      {'key': 'status',
       'value': {
           'xsi_type': 'TextValue',
           'value': 'ACTIVE'
       }},
  ]
  statement = dfp.FilterStatement(query, values)

  while True:
    response = placement_service.getPlacementsByStatement(statement.ToStatement(
    ))
    if 'results' in response:
      print('placement_id, placement_name, ad_unit_id')
      for placement in response['results']:
          for adunits in placement.targetedAdUnitIds:
            print('%d,%s,%s' % (placement['id'], placement['name'], adunits))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

if __name__ == '__main__':
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client)
