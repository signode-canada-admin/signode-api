from tabula import read_pdf, read_pdf_with_template
import os
import glob
import sys


def list_of_files(path, file_ending='*.pdf'):
    '''
    path = directory of files
    file_ending = type of files (default = ".pdf")
    '''
    return glob.glob(os.path.join(path, file_ending))

def enter_directory(path):
    '''
    path = directory to enter(must be r'str')
    '''
    try: 
        os.chdir(path)
    except OSError:       
        print("Entering the directory %s failed" % path)

def move_files(src, dst):
    '''
    src = path to file (.pdf)
    dst = new path to file (.pdf)
    '''
    try:
        os.replace(src, dst)
    except:
        os.rename(src, dst)



def PP_data(file, area=(215.3475, 42.4575, 666.6975, 147.2625) , pages=1):
    '''
    file: source file (type: .pdf)
    pages: 1, 2, .. 1-2,   "all"
    return PP first column data (type: .json)
    
    area (line items) => area = (215.3475, 42.075, 668.2275, 127.755) (default)
    area (ship Via) => area = (665.3007518796992, 42.94736842105263, 741.2255639097745, 406.4661654135338)
    '''
    
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    rows_text = [row[0]["text"] for row in rows_data]
    return rows_text
    

def ret_index(data):
    '''
    data (type: []): first column of the table
    return (type: int): return index of the po_no
    
    item list starts at ret_index(data)+2
    '''
    if 'order' in data[0].lower():
        return 1
    return 0

def return_PP_dict(data=None, via_data=None):
    '''
    data (type: []): first column of the table
    
    return (type: {}): 
    {   
        "customer_name": ,
        "warehouse": ,
        "order_type": ,
        "ship_to": "",
        "ship_via": Ship Via,
        "po_no": 'Order No',
        "num_line_items": #,
        "line_items": [
            {"qty": #,
            "part_no": "str"}
        ], .....
    }
    '''
    errors = []

    start_index = ret_index(data)
    po_no = data[start_index].strip()
    if isinstance(po_no, str):
        po_no=str(po_no)
    data = data[start_index+2:]
    line_items = []
    for line in data:
        qty, part_no = line.split(" ")
        if qty.strip().isdigit():
            qty=int(qty.strip())
        else:
            errors.append({"error": "qty is not an integer", "type": "qty"})
        if isinstance(part_no.strip(), str):
            part_no=str(part_no.strip())
        line_items.append({
            "quantity": qty,
            "product": part_no
        })
    if errors:
        pass

    return {
        "ship_via": via_data,
        "po_no": po_no,
        "num_line_items": len(line_items),
        "line_items": line_items,
        "ship_to": "00",
    }


def premium_plus_extraction_algo(file):
    return return_PP_dict(PP_data(file), PP_data(file, area=(665.3007518796992, 42.94736842105263, 741.2255639097745, 406.4661654135338))[0].split()[-1])

try:
    print(premium_plus_extraction_algo(rf"{sys.argv[1]}"))  
except Exception as e:
    ret = {
        "success": "false",
        "ship_via": "",
        "ship_to": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": "Unexpected error occured"
    }
    print(ret)

# print(premium_plus_extraction_algo("http://localhost:4000/api/edi/pp/412749"))   
sys.stdout.flush()
