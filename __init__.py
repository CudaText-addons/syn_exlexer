import os
from sw import *
from .work import *

class Command:
    def run(self):
        folder = r'c:\SynWrite_lexers'
        while not os.path.isdir(folder):
            folder = dlg_input('Folder for zip file:', folder, '', '')
            if not folder: return
            try:
                os.mkdir(folder)
            except:
                pass

        lexers = lexer_proc(LEXER_GET_LIST, '')
        n = dlg_menu(MENU_SIMPLE, 'Lexer to export', '\n'.join(lexers))
        if n is None: return
        
        do_export(folder, lexers[n])
