import pandas as pd
import pyodbc
import os
import json


if os.path.isdir("secrets"):
    secrets_files = [f for f in os.listdir(
        "secrets") if os.path.isfile(os.path.join("secrets", f))]
    if(len(secrets_files) > 0):
        with open("secrets/" + secrets_files[0], 'r') as f:
            secrets_json = json.load(f)
        connection_string = secrets_json["connection"]
    else:
        print("no secret file found.")
else:
    print("not found")

conn = pyodbc.connect(connection_string)

query = "SELECT * FROM dbo.tblItineraryComponents where RowCreateDate >= Convert(datetime,'2019-10-08')"


df_itinerary = pd.read_sql(query, conn)

df_lesscolumn = df_itinerary[['ItineraryID',
                              'TotalPriceExTax', 'ComponentType', 'RowCreateDate']]
df_pricegroupby = df_lesscolumn.groupby('ItineraryID').sum().reset_index()

print(df_pricegroupby)

df_package = df_lesscolumn[df_lesscolumn.ComponentType ==
                           'Package'][['ItineraryID', 'RowCreateDate']]
print(df_package)

df_merge = df_package.merge(df_pricegroupby)


def hr_func(ts):
    return ts.hour


df_merge['hour'] = df_merge['RowCreateDate'].apply(hr_func)

df_merge = df_merge[['hour', 'TotalPriceExTax']]

print(df_merge)


df_default_hr = pd.concat([pd.DataFrame([[i, float(0)]], columns=[
                           'hour', 'TotalPriceExTax']) for i in range(24)], ignore_index=True)

print(df_default_hr)
df_merge = df_merge.append(df_default_hr, ignore_index=True)
print(df_merge)

df_24hours = df_merge.groupby('hour').sum()


df_24hours = df_24hours.cumsum(axis=0).reset_index()


def sum_one(hr):
    return hr+1


df_24hours['to'] = df_24hours['hour'].apply(sum_one)

df_24hours = df_24hours[['hour', 'to', 'TotalPriceExTax']]
print(df_24hours)
