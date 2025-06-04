'''
Description:
------------
A program to download data from the SandSnap database
'''
# pylint: disable=line-too-long,invalid-name

import json

import requests

def sand_snap_query(url : str, save_path : str, layer_defs : str):
    """
    Description:
    ------------
    Sends a query with defined filters to the SandSnap server,
    downloads the response, and saves it in json format to a 
    local file.
    
    Parameters:
    -----------
    url : str
        The url of the query page without any parameters
	
        save_path : str
            The path to the output file. should be a .json or .csv
	    
        layer_defs : str
            The filter parameters to be included in the query. Use json 
            representation for layer definitions as described here: 
            https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service/
	    
        Returns:
        --------
        None, but does generate a file with output in the location specified by save_path
        """
    try:

        if not isinstance(url, str) or not isinstance(save_path, str) or not isinstance(layer_defs, str):
            raise TypeError

        # build url with parameters
        layer_defs = layer_defs.replace(" ", "+")
        layer_defs = layer_defs.replace("'", "%27")
        url = url + '?layerDefs=%7B"0"%3A"' + layer_defs + '"%7D&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&outSR=&datumTransformation=&applyVCSProjection=false&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&returnIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&returnZ=false&returnM=false&sqlFormat=none&f=pjson&token='

        with open(save_path, "w", encoding="utf-8") as output_file:

            # Request data from server
            response = requests.get(url, timeout=5)

	        # Check for errors
            if response.status_code == 200:

	            # Save data into output file
                data = response.json()
                if data is not None:
                    data = data["layers"][0]["features"]

                    json_string = json.dumps(data)
                    output_file.write(json_string)

                else:
                    print("Unable to retrive data from server")

            else:
                print(f"Request failed with error code {response.status_code}.")

    except (requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"Program failed with error {e}.")

    except TypeError:
        print("One or more input arguments had incorrect type. All arguments should be strings")


### MAIN ###

# url for SandSnap query page
URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query"

# path to file data is outputted in. Should be a json file.
SAVE_FILE_PATH = "output.json"

# filters for only data points with a calculated grain size and no errors
VALID_DATA_FILTER = "calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"
sand_snap_query(URL, SAVE_FILE_PATH, VALID_DATA_FILTER)
