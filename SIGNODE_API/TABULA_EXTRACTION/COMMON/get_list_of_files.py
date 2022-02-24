import os
import glob
import sys

def list_of_files(path, file_ending='*.pdf'):
    '''
    path = directory of files
    file_ending = type of files (default = ".pdf")
    '''
    return glob.glob(os.path.join(path, file_ending))

# def paths():
#     code_path = os.getcwd()
#     premium_plus_path = rf"Y:\Pick Ticket Project\EDI\Premium_plus" #store this to .env file
#     pdf_files_path_premium_plus = os.path.join(premium_plus_path, "PDFS_PREMIUM_PLUS")
#     po_archive_path_premium_plus = os.path.join(pdf_files_path_premium_plus, "ARCHIVED_PREMIUM_PLUS_POs")
#     sx_excel_path_premium_plus = os.path.join(premium_plus_path, "EXCEL_SX_PREMIUM_PLUS")
#     return {
#         "code": code_path,
#         "root": premium_plus_path,
#         "pdfs": pdf_files_path_premium_plus,
#         "pdfs_archive": po_archive_path_premium_plus,
#         "sx_excel": sx_excel_path_premium_plus
#     }

def paths(site):
    code_path = os.getcwd()
    root_path = rf"Y:\Pick Ticket Project\EDI" #store this to .env file
    pdf_files = os.path.join(root_path, f"CUSTOMERS\{site}")
    po_archive = os.path.join(pdf_files, "ARCHIVED_POs")
    sx_excel_path = os.path.join(root_path, "EXCEL_SX")
    sx_excel_archive = os.path.join(sx_excel_path, "ARCHIVED")
    return {
        "code": code_path,
        "root": root_path,
        "pdfs": pdf_files,
        "pdfs_archive": po_archive,
        "sx_excel": sx_excel_path,
        "sx_excel_archive": sx_excel_archive
    }

def get_list_of_files(site):
    all_paths = paths(f"{site}")
    pdfs = list_of_files(all_paths["pdfs"])
    archived_pdfs = list_of_files(all_paths["pdfs_archive"])
    return {
        'len' : len(pdfs),
        'list': [os.path.basename(pdf)[:-4] for pdf in pdfs],
        'archived': {
            'len': len(archived_pdfs),
            'pdfs': [os.path.basename(pdf)[:-4] for pdf in archived_pdfs]
        }
    }

try:
    print(get_list_of_files(rf"{sys.argv[1]}"))
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
