
from tabula import read_pdf
import sys

#Arrays to assign the correct symbol and description for Travel and Service Prices
Description_Array = ["Standard Travel",
                    "Standard Travel - Overtime",
                    "Standard Service",
                    "Standard Travel - Overtime", 
                    ]
Code_Array = ["T", "TL", "SL", "SLT",]
SX_Description = ["Travel - Regular Time", "Travel - Time 1/2", "On-Site Service - Regular", "On-Site Service - Time and 1/2",]

#Function to get the Service Order Number
def service_order(file, area=(29.39293689727783, 343.4136804580688, 92.64356060028076, 543.5833013534545), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Service_Order_text = [row[0]["text"] for row in rows_data]
    Service_Order_No = Service_Order_text[1]
    return Service_Order_No

#Function to get the Customer Number
def customer_no(file, area=(250.3980573654175, 59.157936286926265, 265.2805570602417, 301.74268131256105), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Customer_No = ([row[1]["text"] for row in rows_data])[0]
    
    #Add "-00" to the Customer Number if it's not there
    if len(Customer_No) == 4:
        Customer_No = Customer_No + "-00"
    return Customer_No

#Function to get the Purchase Order Number
def po_no(file, area=(235.51555767059327, 278.6748067855835, 268.25705699920655, 588.2308004379272), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    PO_No = ([row[1]["text"] for row in rows_data])[0]
    return PO_No

#Function to get the other parts from the pdf
def service(file, pages = "all", area=(2.6044374465942384, 4.09268741607666, 840.4891702651977, 594.183800315857)):
    
    #Using the Functions declared above to get the Service Order, Customer, & PO Numbers
    Service_Order_No = service_order(file)
    Customer_No = customer_no(file)
    
    try:
        PO_No = po_no(file)
    except:
        PO_No = "Please Fill in as the Field is Blank"
    
    json_data = read_pdf(file, pages="all", area=area, stream=True, output_format="json")
   
    no_of_pages = len(json_data)
    x = 0
    n = 1
    Column_0 = []
    Column_1 = []
    Column_2 = []
    temp_Column_0 = []
    temp_Column_1 = []
    temp_Column_2 = []
    line_items = []
    
    a = json_data[0]["data"]
    b = [row[0]["text"] for row in a]
    
    #Find out where to start taking data for the First Page
    for i in range(0,len(b)):
        if "Serial Number Item #" in b[i]:
            #tech_report = b[i:]
            g = i

    #Combine specfic columns from all the pages into one array 
    while x != (no_of_pages):
        
        if x == 0:
            y = 1 + g
        else:
            y = 6
        
        a = json_data[x]["data"]
        
        if ([row[1]["text"] for row in a][y:])[0] == '':
            n = 2
        
        b = [row[0]["text"] for row in a][y:]
        Column_0 = (temp_Column_0 + b)
        temp_Column_0 = Column_0
        
        b = [row[n]["text"] for row in a][y:]
        Column_1 = (temp_Column_1 + b)
        temp_Column_1 = Column_1
        
        b = [row[-1]["text"] for row in a][y:]
        Column_2 = (temp_Column_2 + b)
        temp_Column_2 = Column_2
        
        x = x+1
    
    #Specify the array to only include the Descriptions
    for i in range(0,len(Column_1)):
        if "Cycle Count" in Column_1[i]:
            Column_1 = Column_1[:i]
            break

    #Specify the array to only include the quantity numbers       
    for i in range(0,len(Column_2)):
        if "Machine Status" in Column_2[i]:
            Column_2 = Column_2[:i]
            break
    
    #Assign the Techincians Report to an array
    for i in range(0,len(Column_0)):
        if "Technicians Report" in Column_0[i]:
            Technicians_Report = Column_0[(i+1):-1]
            break

    #Specify the array to only include only Serial & Item #   
    for i in range(0,len(Column_0)):
        if "Machine Name" in Column_0[i]:
            Column_0 = Column_0[:i]
            break

    #Specify the array to only include the Item #        
    for i in range(0,len(Column_0)):
        Column_0[i] = (Column_0[i].split(' '))[-1]

    #Assign Specfic Item # for Descriptions without  
    for i in range(0,len(Column_1)):
        for m in range(0, len(Description_Array)):
            if Column_1[i] == Description_Array[m]:
                Column_0[i] = Code_Array[m]
                Column_1[i] = SX_Description[m]
    
    # Group the Item #, Description, & Quantity within the list of "line items"
    for i in range(len(Column_0)):
        Column_0[i] = Column_0[i].replace(",",".")
        line_items.append(
            {
                "Item #": Column_0[i],
                "Description" : Column_1[i],
                "Quantity" : Column_2[i]
            }
        )

    #Return the Purchase Order #, Customer #, Service Order #, # of Line Items,
    #Line Items (declared above), & Technicians Report
    return {
        "po_no": PO_No,
        "customer_no": Customer_No,
        "service_order": Service_Order_No,
        "num_line_items": len(line_items),
        "line_items" :line_items,
        "technicians_report": Technicians_Report
    }

# Error checking    
try:
    print(service(rf"{sys.argv[1]}"))  
except Exception as e:
    ret = {
        "success": "false",
        "ship_to": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": "Unexpected error occured"
    }
    print(ret)

# To Test on local document uncomment this line and change the file path:    
#print(service(r"C:\Users\0235897\OneDrive - Signode Industrial Group\Desktop\blank po.pdf"))   

sys.stdout.flush()