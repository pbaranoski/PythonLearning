import os
import traceback

temp_input = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input"
temp_output = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output"

out_dir = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\OutfolderPath"

def create_output_csv(input_table):
    try:
        
        ###if not arcpy.Exists(input_table):
        ###    return None
        # writes out only geocode fields
        ###dataList = arcpy.ListFields(input_table) # updated code for ArcGIS 10.8

        fields = ["FID", "SCORE", "MATCH_ADDR","ADDR_TYPE","DISPLAYX", "DISPLAYY"]
        
        ###rows = arcpy.da.SearchCursor(input_table, field_names=fields)
        rows = [(8, 80, "9304 Ravenridge Road", "A", "dx", "dy"),
                (3, 85, "9304 Ravenridge Road", "A", "dx", "dy"),
                (1, 90, "1313 Mockingbird Lane", "A", "dx", "dy")]
        
        ## Why are we doing this?  isn't out_addr = rows? Print statements show them to be identical
        out_addr = [row for row in rows]

        print("Rows:")
        print (rows)
        print("out_addr:")
        print(out_addr)

        sorted_out_addr = sorted(out_addr, key=lambda tup: int(tup[0]))

        out_file = os.path.join(temp_output,"FID"+os.path.basename(input_table)+ ".csv")
        with open(out_file,"w") as outfobj:
            ## Paul --> write header - iterates over fields; 
            ## The string "\t" is inserted between each item in fields.  
            # -->  String.join for array adds String between each array member           
            # "FID"	"SCORE"	"MATCH_ADDR"	"ADDR_TYPE"	"DISPLAYX"	"DISPLAYY"
            outfobj.write('"'+'"\t"'.join(fields)+'"\n') 

            ## Paul --> move code closer to its dependency
            ##out_addr = [row for row in rows]

            # all the rows sorted by FID to match up with input csv
            #### Paul sorted_out_addr = sorted(out_addr, key=lambda tup: int(tup[0]))# updated code for ArcGIS 10.8

            #sort by FID
            tab_out_addr = []

            # encode address parts if needed
            for addr in sorted_out_addr:
                line = []
                for v in addr:
                    # Note that in Python 3.x, this type was removed because all strings are now Unicode
                    # unicode is specific to Python 2. In Python 3, use str
                    #if isinstance(v, unicode):
                    if isinstance(v,str):
                        #line.append(v.encode('utf-8'))
                        # No operation instruction is "pass"
                        line.append(v)
                    else:
                        line.append(str(v))

                #convert to tabbed
                tab_out_addr.append('"'+'"\t"'.join(line)+'"\n')

            outfobj.writelines(map(str, tab_out_addr))
            outfobj.close()
        return out_file
    #except:    
        ##print traceback.format_exc()
    except (Exception) as e:
        print ("exception")
        print("Error occurred:", e)
        #Error occurred: sequence item 2: expected str instance, bytes found
        print ("errorno:" + e.__cause__)
        #TypeError: can only concatenate str (not "NoneType") to str


create_output_csv("file1_txt")       
