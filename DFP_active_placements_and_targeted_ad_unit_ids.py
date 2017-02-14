#!/usr/bin/python
# _*_ coding:utf-8 _*_

from googleads import dfp
import unicodecsv as csv

def main(client):

  placement_service = client.GetService('PlacementService', version='v201702')
  ad_unit_service = client.GetService('InventoryService', version='v201702')
  query = 'WHERE status = :status'
  values = [
      {'key': 'status',
       'value': {
           'xsi_type': 'TextValue',
           'value': 'ACTIVE'
       }},
  ]
  statement = dfp.FilterStatement(query, values)

  with open('dfp_placements.csv', 'wb') as csvfile:
    fieldnames = ['placement_id', 'placement_name', 'ad_unit_id', 'ad_unit_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

  print ', '.join(fieldnames)  # Stupid way to print arrays.

  while True:
    dfp_placements = placement_service.getPlacementsByStatement(statement.ToStatement())
    dfp_ad_units = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())

    if 'results' in dfp_placements and dfp_ad_units:
      for placement in dfp_placements['results']:
        for adunit in dfp_ad_units['results']:
          for targetedAdUnit in placement.targetedAdUnitIds:
            if adunit.id == targetedAdUnit:
              print('%d,%s,%s,%s' % (placement['id'], placement['name'], adunit.id, adunit.name))
              with open('dfp_placements.csv', 'ab') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',')
                csv_writer.writerow([placement.id, placement.name, adunit.id, adunit.name])
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

if __name__ == '__main__':
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client)
