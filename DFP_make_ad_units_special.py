#!/usr/bin/python

from googleads import dfp

AD_UNITS_TO_UPDATE = []

def main(client, AD_UNITS_TO_UPDATE):
    for ad_unit_to_update in AD_UNITS_TO_UPDATE:
        inventory_service = client.GetService('InventoryService', version='v201702')

        values = [{
            'key': 'id',
            'value': {
                'xsi_type': 'TextValue',
                'value': ad_unit_to_update
            }
        }]
        query = 'WHERE id = :id'
        statement = dfp.FilterStatement(query, values)

        response = inventory_service.getAdUnitsByStatement(
            statement.ToStatement())

        if 'results' in response:
            updated_ad_units = []
            for ad_unit in response['results']:
                ad_unit['explicitlyTargeted'] = True
                updated_ad_units.append(ad_unit)

            ad_units = inventory_service.updateAdUnits(updated_ad_units)
            for ad_unit in ad_units:
                ad_unit_sizes = ['{%s x %s}' % (size['size']['width'],
                                                size['size']['height'])
                                 for size in ad_unit['adUnitSizes']]
                print ('Ad unit with ID \'%s\', name \'%s\', and sizes [%s] was updated' % (
                ad_unit['id'], ad_unit['name'], ','.join(ad_unit_sizes)))


if __name__ == '__main__':
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client, AD_UNITS_TO_UPDATE)
