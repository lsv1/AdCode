#!/usr/bin/python
# -*- coding: utf-8 -*-
# I'm dropping all non ascii characters from product names because it's easy, this isn't great if you're a non-American DFP user.
# You may have to consider encoding fixes if you need special characters in your product names.

from googleads import dfp
import csv


def main(client):
    placement_service = client.GetService('PlacementService', version='v201702')

    statement = dfp.FilterStatement()

    with open('dfp_placements.csv', 'wb') as csvfile:
        fieldnames = ['placement_status', 'placement_id', 'placement_name', 'ad_unit_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print ', '.join(fieldnames)  # Stupid way to print this IMO. Seems unpythonic.

    while True:
        response = placement_service.getPlacementsByStatement(statement.ToStatement())
        with open('dfp_placements.csv', 'ab') as csvfile:
            if 'results' in response:
                for placement in response['results']:
                    try:
                        for ad_unit_id in placement.targetedAdUnitIds:
                            print('%d,%s,%s,%s') % (placement.id, placement.status, placement.name.encode('ascii', 'ignore'), ad_unit_id)
                            csv_writer = csv.writer(csvfile, delimiter=',')
                            csv_writer.writerow([placement.id, placement.status, placement.name.encode('ascii', 'ignore'), ad_unit_id])

                    except:
                        print('%d,%s,%s,%s') % (
                        placement.id, placement.status, placement.name.encode('ascii', 'ignore'), "N/A")
                        csv_writer = csv.writer(csvfile, delimiter=',')
                        csv_writer.writerow([placement.id, placement.status, placement.name.encode('ascii', 'ignore'), "N/A"])
                        pass
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT


if __name__ == '__main__':
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
