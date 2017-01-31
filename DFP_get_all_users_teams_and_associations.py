#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import appropriate modules from the client library.
from googleads import dfp

def main(client):
    # Initialize appropriate service.

    user_service = client.GetService('UserService', version='v201611')
    team_service = client.GetService('TeamService', version='v201611')
    user_team_association_service = client.GetService('UserTeamAssociationService',version='v201611')
    roles = user_service.getAllRoles()

    # Create a statement to select users. - Not required, need all users.

    statement = dfp.FilterStatement()

    # Retrieve a small amount of users at a time, paging
    # through until all users have been retrieved.

    while True:
        dfp_users = user_service.getUsersByStatement(statement.ToStatement())
        dfp_teams = team_service.getTeamsByStatement(statement.ToStatement())
        dfp_user_team_assoc = user_team_association_service.getUserTeamAssociationsByStatement(statement.ToStatement())

        ''' Commenting out this big block that was used for testing the whole dataset
        if 'results' in dfp_users and dfp_teams and dfp_user_team_assoc:

            print('Users')
            for user in dfp_users['results']:
                # Print out some information for each user.
                print '%d, %s' % (user['id'], user['name'])
            statement.offset += dfp.SUGGESTED_PAGE_LIMIT

            print('Teams')
            for team in dfp_teams['results']:
                # Print out some information for each team.
                print('%d, %s' % (team['id'],team['name']))
            statement.offset += dfp.SUGGESTED_PAGE_LIMIT

            print('User and Team Associations')
            for user_team_association in dfp_user_team_assoc['results']:
                # Print out some information for each user team association.
                print('%d, %d' % (user_team_association['teamId'],user_team_association['userId']))
            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

        print('Roles')
        for role in roles:
            print '%d, %s' % (role['id'], role['name'])

        '''

        print('isActive, id, name, email, roleId, roleName, teamId')
        for user_check in dfp_users['results']:
            for team_check in dfp_user_team_assoc['results']:
                if team_check.userId == user_check.id:
                    print('%s, %s, %s, %s, %s, %s, %s') % (user_check.isActive, user_check.id, user_check.name, user_check.email, user_check.roleId, user_check.roleName, team_check.teamId)
        break


if __name__ == '__main__':
    # Initialize client object.

    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
