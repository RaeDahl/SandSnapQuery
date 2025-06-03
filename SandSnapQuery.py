'''
Description:
------------
A program to download data from the SandSnap database
'''

import json
import csv

import requests


def sand_snap_query(url : str, save_path : str, query_params : dict, file_type : str = "json"):
    """
    Description:
    ------------
    Sends a query with defined filters to the SandSnap server,
    downloads the response, and saves it in json format to a 
    local file.

    Parameters:
    -----------
    url : str
        The url of the query page

        save_path : str
            The path to the output file. should be a .json or .csv
	
        query_params : dict[str, dict[str, str]]
            The filter parameters to be included in the query. Use json 
            representation for layer definitions as described here: 
            https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service/

        file_type : str
            can be either "csv" or "json", default is json
            sets what file type to save output into

        Returns:
        --------
        None, but does generate a file with output in the location specified by save_path
        """
    try:
        with open(save_path, "w", encoding="utf-8") as output_file:
	
        # Request data from server
        response = requests.get(url, params=query_params, timeout=5)
	
	# Check for errors
        if response.status_code == 200:
			
	# Save data into output file
        data = response.json()
        data = data.get("features")

            if file_type == "json":
                json_string = json.dumps(data)
                output_file.write(json_string)

            elif file_type == "csv":
                writer = csv.DictWriter(output_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            else:
                print(f"Invalid file type {file_type} given. Saving as json instead.")
                json_string = json.dumps(data)
                output_file.write(json_string)

       else:
            print(f"Request failed with error code {response.status_code}.")

    except Exception as e:
		print(f"Program failed with error {e}.")


### MAIN ###

# url for SandSnap query page
URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query?layerDefs=%7B%220%22%3A%22country+%3D+%27USA%27%22%7D&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&outSR=&datumTransformation=&applyVCSProjection=false&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&returnIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&returnZ=false&returnM=false&sqlFormat=none&f=html&token=" 

# path to file data is outputted in. Should be a json file.
SAVE_FILE_PATH = "output.json" 

# filters for only data points with a calculated grain size and no errors
PARAMS = {
    "layerDefs": {"0":"calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"}
} 

sand_snap_query(URL, SAVE_FILE_PATH, PARAMS)
