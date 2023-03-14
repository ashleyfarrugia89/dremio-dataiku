# Dataiku Plugin for Arrow Flight (using Dremio)

## Plugin Information

[Dremio](https://www.dremio.com/) is a lakehouse platform that provides the ability to perform accelerated processing of data on the lake without the need to move it from the lake. Dremio has the following characteristics:

* Semantic Layer
* Self-Service
* Accelerated Processing on the Lake
* Open Data and Table Formats

Dremio is a platform that can be deployed almost anywhere, it can be deployed on bare metal, Hadoop, VM's, Kubernetes, Cloud VMs or even using our Dremio Cloud offering.

The purpose of this plugin is to enable users of Dataiku to gain access to Dremio data for downstream wrangling and processing.


## How does it work?


This plugin leverages [Apache Arrow Flight](https://arrow.apache.org/blog/2019/10/13/introducing-arrow-flight/), providing the ability to extract large volumes of data at 20-50x quicker than ODBC connections. This means that your data is available to you inside Dataiku much quicker.


This plugin comes with a code environment that will install of it's dependencies including pyarrow. This is required to communicate with your Dremio server.


Finally, this plugin has been tested with Python 3.6 only.


## How to use?

* Install this plugin inside Dataiku
* Add plugin to your flow
* Assign a name for your output Dataset, stored inside a storage location of your choice.

This Plugin requires 4 input parameters, these must be input in the Plugin form.

1. Dremio Host - A Dremio host that you will be querying 
2. Dremio Username - A user who has access to your Dremio datasets
3. Dremio Password - The password associated with the user
4. SQL Query - An SQL query that you want to perform against Dremio.
5. VDS Path - The path where you want the VDS to exist within Dremio.
6. PDS Path - The PDS path for the datasource where Dataiku will output the resulting dataset.


Finally, run the Plugin recipe and browse the output Dataset. You should see the result of your query.