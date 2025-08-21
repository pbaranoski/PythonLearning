# Importing the required packages for all your data framing needs.
import os
import sys
import time
import shutil
import traceback
import arcpy
from arcpy import da
from arcpy import management
from arcpy import geocoding
from arcpy import metadata as md


def main():
    try:

        start_time = time.time()
        local_time = time.localtime()
        stime = time.strftime("%H:%M:%S", local_time)

        # print elapsed time
        print(f"Start time is {stime}\n")

        # variables  to store addres locator, sde connection, table name and Street Map file geodatabase paths.
        addr_loc = r'E:/locator/USA.loc'  # The address locator
        egdb_path = r"E:\Snowflake.sde"   # The sde connection to Snowflake database
        # address_table = "GEO_ADDRESS_TABLE"  # Used for Insert example
        address_table = "GEO_ADDRESS"  # Used for Update example
        fgdb_path = r"E:\RoutingServices\StreetData\NorthAmerica.gdb"  # The address database

        # Build field mappings for locator
        input_mappings = {"Address or Place": "ADDRESS",
                          "Address2": "<None>",
                          "Address3": "<None>",
                          "Neighborhood": "<None>",
                          "City": "CITY",
                          "State": "REGION",
                          "ZIP": "POSTAL",
                          "ZIP4": "POSTALEXT",
                          "Country": "<None>"
                          }

        # Preferred_Location_Type = 'ROUTING_LOCATION'
        Preferred_Location_Type = 'ADDRESS_LOCATION'
        out_relationship_type = 'STATIC'
        country_code = 'USA'
        category = ['Address', 'Postal', 'Coordinate System', 'Populated Place']
        Output_Fields = 'ALL'

        addr_fields = arcpy.FieldInfo()

        for field in input_mappings:
            addr_fields.addField(field, input_mappings[field], "VISIBLE", "NONE")

        # Getting metadata information from Street Map file geodatabase
        item_md = md.Metadata(fgdb_path)
        # print(item_md.title)

        # Making connection with Snowflake database using sde connection
        egdb_conn = arcpy.ArcSDESQLExecute(egdb_path)

        # Select statement to grab information from address_table of snowflake
        # sql = f'select ADDRESS, CITY, REGION, POSTAL, POSTALEXT, OBJECTID  from {address_table}'
        sql = f'select ADDRESS, CITY, REGION, POSTAL, POSTALEXT, OBJECTID  from {address_table}'

        # Executing the SQL and storing in rows list
        rows = egdb_conn.execute(sql)

        column_names = ['ADDRESS', 'CITY', 'REGION', 'POSTAL', 'POSTALEXT', 'FID']

        # make temp folders in the script directory
        temp_wksp = arcpy.CreateUniqueName("temp_wksp", os.path.dirname(sys.argv[0]))
        temp_wksp = temp_wksp.replace("\\", "/")
        temp_gdb = os.path.join(temp_wksp, "geocode_out.gdb")
        temp_gdb = temp_gdb.replace("\\", "/")

        if not os.path.exists(temp_wksp):
            os.mkdir(temp_wksp)

        if arcpy.Exists(temp_gdb):
            arcpy.management.Delete(temp_gdb)

        input_address_table = "ADDRESS_TABLE"

        # Create a filegeodatabase
        arcpy.management.CreateFileGDB(os.path.dirname(temp_gdb), os.path.basename(temp_gdb))

        # Create a table inside filegeodatabase
        arcpy.management.CreateTable(temp_gdb, input_address_table)
        input_address_table = os.path.join(temp_gdb, input_address_table)
        input_address_table = input_address_table.replace("\\", "/")

        # Adding columns to table in filegeodatabase
        arcpy.management.AddField(input_address_table, "ADDRESS", "TEXT", "", "", "300", "", "NULLABLE")
        arcpy.management.AddField(input_address_table, "CITY", "TEXT", "", "", "100", "", "NULLABLE")
        arcpy.management.AddField(input_address_table, "REGION", "TEXT", "", "", "2", "", "NULLABLE")
        arcpy.management.AddField(input_address_table, "POSTAL", "TEXT", "", "", "5", "", "NULLABLE")
        arcpy.management.AddField(input_address_table, "POSTALEXT", "TEXT", "", "", "4", "", "NULLABLE")
        arcpy.management.AddField(input_address_table, "FID", "SHORT", "", "", "38", "", "NON_NULLABLE")

        # Inserting the data into table created in filegeodatabase
        with arcpy.da.InsertCursor(input_address_table, column_names) as iCur:
            for i in rows:
                iCur.insertRow(i)
        # Output feature class name to store geocoded information
        feature_class_name = "GEO_ADDRESS_FC"
        out_feature_class = os.path.join(temp_gdb, feature_class_name)
        out_feature_class = out_feature_class.replace("\\", "/")

        # Geocoding Process using rows from table in filegeodatabase and stores in output geocoded feature class
        try:
            arcpy.geocoding.GeocodeAddresses(input_address_table, addr_loc, addr_fields, out_feature_class,
                                                      out_relationship_type, country_code, Preferred_Location_Type,
                                                      category, Output_Fields)

            print("Geocoded")
            geocoded_tablecount = arcpy.management.GetCount(out_feature_class)[0]  # debug for count

            print(("Geocoded Table Records {}".format(str(geocoded_tablecount))))  # debug for count

        except arcpy.ExecuteError:
            print(arcpy.GetMessages())

        # Searching fields
        field_names = ['Score', 'Match_addr', 'Addr_type', 'X', 'Y', 'USER_FID']

        # Grab column values from geocoded feature class using search files in SearchCursor
        try:
            feature_cur = da.SearchCursor(out_feature_class, field_names=field_names,
                                          sql_clause=(None, 'ORDER BY USER_FID ASC'))
            # oid_value = 0  # User for in Insert Statement
            for row in feature_cur:
                # oid_value += 1  # User for in Insert Statement
                score_1 = row[0]
                match_addr = row[1]
                add_type = row[2]
                x_value = row[3]
                y_value = row[4]
                streetmap_ver = item_md.title
                fid_value = row[5]

                # Insert Statement to insert into Snowflake table
                # stmt1 = f'INSERT INTO GEOCODED_ADDRESS_TABLE VALUES({oid_value}, {score_1}, \'{match_addr}\',' \
                #         f' \'{add_type}\', {x_value},{y_value}, \'{streetmap_ver}\', {fid_value})'

                # Update Statement to update Snowflake table
                stmt1 = f'UPDATE GEO_ADDRESS set SCORE = {score_1}, MATCH_ADDR = \'{match_addr}\', ' \
                        f'ADDR_TYPE = \'{add_type}\', DISPLAYX = {x_value}, DISPLAYY = {y_value},' \
                        f'STREETMAP_VERSION = \'{streetmap_ver}\' WHERE OBJECTID={fid_value}'
                egdb_conn.execute(stmt1)

            del feature_cur

            egdb_conn.commitTransaction()
        except arcpy.ExecuteError:
            print(arcpy.GetMessages())
            pass

        del rows
        # Disconnect and exit
        del egdb_conn

        local_time = time.localtime()
        end_time = time.strftime("%H:%M:%S", local_time)
        # print end time
        print(f"\nEnd Time is {end_time}")

    except:
        print((traceback.format_exc()))
	
    # finally:
    #     try:
    #         if os.path.exists(temp_wksp):
    #             shutil.rmtree(temp_wksp)
    #     except:
    #         pass
    # print elapsed time
    elapsed_time = time.strftime("%M:%S", time.gmtime(time.time() - start_time))
    print(f"Elapsed Time is {elapsed_time}")
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
