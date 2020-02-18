import requests
import pandas as pd

headers = {
    'X-DC-DEVKEY': "NEED YOUR OWN KEY", #API key
    'Content-Type': "application/json"
    }

#This URL grabs a CSV of active orders in the account
url = "https://www.digicert.com/services/v2/order/certificate?content_type=csv&attachment_filename=orders.csv&includeNotes=true&filters%5Bstatus%5D%5B0%5D=issued&filters%5Bstatus%5D%5B1%5D=pending&filters%5Bstatus%5D%5B2%5D=reissue_pending&filters%5Bvalid_till%5D%5B0%5D=%3ENOW&filters%5Bvalid_till%5D%5B1%5D=null&filters%5Bstatus%5D%5B2%5D=issued"
response = requests.request("GET", url, headers=headers)

#Get CSV Report and Save Locally
with open('orders.csv', "wb") as csv_file:
    for block in response.iter_content(1024):
        csv_file.write(block)

#Read and Sort by Number of Days Remaining
df = pd.read_csv("orders.csv")
df.sort_values("certificate.days_remaining", axis = 0, ascending = True,
                 inplace = True, na_position ='last')
#Save as a New CSV
df.to_csv("order_sort.csv")
dfsorted = pd.read_csv("order_sort.csv")

#Grab Columns from CSV
x = dfsorted["id"]
y = dfsorted["certificate.common_name"]
z = dfsorted["certificate.days_remaining"]

#Print Pulled Data
for i in range(len(x)):
    print("Order Number: " + str(x[i]) + "     " + str(y[i]) + "      " + str(z[i]))
