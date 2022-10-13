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
query = get_recipe_config().get("sql_query")

def flight_query(host, username, password, query):
    client = flight.FlightClient('grpc+tcp://{0}:32010'.format(host))
    bearer_token = client.authenticate_basic_token(username, password)
    options = flight.FlightCallOptions(headers=[bearer_token])
    info = client.get_flight_info(flight.FlightDescriptor.for_command(query + '-- arrow flight'), options)
    reader = client.do_get(info.endpoints[0].ticket, options)

    batches = []
    while True:
        try:
            batch, metadata = reader.read_chunk()
            batches.append(batch)
        except StopIteration:
            break
    data = pa.Table.from_batches(batches)
    df = data.to_pandas()
    return df

df = flight_query(DREMIO_HOST, USER, PASSWD, query)

tbl = dataiku.Dataset(OUTPUT)
tbl.write_with_schema(df)