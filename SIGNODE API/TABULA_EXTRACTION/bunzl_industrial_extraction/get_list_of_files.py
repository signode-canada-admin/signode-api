import os
import glob
import sys

def list_of_files(path, file_ending='*.pdf'):
    '''
    path = directory of files
    file_ending = type of files (default = ".pdf")
    '''
    return glob.glob(os.path.join(path, file_ending))

def paths():
    code_path = os.getcwd()
    bunzl_industrial_path = rf"Y:\Pick Ticket Project\EDI\Bunzl_industrial" #store this to .env file
    pdf_files_path_bunzl_industrial = os.path.join(bunzl_industrial_path, "PDFS_BUNZL_INDUSTRIAL")
    po_archive_path_bunzl_industrial = os.path.join(pdf_files_path_bunzl_industrial, "ARCHIVED_BUNZL_INDUSTRIAL_POs")
    sx_excel_path_bunzl_industrial = os.path.join(bunzl_industrial_path, "EXCEL_SX_BUNZL_INDUSTRIAL")
    return {
        "code": code_path,
        "root": bunzl_industrial_path,
        "pdfs": pdf_files_path_bunzl_industrial,
        "pdfs_archive": po_archive_path_bunzl_industrial,
        "sx_excel": sx_excel_path_bunzl_industrial
    }

def get_list_of_files():
    all_paths = paths()
    pdfs = list_of_files(all_paths["pdfs"])
    archived_pdfs = list_of_files(all_paths["pdfs_archive"])
    return {
        'success': 'true',
        'len' : len(pdfs),
        'list': [os.path.basename(pdf)[:-4] for pdf in pdfs],
        'archived': {
            'len': len(archived_pdfs),
            'pdfs': [os.path.basename(pdf)[:-4] for pdf in archived_pdfs]
        }
    }

try:
    print(get_list_of_files())
except Exception as e:
    ret = {
        'success': 'false',
        'len' : 0,
        'list': [],
        'archived': {
            'len': 0,
            'pdfs': [0]
        },
        'error': "unexpected error occurred"
    }
    print(ret)
sys.stdout.flush()
