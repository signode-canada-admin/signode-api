from tabula import read_pdf
import sys
import numpy as np

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
Code_Array = ["T", "TL", "SL", "SLT","SLD","TD","NC-SL","NC-SLT","NC-SLD","NC-T","NC-TL","NC-TD"]
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

def service_order(file, area=(29.39293689727783, 343.4136804580688, 92.64356060028076, 543.5833013534545), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Service_Order_text = [row[0]["text"] for row in rows_data]
    Service_Order_No = Service_Order_text[1]
    return Service_Order_No

def customer_no(file, area=(250.3980573654175, 59.157936286926265, 265.2805570602417, 301.74268131256105), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Customer_No = ([row[1]["text"] for row in rows_data])[0]
    if len(Customer_No) != 4:
        a = Customer_No[:4]
        b = Customer_No[5:]
        Customer_No = [a,b]
    else:
        Customer_No = [Customer_No, '00']
        
    return Customer_No

def po_no(file, area=(235.51555767059327, 278.6748067855835, 268.25705699920655, 588.2308004379272), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    PO_No = ([row[1]["text"] for row in rows_data])[0]
    return PO_No

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def name(file, area=(263.0127975845337, 47.98960521697998, 295.74989261627195, 301.70209171295164), pages=1):
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    Service_name = ([row[1]["text"] for row in rows_data])
    try:
        Service_name = Service_name[0] + " " + Service_name[1]
    except:
        Service_name = Service_name[0]
        
    Name_List = ["Markham Warehouse","Vancouver Warehouse", "Nam Tran", "Timothy Hegarty", "Rahul Sharma", "Bruce Gilchrist", "Joseph Bosnjak", "Kirk Gilchrist", "Mario Kenty", "Valeriu Serban", "Daniel Jacob", "Mateus Lara", "Spencer Shlakoff"]
    Warehouse_List = ["A001", "A002", "A004", "V003", "V007", "V014", "V017", "V018", "V006", "V023", "V025", "V032", "V033"]
    
    Warehouse = " "
    x = 0
    
    for i in range(0,len(Name_List)):
        if Name_List[i] == Service_name:
            Warehouse = Warehouse_List[i]
            
    return Warehouse


def service(file, pages = "all", area=(2.6044374465942384, 4.09268741607666, 840.4891702651977, 594.183800315857)):
    Service_Order_No = service_order(file)
    Customer_No = customer_no(file)
    Ship_To = Customer_No[1]
    Customer_No = Customer_No[0]
    Warehouse = name(file)
    
    try:
        PO_No = po_no(file)
    except:
        PO_No = "NA"
    
    no_pages_json = read_pdf(file, pages="all", area=area, stream=True, output_format="json")
   
    no_of_pages = len(no_pages_json)
    
    for i in range(1,no_of_pages + 1):
        if i == 1:
            json_data = read_pdf(file, pages= 1, area=(312.9045560836792, 4.836812400817871, 841.9774202346802, 594.9279253005981), stream=True, output_format="json")
        else:
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
    
    a = json_data[0]["data"]
    b = [row[0]["text"] for row in a]
    
   
    
    c = json_data[1]["data"]
    d = [row[0]["text"] for row in c]
    
    g = 0
    for i in range(0,len(b)):
        if "Serial Number Item #" in b[i]:
            g = i
            
    for i in range(0,len(d)):
        if "5B3" in d[i]:
            h = i
            break
   
    while x != (no_of_pages):
        
        if x == 0:
            y = 1 + g
        else:
            y = 1 + h
        
        a = json_data[x]["data"]
        
        try:
            if ([row[1]["text"] for row in a][y:])[0] == '':
                n = 2
                
        except:
            pass
        
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
    
    for i in range(0,len(Column_1)):
        if "Cycle Count" in Column_1[i] or "" == Column_0[i] :
            Column_1 = Column_1[:i]
            p = i
            break
    
    for i in range(0,len(Column_0)):
        if "Technicians Report" in Column_0[i]:
            Technicians_Report = Column_0[(i+1):-1]
            break

    Column_0 = Column_0[:p]
    Column_2 = Column_2[:p]

    not_found = True
    index_work = 0
    
    for i in range(0,len(Column_0)):
        Column_0[i] = (Column_0[i].split(' '))[-1]
        
    for i in range(0,len(Column_1)):
        Column_1[i] = (Column_1[i]).replace("'", "")
        for m in range(0, len(Description_Array)):
            if Column_1[i] == Description_Array[m]:
                Column_0[i] = Code_Array[m]
                Column_1[i] = SX_Description[m]
                if not_found:
                    index_work = i
                    not_found = False
    
    counter = 0
    for j in range(0, len(Technicians_Report)):
        Technicians_Report[j] = (Technicians_Report[j]).replace("—", "-")
        Technicians_Report[j] = (Technicians_Report[j]).replace("–", "-")
        Technicians_Report[j] = (Technicians_Report[j]).replace("'", "*")
        Technicians_Report[j] = (Technicians_Report[j]).replace("’", "*")


        for k in range(0,len(Technicians_Report[j])):
            counter = counter + 1
    
    test = (counter+102) / 1024
    test2 = (int(np.ceil(test))) + 1
    test3 = list(split(Technicians_Report, test2))

    i = 0
    for i in range(test2):
        temp_line_items.append(
            {
                "product": "NOTE",
                "description" : test3[i],
                "quantity" : ''
            }
        )
    i = 0
    
    for i in range(len(Column_0)):
        Column_0[i] = Column_0[i].replace(",",".")
        line_items.append(
            {
                "product": Column_0[i],
                "description" : Column_1[i],
                "quantity" : (Column_2[i])
            }
        )
    temp_line_items_2 = line_items[index_work:]
    line_items = line_items[:index_work]
    line_items = temp_line_items + temp_line_items_2 + line_items 

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
        "ship_to": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": "Unexpected error occured"
    }
    print(ret)
      
sys.stdout.flush()