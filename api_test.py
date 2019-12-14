#call search to get query url
import requests
import pandas as pd


def search():
    url = "https://services.webjet.com.au/api/hotels/searchservice"
    try:
        response = requests.post(
            url,
            json= {"areaId":"300178283","checkInDate":"2019-12-17T00:00:00.000Z","checkOutDate":"2019-12-20T00:00:00.000Z","rooms":[{"numberOfAdults":2,"childAges":[]}],"isRapid":True}
        )
    # handle connection fail, timeout or other http exceptions
    except requests.exceptions.RequestException as e:
        print(e)
        return 
    if response.status_code != 200:
        return 
    json_response = response.json()   
    #check if url exist
    if json_response['_links'] is None:
        return
    return json_response['_links']['query']['href']
#run search
url=search()
print(url)


#get hotels list
def query_hotel_list(url):
    try:
         response = requests.get(
            url
        )
    except requests.exceptions.RequestException as e:
        print(e)
        return 
    if response.status_code != 200:
        return 
    json_response = response.json()   
    if json_response['data'] is None:
        return
    return json_response['data']['hotels']

hotels_list=query_hotel_list(url)
print(len(hotels_list))

#ETL to flat the column info
# conveted_hotel_list =[]
# for x in range(hotels_list):
#     converted_hotel = x
#     converted_hotel['leadRoomPayableNow'] = x['leadRoom']['payableNow'] 

#save the data into datafram
df_hotels_list = pd.DataFrame(hotels_list)

#save the json list into csv
df_hotels_list.to_csv(path_or_buf='test1.csv',index=False)

