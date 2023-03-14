# Code for custom code recipe arrow-v1 (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *
from pyarrow import flight
import pyarrow as pa

OUTPUT = get_output_names_for_role("output_dataset")[0]
DREMIO_HOST =  get_recipe_config().get("dremio_host")
USER = get_recipe_config().get("dremio_user")
PASSWD = get_recipe_config().get("dremio_passwd")
dremio_query = get_recipe_config().get("sql_query")
pds_path = get_recipe_config().get("pds_path")
vds = get_recipe_config().get("dremio_vds")

CREATE_VDS_SQL = "CREATE VDS {0} as select * from {1}.{2}"

def connect(host, username, passwd):
    try:
        client = flight.FlightClient('grpc+tcp://{0}:32010'.format(host))
        bearer_token = client.authenticate_basic_token(username, passwd)
        options = flight.FlightCallOptions(headers=[bearer_token])
    except Exception as e:
        print("Error connecting to server: {0} - {1}".format(host, e))
        return False
    else:
        return [client, options]

def query(client, options, sql):
    ret = None
    try:
        info = client.get_flight_info(flight.FlightDescriptor.for_command(sql + '-- arrow flight'), options)
        reader = client.do_get(info.endpoints[0].ticket, options)
        df = reader.read_pandas()
        return df
    except Exception as e:
        print("Error submitting query to host: ", e)
        ret = False
        return ret
    else:
        return ret

client, options = connect(DREMIO_HOST, USER, PASSWD)
# get data from Dremio
df = query(client, options, dremio_query)
tbl = dataiku.Dataset(OUTPUT)
tbl.write_with_schema(df)
# create view/vds on the data inside Dremio
vds_query = CREATE_VDS_SQL.format(vds, pds_path, OUTPUT)
query(client, options, vds_query)