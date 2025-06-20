'''
Description:
------------
A program to download data from the SandSnap database
'''
# pylint: disable=line-too-long,invalid-name

import json
import os
import requests

def sand_snap_query(url : str, save_path : str, layer_defs : str, geometry : list=None):
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

        geometry : list[str]
            Optional parameters for filtering geometry, default is none
            Enter in format [xmin, ymin, xmax, ymax] with lat/lon coordinates as strings
	    
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

        if geometry is None:
            url = url + '?layerDefs=%7B"0"%3A"'  +  \
            layer_defs +  \
            '"%7D&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&outSR=&datumTransformation=' +  \
            '&applyVCSProjection=false&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&returnIdsOnly=false&returnCountOnly=false' + \
            '&returnDistinctValues=false&returnZ=false&returnM=false&sqlFormat=none&f=pjson&token='

        else:
            url = url + '?layerDefs=%7B"0"%3A"' +  \
            layer_defs + '"%7D&geometry=%7B%22xmin%22%3A' +  \
            str(geometry[0]) + '%2C+%22ymin%22%3A' +  \
            str(geometry[1]) + '%2C+%22xmax%22%3A' +  \
            str(geometry[2]) + '%2C+%22ymax%22%3A' +  \
            str(geometry[3]) +  \
            '%7D&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&outSR=&datumTransformation=&applyVCSProjection=false' + \
            '&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&returnIdsOnly=false&returnCountOnly=false&returnDistinctValues=false' +  \
            '&returnZ=false&returnM=false&sqlFormat=none&f=pjson&token='

        with open(save_path, "w", encoding="utf-8") as output_file:

            # Request data from server
            response = requests.get(url, timeout=5)

	        # Check for errors
            if response.status_code == 200:

	            # Save data into output file
                data = response.json()

                if data is not None:
                    try:
                        if data["error"]:
                            raise ValueError
                    except KeyError:
                        pass
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
    except ValueError:
        print("The URL was invalid")


def get_sandsnap_image(snap_id: str):
    """
    Description:
    ------------
    Downloads the image associated with a sandsnap
    
    Parameters:
    -----------
    snap_id : str
        The id number of the sandsnap to get an image for, as a string
	    
        Returns:
        --------
        None, but does save the image as a jpg file
        """

    url = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/ArcGIS/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/0/" + \
        snap_id + "/attachments"

    response = requests.post(url, data={"token" : ""}, timeout=5)
    if response.status_code == 200:
        # Find link for image file
        lines = response.text.splitlines()
        new_url = lines[33]
        new_url = new_url.split('"')[1]
        new_url = "https://services6.arcgis.com" + new_url

        # Get image file
        image_response = requests.get(new_url, timeout=5, stream=True)
        if image_response.status_code == 200:
            filename = "sandsnap_" + snap_id + "_image.jpg"
            filename = os.path.join("output_files", filename)
            with open(filename, "wb") as image_file:
                image_file.write(image_response.content)

        else:
            print(f"Image request failed with error code {response.status_code}.")
    else:
        print(f"request failed with error code {response.status_code}.")

### MAIN ###

# # url for SandSnap query page
# URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query"

# # path to file data is outputted in. Should be a json file.
# SAVE_FILE_PATH = "output.json"

# # filters for only data points with a calculated grain size and no errors
# VALID_DATA_FILTER = "calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"
# #sand_snap_query(URL, SAVE_FILE_PATH, VALID_DATA_FILTER)

# get_sandsnap_image("2120")
