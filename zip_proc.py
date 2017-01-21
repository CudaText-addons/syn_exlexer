import os
import zipfile

def make_zip_file(fn_zip, file_list):
    """ Makes zip ignoring files paths, all files in zip root """
    with zipfile.ZipFile(fn_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fn in file_list:
            zf.write(fn, os.path.basename(fn))
