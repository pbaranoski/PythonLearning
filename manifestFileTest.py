from datetime import datetime

# IDRBI-99999-20210126-165003
tmstmp = datetime.today().strftime('%Y%m%d-%H%M%S')

jiraTicket = "https://jiraent.cms.gov/browse/IDRBI-99999"
URLParts = jiraTicket.split("/")
dataRequestID = f'{URLParts[len(URLParts) - 1]}-{tmstmp}'

print (dataRequestID)

DAYS4MM="31|28|31|30|31|30|31|31|30|31|30|31"
sMMFormatted = "08"

dd = DAYS4MM.split("|") [(int(sMMFormatted) - 1)]
#idx = int(sMMFormatted) - 1
#dd = DAYS4MM.split("|") [idx]
print (dd)
