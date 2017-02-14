#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleads import dfp

def main(client):

    user_service = client.GetService('UserService', version='v201702')
    user_team_association_service = client.GetService('UserTeamAssociationService',version='v201702')

    statement = dfp.FilterStatement()

    while True:
        dfp_users = user_service.getUsersByStatement(statement.ToStatement())
        dfp_user_team_assoc = user_team_association_service.getUserTeamAssociationsByStatement(statement.ToStatement())

        print('isActive, id, name, email, roleId, roleName, teamId')
        for user_check in dfp_users['results']:
            for team_check in dfp_user_team_assoc['results']:
                if team_check.userId == user_check.id:
                    print('%s, %s, %s, %s, %s, %s, %s') % (user_check.isActive, user_check.id, user_check.name, user_check.email, user_check.roleId, user_check.roleName, team_check.teamId)
        break

if __name__ == '__main__':

    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
