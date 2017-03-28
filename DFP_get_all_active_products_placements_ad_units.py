#!/usr/bin/python
# -*- coding: utf-8 -*-

# DFP_get_all_active_products_placements_ad_units.py
# This script pulls various data from the DFP Premium API using the DFP Client Library v201702
# Including: Products, Placements and Ad Units, some of the attributes are saved to CSV for storage, then read into Panda Data Frames for joining/merging and then outputs to CSV for the business user.

# Note - I'm dropping all non ascii characters from product names because it's easy and my business folks don't care.

from googleads import dfp
import csv
import os
import pandas
import \
    winsound  # This script takes a while to run on my network, so I want to know when it's done, usually doesn't work when I have Drum and Bass blasting though.


def products(client):
    product_service = client.GetService('ProductService', version='v201702')

    statement = dfp.FilterStatement()

    filename = 'dfp_products.csv'

    try:
        os.remove(filename)
        print('Old file ' + filename + ' removed.')
    except:
        pass

    with open(filename, 'ab') as csvfile:
        fieldnames = ['product_id', 'product_status', 'product_name', 'placement_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print ', '.join(fieldnames)  # Strange way to print this, at least for my newb brain. Seems unpythonic.

    while True:
        response = product_service.getProductsByStatement(statement.ToStatement())
        with open(filename, 'ab') as csvfile:
            if 'results' in response:
                for product in response['results']:
                    try:
                        for placement_id in product.builtInTargeting.inventoryTargeting.targetedPlacementIds:
                            print('%d,%s,%s,%s') % (
                                product.id, product.status, product.name.encode('ascii', 'ignore'), placement_id)
                            csv_writer = csv.writer(csvfile, delimiter=',')
                            csv_writer.writerow(
                                [product.id, product.status, product.name.encode('ascii', 'ignore'), placement_id])

                    except:
                        print('%d,%s,%s,%s') % (
                            product.id, product.status, product.name.encode('ascii', 'ignore'), 'N/A')
                        csv_writer = csv.writer(csvfile, delimiter=',')
                        csv_writer.writerow([product.id, product.status, product.name.encode('ascii', 'ignore'), 'N/A'])
                        pass
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break


def placements(client):
    placement_service = client.GetService('PlacementService', version='v201702')

    statement = dfp.FilterStatement()

    filename = 'dfp_placements.csv'

    try:
        os.remove(filename)
        print('Old file ' + filename + ' removed.')
    except:
        pass

    with open(filename, 'ab') as csvfile:
        fieldnames = ['placement_id', 'placement_status', 'placement_name', 'ad_unit_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print ', '.join(fieldnames)  # Strange way to print this, at least for my newb brain. Seems unpythonic.

    while True:
        response = placement_service.getPlacementsByStatement(statement.ToStatement())
        with open(filename, 'ab') as csvfile:
            if 'results' in response:
                for placement in response['results']:
                    try:
                        for ad_unit_id in placement.targetedAdUnitIds:
                            print('%d,%s,%s,%s') % (
                                placement.id, placement.status, placement.name.encode('ascii', 'ignore'),
                                ad_unit_id)
                            csv_writer = csv.writer(csvfile, delimiter=',')
                            csv_writer.writerow(
                                [placement.id, placement.status, placement.name.encode('ascii', 'ignore'),
                                 ad_unit_id])

                    except:
                        print('%d,%s,%s,%s') % (
                            placement.id, placement.status, placement.name.encode('ascii', 'ignore'), "N/A")
                        csv_writer = csv.writer(csvfile, delimiter=',')
                        csv_writer.writerow(
                            [placement.id, placement.status, placement.name.encode('ascii', 'ignore'), "N/A"])
                        pass
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break


def ad_units(client):
    ad_unit_service = client.GetService('InventoryService', version='v201702')

    statement = dfp.FilterStatement()

    filename = 'dfp_ad_units.csv'

    try:
        os.remove(filename)
        print('Old file ' + filename + ' removed.')
    except:
        pass

    with open(filename, 'ab') as csvfile:
        fieldnames = ['ad_unit_id', 'ad_unit_status', 'ad_unit_name', 'ad_unit_hasChildren', 'ad_unit_parentId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print ', '.join(fieldnames)  # Strange way to print this, at least for my newb brain. Seems unpythonic.

    while True:
        response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
        with open(filename, 'ab') as csvfile:
            if 'results' in response:
                for ad_unit in response['results']:
                    try:
                        print('%s,%s,%s,%s,%s' % (
                            ad_unit.id, ad_unit.status, ad_unit.name, ad_unit.hasChildren, ad_unit.parentId))
                        csv_writer = csv.writer(csvfile, delimiter=',')
                        csv_writer.writerow(
                            [ad_unit.id, ad_unit.status, ad_unit.name.encode('ascii', 'ignore'), ad_unit.hasChildren,
                             ad_unit.parentId])
                    except:
                        print('%s,%s,%s,%s,%s' % (
                            ad_unit.id, ad_unit.status, ad_unit.name, ad_unit.hasChildren, 'N/A'))
                        csv_writer = csv.writer(csvfile, delimiter=',')
                        csv_writer.writerow(
                            [ad_unit.id, ad_unit.status, ad_unit.name.encode('ascii', 'ignore'), ad_unit.hasChildren,
                             'N/A'])
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break


def outputs():
    dfp_products_file = 'dfp_products.csv'
    dfp_placements_file = 'dfp_placements.csv'
    dfp_ad_units_file = 'dfp_ad_units.csv'

    dfp_products_data = []
    dfp_placements_data = []
    dfp_ad_units_data = []

    with open(dfp_products_file) as f1:
        f1_data = csv.DictReader(f1)
        for row in f1_data:
            dfp_products_data.append(
                {'product_id': row['product_id'],
                 'product_status': row['product_status'],
                 'product_name': row['product_name'],
                 'placement_id': row['placement_id']})

    with open(dfp_placements_file) as f2:
        f2_data = csv.DictReader(f2)
        for row in f2_data:
            dfp_placements_data.append(
                {'placement_id': row['placement_id'],
                 'placement_status': row['placement_status'],
                 'placement_name': row['placement_name'],
                 'ad_unit_id': row['ad_unit_id']})

    with open(dfp_ad_units_file) as f3:
        f3_data = csv.DictReader(f3)
        for row in f3_data:
            dfp_ad_units_data.append(
                {'ad_unit_id': row['ad_unit_id'],
                 'ad_unit_status': row['ad_unit_status'],
                 'ad_unit_name': row['ad_unit_name'],
                 'ad_unit_hasChildren': row['ad_unit_hasChildren'],
                 'ad_unit_parentId': row['ad_unit_parentId']})

    df1 = pandas.DataFrame(dfp_products_data)
    df2 = pandas.DataFrame(dfp_placements_data)
    df3 = pandas.DataFrame(dfp_ad_units_data)

    # Products => Placement general join.
    output = df1.merge(df2)

    ad_unit_names = dict(zip(df3['ad_unit_id'], df3['ad_unit_name']))
    ad_unit_statuses = dict(zip(df3['ad_unit_id'], df3['ad_unit_status']))
    ad_unit_parentIds = dict(zip(df3['ad_unit_id'], df3['ad_unit_parentId']))

    # I don't know how to chain dictionary lookups yet!
    output['ad_unit_status'] = output['ad_unit_id'].map(ad_unit_statuses)
    output['ad_unit_name'] = output['ad_unit_id'].map(ad_unit_names)
    output['ad_unit_parent_id'] = output['ad_unit_id'].map(ad_unit_parentIds)
    output['ad_unit_parent_name'] = output['ad_unit_id'].map(ad_unit_names)

    try:
        os.remove('df_products_placements_ad_units.csv')
    except:
        pass

    output.to_csv('df_products_placements_ad_units.csv', sep=',', index=False)


dfp_client = dfp.DfpClient.LoadFromStorage()
products(dfp_client)
placements(dfp_client)
ad_units(dfp_client)
outputs()
winsound.Beep(400, 100)  # This script takes a while to run on my network.
