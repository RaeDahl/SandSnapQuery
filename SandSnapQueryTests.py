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
VICKSBURG_FILTER = [-91, 32, -90, 33]

SAVE_PATH = "unit_test_output.json"

# print status message
print("\n================================")
print("     Starting unit tests.")
print("================================")

# Test basic functionality
print("\n\033[36mTesting correct query with default parameters\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, DEFAULT_FILTER)
if os.path.exists(SAVE_PATH):
    if os.path.getsize(SAVE_PATH):
        print("\033[32mQuery and json file save successful\033[0m")
    else:
        print("\033[31mSaved file is blank\033[0m")
else:
    print("\033[31mNo file saved to save path\033[0m")

# Test error handling

# Wrong URL
print("\n\033[36mTesting error handling for incorrect urls\033[0m")
sand_snap_query(BROKEN_URL, SAVE_PATH, DEFAULT_FILTER)

# Invalid parameters
print("\n\033[36mTesting error handling for queries with invalid filter parameters\033[0m")
print("If errors are handled correctly, you should see 2 error messages print below")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, BROKEN_FILTER_1)
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, BROKEN_FILTER_2)

# Test filtering for specific data point
print("\n\033[36mTesting filtering for a specific object id\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, CANNON_BEACH_FILTER)
with open(SAVE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)
    if data:
        if data[0]["attributes"]["objectid"] == 2120:
            print("\033[32mFiltering by objectid successful\033[0m")
        else:
            print("\033[31mID 2120 does not show up in result\033[0m")
    else:
        print("\033[31mFilter by ID query unsuccessful, no data found\033[0m")

print("\n\033[36mTesting filtering for a specific state\033[0m")
sand_snap_query(CORRECT_QUERY_URL, SAVE_PATH, OREGON_FILTER)
with open(SAVE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)
    if data:
        if len(data) == 6:
            print("\033[32mFiltering by state successful\033[0m")
        elif len(data) < 6:
            print(f"\033[31mSome data points missing. Only found {len(data)} valid sandsnaps in OR, there should be 6.\033[0m")
        else:
            print(f"\033[31mExtra data found. Found {len(data)} valid sandsnaps in OR, there should only be 6\033[0m")
    else:
        print("\033[31mFilter by state query unsuccessful, no data found\033[0m")

print("\n\033[36mTesting filtering by geometry\033[0m")
sand_snap_query(CORRECT_QUERY_URL, "geometry_filter_output.json", DEFAULT_FILTER, geometry=VICKSBURG_FILTER)
with open("geometry_filter_output.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    if data:
         snap_found = False
         for sandsnap in data:
             if  sandsnap["attributes"]["objectid"] == 687:
                  print("\033[32mSandsnap known to be in area found.\033[0m")
                  snap_found = True
                  break

         if not snap_found:
             print("\033[35mID 687 does not show up in result, missing data\033[0m")

         if len(data) == 75:
             print("\033[32mCorrect number of sandsnaps found when filtering by geometry\033[0m")
         elif len(data) < 6:
             print(f"\033[31mSome data points missing. Only found {len(data)} valid sandsnaps in range, there should be 75.\033[0m")
         else:
             print(f"\033[31mExtra data found. Found {len(data)} valid sandsnaps in area, there should only be 75\033[0m")

    else:
        print("\033[31mFilter by geometry query unsuccessful, no data found\033[0m")

# print status message
print("\n================================")
print("       Testing completed.")
print("================================\n")
