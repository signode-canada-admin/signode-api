from tabula import read_pdf
import sys
import numpy as np

#Array of the descriptions for service hours that come from D365
Description_Array = ["Standard Travel",
                    "Standard Travel - Overtime",
                    "Standard Service",
                    "Standard Service - Overtime",
                    "Standard Service - Double Time",
                    "Standard Travel - Double Time",
                    "SMA Labor",
                    "SMA Labor - Overtime",
                    "SMA Labor - Double Time",
                    "SMA Travel",
                    "SMA Travel - Overtime",
                    "SMA Travel - Double Time" 
                    ]

#Corresponding SX codes for the D365 descriptions in the above array
Code_Array = ["T", "TL", "SL", "SLT","SLD","TD","NC-SL","NC-SLT","NC-SLD","NC-T","NC-TL","NC-TD"]

#Corresponding SX descriptions for the D365 descriptions in the first array 
SX_Description = ["Travel - Regular Time", 
                "Travel - Time 1/2", 
                "On-Site Service - Regular", 
                "On-Site Service - Time and 1/2",
                "Service Double Time",
                "Travel Double Time",
                "Service Regular No Charge",
                "Service Time and 1/2 no Charge",
                "Service Double Time No Charge",
                "Travel Regular No Charge",
                "Travel Time and 1/2 No Charge",
                "Travel Double Time No Charge"]

#Function to extract only the service Order number
def service_order(file, area=(29.39293689727783, 343.4136804580688, 92.64356060028076, 543.5833013534545), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Service_Order_text = [row[0]["text"] for row in rows_data]
    Service_Order_No = Service_Order_text[1]
    return Service_Order_No

#Function to extract only the Customer #
def customer_no(file, area=(250.3980573654175, 59.157936286926265, 265.2805570602417, 301.74268131256105), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Customer_No = ([row[1]["text"] for row in rows_data])[0]
    #Check if the Customer # contains the Ship-To Number
    if len(Customer_No) != 4:
        a = Customer_No[:4]
        b = Customer_No[5:]
        Customer_No = [a,b]
    #If not, then set a default value of '00'
    else:
        Customer_No = [Customer_No, '00']
        
    return Customer_No

#Function to extract only the PO #
def po_no(file, area=(235.51555767059327, 278.6748067855835, 268.25705699920655, 588.2308004379272), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    PO_No = ([row[1]["text"] for row in rows_data])[0]
    return PO_No

#Function used later on to spilt the Techi
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

#Function to get the name of the Technician from the report 
def name(file, area=(263.0127975845337, 47.98960521697998, 295.74989261627195, 301.70209171295164), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Service_name = ([row[1]["text"] for row in rows_data])
    #Depending on the length of the name, it could be in different columns/rows
    try:
        Service_name = Service_name[0] + " " + Service_name[1]
    except:
        Service_name = Service_name[0]
    
    #Array of Technician and Warehouse names
    Name_List = ["Markham Warehouse","Vancouver Warehouse", "Nam Tran", 
                "Timothy Hegarty", "Rahul Sharma", "Bruce Gilchrist", 
                "Joseph Bosnjak", "Kirk Gilchrist", "Mario Kenty", 
                "Valeriu Serban", "Daniel Jacob", "Mateus Lara", 
                "Spencer Shlakoff"]
    
    #Array of the Corresponding Warehouse codes to the Technician/Warehouse names
    Warehouse_List = ["A001", "A002", "A004", "V003", "V007", "V014", "V017", "V018", "V006", "V023", "V025", "V032", "V033"]
    
    Warehouse = " "
    x = 0
    #Assign the Warehouse Code by matching the Technician Name on the report with the "Name List" Array
    for i in range(0,len(Name_List)):
        if Name_List[i] == Service_name:
            Warehouse = Warehouse_List[i]
            
    return Warehouse

#Main function that is called to start the Extraction process
def service(file, pages = "all", area=(2.6044374465942384, 4.09268741607666, 840.4891702651977, 594.183800315857)):
    #Calling and Assigning all the function defined above
    Service_Order_No = service_order(file)
    Customer_No = customer_no(file)
    Ship_To = Customer_No[1]
    Customer_No = Customer_No[0]
    Warehouse = name(file)
    
    #In the case that a PO # hasn't been assigned give it a value of "NA"
    try:
        PO_No = po_no(file)
    except:
        PO_No = "NA"
    
    #Get the raw extracted data from all the pages
    no_pages_json = read_pdf(file, pages="all", area=area, stream=True, output_format="json")
    
    #Calculate the number of pages in the pdf
    no_of_pages = len(no_pages_json)
    
    #Uses a different area for the first page to ensure consistent formatting 
    for i in range(1,no_of_pages + 1):
        if i == 1:
            json_data = read_pdf(file, pages= 1, area=(312.9045560836792, 4.836812400817871, 841.9774202346802, 594.9279253005981), stream=True, output_format="json")
        else:
            #Extracts data page by page and adds the data to one list
            temp_json_data = read_pdf(file, pages = i, area=area, stream=True, output_format="json")
            json_data = json_data + temp_json_data
                  
    x = 0
    n = 1
    Column_0 = []
    Column_1 = []
    Column_2 = []
    temp_Column_0 = []
    temp_Column_1 = []
    temp_Column_2 = []
    line_items = []
    temp_line_items = []
    
    #Get the first column of data
    a = json_data[0]["data"]
    b = [row[0]["text"] for row in a]
    
    #Get the second column of data
    c = json_data[1]["data"]
    d = [row[0]["text"] for row in c]
    
    g = 0

    #This loop find the row where the line items start for the first page
    for i in range(0,len(b)):
        if "Serial Number Item #" in b[i]:
            g = i
    
    #This loop finds where the line items start past the first page
    for i in range(0,len(d)):
        if "5B3" in d[i]:
            h = i
            break
   
   #This loop filters each column on each page and adds them to one array
    while x != (no_of_pages):
        
        if x == 0:
            y = 1 + g
        else:
            y = 1 + h
        
        a = json_data[x]["data"]
        
        #Checks if there is an empty column in the extracted data
        try:
            if ([row[1]["text"] for row in a][y:])[0] == '':
                n = 2
                
        except:
            pass
        
        #Column for the Item Code / Product Number and the Technicians Report
        b = [row[0]["text"] for row in a][y:]
        Column_0 = (temp_Column_0 + b)
        temp_Column_0 = Column_0
        
        #Column for the Product Description
        b = [row[n]["text"] for row in a][y:]
        Column_1 = (temp_Column_1 + b)
        temp_Column_1 = Column_1
        
        #Column for the quantity of products used
        b = [row[-1]["text"] for row in a][y:]
        Column_2 = (temp_Column_2 + b)
        temp_Column_2 = Column_2
        
        x = x+1
    
    # Loop to find where the line items end 
    for i in range(0,len(Column_1)):
        if "Cycle Count" in Column_1[i] or "" == Column_0[i] :
            Column_1 = Column_1[:i]
            p = i
            break
    
    #Seperate the Technicians Report from the Product Numbers
    for i in range(0,len(Column_0)):
        if "Technicians Report" in Column_0[i]:
            Technicians_Report = Column_0[(i+1):-1]
            break
    
    #Restrict the columns for product numbers and quantity using the position found above "p"
    Column_0 = Column_0[:p]
    Column_2 = Column_2[:p]

    not_found = True
    index_work = 0
    
    #Seperate the D365 # and the SX # and assign Column 0 only the SX #
    for i in range(0,len(Column_0)):
        Column_0[i] = (Column_0[i].split(' '))[-1]

    #Format the Description and Product # Correctly    
    for i in range(0,len(Column_1)):
        Column_1[i] = (Column_1[i]).replace("'", "")
        #For the work/labour codes, search the "Description_Array" to match with the product descriptions 
        #Found found switch both the description and product number with the SX version
        for m in range(0, len(Description_Array)):
            if Column_1[i] == Description_Array[m]:
                Column_0[i] = Code_Array[m]
                Column_1[i] = SX_Description[m]
                if not_found:
                    index_work = i
                    not_found = False
    
    counter = 0
    
    #Formatting the Technicians_Report to remove any illegal characters when converting to JSON
    for j in range(0, len(Technicians_Report)):
        Technicians_Report[j] = (Technicians_Report[j]).replace("—", "-")
        Technicians_Report[j] = (Technicians_Report[j]).replace("–", "-")
        Technicians_Report[j] = (Technicians_Report[j]).replace("'", "*")
        Technicians_Report[j] = (Technicians_Report[j]).replace("’", "*")

        #Find how many characters are in the Technicians_Report
        for k in range(0,len(Technicians_Report[j])):
            counter = counter + 1
    
    #Calculations to split the Technicians_Report as there is a 1024 character limit per description
    test = (counter+102) / 1024
    test2 = (int(np.ceil(test))) + 1
    test3 = list(split(Technicians_Report, test2))

    i = 0

    #Putting the Technicians Report in the correct format
    for i in range(test2):
        temp_line_items.append(
            {
                "product": "NOTE",
                "description" : test3[i],
                "quantity" : ''
            }
        )
    i = 0
    
    #Putting the line items into the correct format
    for i in range(len(Column_0)):
        Column_0[i] = Column_0[i].replace(",",".")
        line_items.append(
            {
                "product": Column_0[i],
                "description" : Column_1[i],
                "quantity" : (Column_2[i])
            }
        )
    
    #Moving all the labour/work items to the top of the Line Items
    temp_line_items_2 = line_items[index_work:]
    line_items = line_items[:index_work]

    #Join the Formatted Technicians Report and the Formatted Line Items
    line_items = temp_line_items + temp_line_items_2 + line_items 

    #Return all the extracted data in specfic variables 
    return {
        "po_no": PO_No,
        "customer_no": Customer_No,
        "reference": Service_Order_No,
        "num_line_items": len(line_items),
        "line_items" :line_items,
        "ship_via" :"SC",
        "ship_to" :Ship_To,
        "warehouse": Warehouse
    }

try:
    print(service(rf"{sys.argv[1]}")) 
except Exception as e:
    ret = {
        "success": "false",
        "po_no": "",
        "customer_no": "",
        "reference": "",
        "num_line_items": "",
        "line_items" : "",
        "ship_via" :"",
        "ship_to" :"",
        "warehouse": "",
        "error": "Please Inform CI Team"
    }
    print(ret)
      
sys.stdout.flush()