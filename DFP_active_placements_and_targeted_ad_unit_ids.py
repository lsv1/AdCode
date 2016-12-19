# Import appropriate modules from the client library.
from googleads import dfp

def main(client):
  # Initialize appropriate service.
  placement_service = client.GetService('PlacementService', version='v201608')
  query = 'WHERE status = :status'
  values = [
      {'key': 'status',
       'value': {
           'xsi_type': 'TextValue',
           'value': 'ACTIVE'
       }},
  ]
  # Create a statement to select placements.
  statement = dfp.FilterStatement(query, values)

  # Retrieve a small amount of placements at a time, paging
  # through until all placements have been retrieved.
  while True:
    response = placement_service.getPlacementsByStatement(statement.ToStatement(
    ))
    if 'results' in response:
      print ('placement_name,placement_id, targetedAdUnitIds')
      for placement in response['results']:
          for ad_unit_id in placement['targetedAdUnitIds']:
            # Print out some information for each placement.
            print('%s,%d,%s' % (placement['name'],placement['id'],ad_unit_id))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

  #print '\nNumber of results found: %s' % response['totalResultSetSize']


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client)
