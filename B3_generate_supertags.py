#!/usr/bin/python
# Generate Supertags from the District M B3 API Response object (http://b3.districtm.ca/api/tags/superTag), make sure to change null => "null" before running.
# TODOs: Add functionality to login, make authenticated request, and then parse the response into the below file

import datetime

supertags = {"..."} #Paste response object

def generate_supertags():
    publisher = "My Publisher"
    text_file = open(publisher + " - Supertags.txt", "w")
    text_file.write("%s - Supertags\n" % publisher)
    text_file.write("Generated on %s\n\n" % datetime.datetime.today().strftime('%Y-%m-%d at %H:%M:%S'))
    for supertag in supertags['tags']:
        text_file.write(
            "<!-- District M SuperTag - %s - %s\n" % (supertag['domain']['sDomain'], supertag['adSize']['main']))
        text_file.write("%s\n\n" % (supertag['tagJS'].replace("\/", "/")))
    text_file.close()

generate_supertags()
