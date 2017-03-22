#!/usr/bin/python
# -*- coding: utf-8 -*-

# Changes incoming.

from googleads import dfp

def main(client):

    user_service = client.GetService('UserService', version='v201702')
    user_team_association_service = client.GetService('UserTeamAssociationService',version='v201702')

    statement = dfp.FilterStatement()

    while True:
        dfp_users = user_service.getUsersByStatement(statement.ToStatement())

        print('isActive, id, name, email, roleId, roleName, teamId')
        for user in dfp_users['results']:
            print('%s,%s,%s,%s,%s,%s') % (user.isActive, user.id, user.name, user.email, user.roleId, user.roleName)
        break

if __name__ == '__main__':

    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
