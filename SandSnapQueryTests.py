'''
Description:
------------
Unit tests for SandSnap Query code
'''
# pylint: disable=line-too-long,invalid-name

import json
import os

from SandSnapQuery import sand_snap_query

CORRECT_QUERY_URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/ArcGIS/rest/services/survey123_402b0c9d9dfe4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query"
BROKEN_URL = "https://services6.arcgis.com/rZL2YPlohtwSQBWu/arcgis/rest/services/survey123_402b0ce4bcc8b4b7d6873c710fe_fieldworker/FeatureServer/query?layerDefs=%7B%220%22"

DEFAULT_FILTER = "calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"
BROKEN_FILTER_1 = "survey"
BROKEN_FILTER_2 = 0

CANNON_BEACH_FILTER = "objectid=2120"
OREGON_FILTER = "calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error' AND location_state = 'OR'"
# VICKSBURG_FILTER = {
#     "layerDefs": {"0":"calc_grain_size <> 'Unknown Grain Size' AND calc_grain_size IS NOT NULL AND unknown_error_flag = 'False' AND process_status <> 'Error'"},
#     "geometry": {"xmin":-91, "ymin":32, "xmax":-90, "ymax":33}
# }

SAVE_PATH = "unit_test_output.json"
CSV_SAVE_PATH = "unit_test_output.csv"


# Test basic functionality
print("\033[36mTesting correct query with default parameters\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, DEFAULT_FILTER)
if os.path.exists(SAVE_PATH):
    print("Query and json file save successful")
else:
    print("\033[35mNo file saved to save path\033[0m")

# Test error handling

# Wrong URL
print("\033[36mTesting error handling for incorrect urls\033[0m")
sand_snap_query(BROKEN_URL, SAVE_PATH, DEFAULT_FILTER)

# Invalid parameters
print("\033[36mTesting error handling for queries with invalid filter parameters\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, BROKEN_FILTER_1)
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, BROKEN_FILTER_2)


# Test filtering for specific data point
print("\033[36mTesting filtering for a specific object id\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, CANNON_BEACH_FILTER)
with open(SAVE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)
    if data:

        if list(filter(lambda x:x ["objectid"] == "2120", data)):
            print("Filtering by objectid successful")
        else:
            print("\033[35mID 2120 does not show up in result\033[0m")
    else:
        print("\033[35mFilter by ID query unsuccessful, no data found\033[0m")

print("\033[36mTesting filtering for a specific state\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, OREGON_FILTER)
with open(SAVE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)
    if data:
        if len(data) == 6:
            print("Filtering by state successful")
        elif len(data) < 6:
            print(f"\033[35mSome data points missing. Only found {len(data)} valid sandsnaps in OR, there should be 6.\033[0m")
        else:
            print(f"\033[35mExtra data found. Found {len(data)} valid sandsnaps in OR, there should only be 6\033[0m")
    else:
        print("\033[35mFilter by state query unsuccessful, no data found\033[0m")

# print("\033[36mTesting filtering by geometry\033[0m")
# sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, VICKSBURG_FILTER)
# with open(SAVE_PATH, "r", encoding="utf-8") as file:
#     data = json.load(file)
#     if data:
#         if list(filter(lambda x:x ["objectid"] == "687", data)):
#             print("Sandsnap known to be in area found.")
#         else:
#             print("\033[35mID 687 does not show up in result, missing data\033[0m")

#         if len(data) == 75:
#             print("Correct number of sandsnaps found when filtering by geometry")
#         elif len(data) < 6:
#             print(f"\033[35mSome data points missing. Only found {len(data)} valid sandsnaps in range, there should be 75.\033[0m")
#         else:
#             print(f"\033[35mExtra data found. Found {len(data)} valid sandsnaps in area, there should only be 75\033[0m")

#     else:
#         print("Filter by geometry query unsuccessful, no data found")
