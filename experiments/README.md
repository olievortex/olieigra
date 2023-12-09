# Olie's IGRA Experiments
This folder contains various experiments related to the IGRA data. My vision is to build a near-time machine learning algorithm that can classify severe weather threat risk for various forecast periods based on radiosone observations.

Although I have some familiarity with forecasting severe weather as an amatuer storm chaser, machine learning is completely new to me. I am documenting my learning experience through the various experiments. Each experiment is a stepping stone to the ultimate vision.

My goals
 - Solidify my learning by attempting to teach others
 - Provide learners a practical application of machine learning
 - Allow the community to contribute by creating their own experiments

## Folder Structure
- /liftedindex_lr - Folder containing a linear regression to predict the LI severe weather parameter
- /download_data.ipynb - Notebook that downloads IGRA2 observations by station id
- /download_docs.ipynb - Notebook that downloads basic documentation and the station list
- /transform_data_gph20s10k.ipynb - Notebook to transform IGRA2 observation into 21 height levels
- /transform_station_list.ipynb - Notebook that converts the raw station list to a csv file

## Getting data
There is an automated process of fetching IGRA2 data using the notebooks in this folder. Execute the notebooks in the following order:

1. download_docs
2. transform_station_list
3. download_data
4. transform_data_gph20s10k

The first cell in each notebook contains variables that can be modified to suit your needs.

## Microsoft Fabric / Lake House
Some notebooks have been adapted from Microsoft Fabric. The base path of /lakehouse/ is used for file IO. **You do not need pySpark or Microsoft Fabric to run these notebooks!** Just change the path to something you like, or create a /lakehouse/ folder in your volume root.

Microsoft Fabric is a amazing but expensive Data Engineering and Machine Learning SaaS offering. This [Udemy Course](https://www.udemy.com/course/microsoft-fabric-k/) provides a nice introduction to Fabric. It helped me greatly. I get no compensation from sharing this.

To keep this project accessable to all, user contributions should not be dependent upon pySpark, Microsoft Fabric, or any other pay-to-use or clustering soltion.

## Medallion Architecture
It helps to organize data based on the level of processing. Organizing data by the medallion architecture is one way to do this. My notebooks assume the following:

- /lakehouse/default/Files/bronze - Storage of raw, unprocessed files
- /lakehouse/default/Files/silver - Files that have undergone some sort of transformation from bronze
- /lakehouse/default/Files/gold - Files that are in a format ready for immediate consumption
