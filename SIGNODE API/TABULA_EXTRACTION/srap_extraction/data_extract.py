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



def srap_data(file, area=(119.7225, 13.3875, 733.2525, 495.3375) , pages=1):
    '''
    file: source file (type: .pdf)
    pages: 1, 2, .. 1-2,   "all"
    return PP first column data (type: .json)
    
    area (line items) => area = (215.3475, 42.075, 668.2275, 127.755) (default)
    area (ship Via) => area = (665.3007518796992, 42.94736842105263, 741.2255639097745, 406.4661654135338)
    '''
    
    json_data = read_pdf(file, pages=f"{pages}", area=area, lattice=True, output_format="json")
    
    cnt = 0
    rows_data = json_data[cnt]["data"]
    while not rows_data:
        cnt+=1
        rows_data = json_data[cnt]["data"] 
    po_text = [row[1]["text"] for row in rows_data]
    line_item_text = [row[0]["text"] for row in rows_data]
    quantity_text = [row[2]["text"] for row in rows_data]

    # po = po_text.split(" ")[-1]
    po = po_text[0].split(" ")[-1].split("\r")[-1]
    ship_via = line_item_text[0].split(" ")[-1].split("\r")[-1]

    line_item = [line.strip() for line in line_item_text[3:] if line != ""]
    quantity = [line.strip() for line in quantity_text[3:] if line != ""]
    line_items = []
    for i in range(len(line_item)):
        line_item[i] = line_item[i].replace(",",".")
        line_items.append(
            {
                "quantity": quantity[i],
                "product" : line_item[i]
            }
        )

    return {
        "po_no": po,
        "num_line_items": len(line_items),
        "line_items" :line_items,
        "ship_via": ship_via,
    }


try:
    print(srap_data(rf"{sys.argv[1]}"))  
except Exception as e:
    ret = {
        "success": "false",
        "ship_via": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": "Unexpected error occured"
    }
    print(ret)

# print(srap_data("http://localhost:4000/api/edi/srap/Commande%20Signode-SRAP%20YL-807"))   
sys.stdout.flush()

