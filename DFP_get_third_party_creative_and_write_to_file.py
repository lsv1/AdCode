#!/usr/bin/env python
from googleads import dfp

# This script appends third party creative snippets to a text file.
# This is useful to audit many post-bid creatives.

# Paste your third party creative IDs in the below array and execute.
# The output filename is creative_output.txt and will be written in the run directory of this script.
CREATIVE_IDS = ['1234', '12345', '123456']


def main(client, creative_id):
    creative_service = client.GetService('CreativeService', version='v201705')

    for i in CREATIVE_IDS:
        values = [{
            'key': 'type',
            'value': {
                'xsi_type': 'TextValue',
                'value': 'ThirdPartyCreative'
            }
        }, {
            'key': 'id',
            'value': {
                'xsi_type': 'NumberValue',
                'value': i
            }
        }]
        query = 'WHERE creativeType = :type AND id = :id'
        statement = dfp.FilterStatement(query, values, 1)

        while True:
            response = creative_service.getCreativesByStatement(statement.ToStatement())
            if 'results' in response:
                for creative in response['results']:
                    text_file = open("creative_output.txt", "a")
                    text_file.write('Creative ID:%d\nCreative Name: %s\n%s\n' % (
                    creative['id'], creative['name'], creative['snippet']))
                    text_file.close()

                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break


if __name__ == '__main__':
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client, CREATIVE_IDS)
