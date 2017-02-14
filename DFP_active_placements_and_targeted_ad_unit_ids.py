#!/usr/bin/python

from googleads import dfp

def main(client):

  placement_service = client.GetService('PlacementService', version='v201611')
  ad_unit_service = client.GetService('InventoryService', version='v201611')
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
    dfp_placements = placement_service.getPlacementsByStatement(statement.ToStatement())
    dfp_ad_units = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())

    if 'results' in dfp_placements and dfp_ad_units:
      print('placement_id, placement_name, ad_unit_id, ad_unit_name')
      for placement in dfp_placements['results']:
        for adunit in dfp_ad_units['results']:
          for targetedAdUnit in placement.targetedAdUnitIds:
            if adunit.id == targetedAdUnit:
              print('%d,%s,%s,%s' % (placement['id'], placement['name'], adunit.id, adunit.name))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

if __name__ == '__main__':
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client)
