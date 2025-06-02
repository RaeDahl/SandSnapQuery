# Unit tests for SandSnap Query code

from SandSnapQuery import SandSnapQuery
import json

CORRECT_QUERY_URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query?layerDefs=%7B%220%22%3A%22country+%3D+%27USA%27%22%7D&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&outSR=&datumTransformation=&applyVCSProjection=false&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&returnIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&returnZ=false&returnM=false&sqlFormat=none&f=html&token="
BROKEN_URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0ce4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query?layerDefs=%7B%220%22%3A%22calc_grain_size+%3C%3E+%27Unknown+Grain+Size%27%22%7D&geometry=-91%2C+32%2C+-90%2C+33&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&outSR=&datumTransformation=&applyVCSProjection=false&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&returnIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&returnZ=false&returnM=false&sqlFormat=none&f=html&token="

DEFAULT_FILTER = {
	"layerDefs": {"0":"calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"}
} 
BROKEN_FILTER_1 = {
	"layerDefs": "survey"} 
BROKEN_FILTER_2 = {"layerDefs": 0}

CANNON_BEACH_FILTER = {"layerDefs": {"0":"objectid=2120"}}
OREGON_FILTER = {
	"layerDefs": {"0":"calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error' AND location_state = 'OR'"}
} 
VICKSBURG_FILTER = {
	"layerDefs": {"0":"calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"}
	"geometry": {-91, 32, -90, 33}
} 

SAVE_PATH = "unit_test_output.json"
CSV_SAVE_PATH = "unit_test_output.csv"


# Test basic functionality
SandSnapQuery(CORRECT_QUERY_URL, SAVE_PATH, DEFAULT_FILTER)
if(os.path.exists(SAVE_PATH)):
	print("Query and json file save successful")
else:
	print("No file saved to save path")
	
SandSnapQuery(CORRECT_QUERY_URL, CSV_SAVE_PATH, DEFAULT_FILTER, file_type="csv")
if(os.path.exists(CSV_SAVE_PATH)):
	print("Query and csv file save successful")
else:
	print("No file saved to save path")


# Test error handling

# Wrong URL
SandSnapQuery(BROKEN_URL, SAVE_PATH, DEFAULT_FILTER)

# Invalid parameters
SandSnapQuery(CORRECT_QUERY_URL, SAVE_PATH, BROKEN_FILTER_1)
SandSnapQuery(CORRECT_QUERY_URL, SAVE_PATH, BROKEN_FILTER_2)


# Test filtering for specific data point

SandSnapQuery(CORRECT_QUERY_URL, SAVE_PATH, CANNON_BEACH_FILTER)
file = open(SAVE_PATH, r)
data = json.load(file)
if (data):

	if(list(filter(lambda x:x ["objectid"] == "2120", data))):
		print("Filtering by objectid successful)
	else:
		print("ID 2120 does not show up in result")
else:
	print("Filter by ID query unsuccessful, no data found")


SandSnapQuery(CORRECT_QUERY_URL, SAVE_PATH, OREGON_FILTER)
file = open(SAVE_PATH, r)
data = json.load(file)
if (data):

	if(len(data) == 6):
		print("Filtering by state successful)
	elif (len(data) < 6):
		print(f"Some data points missing. Only found {len(data)} valid sandsnaps in OR, there should be 6.")
	else:
		print(f"Extra data found. Found {len(data)} valid sandsnaps in OR, there should only be 6")
else:
	print("Filter by state query unsuccessful, no data found")


SandSnapQuery(CORRECT_QUERY_URL, SAVE_PATH, VICKSBURG_FILTER)
file = open(SAVE_PATH, r)
data = json.load(file)
if (data):

	if(list(filter(lambda x:x ["objectid"] == "687", data))):
		print("Sandsnap known to be in area found.")
	else:
		print("ID 687 does not show up in result, missing data")

	if(len(data) == 75):
		print("Correct number of sandsnaps found when filtering by geometry")
	elif (len(data) < 6):
		print(f"Some data points missing. Only found {len(data)} valid sandsnaps in range, there should be 75.")
	else:
		print(f"Extra data found. Found {len(data)} valid sandsnaps in area, there should only be 75")

else:
	print("Filter by geometry query unsuccessful, no data found")
