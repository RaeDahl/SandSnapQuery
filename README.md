
# SandSnap API Query

## Description:
 
A Python program to retrieve data from the [SandSnap query page](https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query). Uses the requests library to send a get request to the SandSnap API, the save the data into a local file.

## Current Functionality:
  
  - Downloads data from SandSnap API
  - Can include filters in API query (Eg. only return data points with no errors, or give all data from a specific state)
  - Saves data in json or csv files

## Usage

There is a default query set up in the `MAIN` section of `SandSnapQuery.py`. This code will download all data without errors and save it in json format. Comment it out when running the unit tests or if you 
plan to import the function into other files. The function takes 4 arguments: The url for the query page, the path to save the output to, the filters for the data, and an optional argument for the file type
to save in (default is json). Because arguments like the url and filter can be very long, it is recommended that you save those in separate variables before passing them to the query function.

**Examples**: 
`SandSnapQuery(url, "output.json", valid_data_filter)`
`SandSnapQuery(url, "output.csv", beaches_in_oregon, file_type= "csv")`

Define filter parameters using the json representation for layer definitions as described in the [ArcGIS documentation](https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service/).

**Examples**
`{"layerDefs": {"0":"calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"}} ` will filter for only data without errors
`{"layerDefs": {"0":"location_state = 'OR'"}` will return all SandSnaps in Oregon

## Testing
  
The repository also includes a suite of unit tests to ensure that the query function works properly. The query function is run with both correct and incorrect parameters, and checked for proper error handling. 
The data returned by the program is checked against known data from the SandSnap website to make sure it is downloading and filtering correctly.

## Known Issues

## Dependencies

  - [requests](https://pypi.org/project/requests/)
  - [json](https://docs.python.org/3/library/json.html)
