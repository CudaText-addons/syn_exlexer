import os
from sw import *
from .work import *

FOLDER = r'c:\SynWrite_lexers'

class Command:
    def run(self):
        if app_api_version() < '1.0.142':
            msg_box(MSG_ERROR, 'ExLexer: app update needed')
            return
    
        folder = FOLDER
        while not os.path.isdir(folder):
            folder = dlg_input('Folder:', folder, '', '')
            if not folder: return
            try:
                os.mkdir(folder)
            except:
                pass

        lexers = lexer_proc(LEXER_GET_LIST, '')
        n = dlg_menu(MENU_SIMPLE, 'Lexer to export', '\n'.join(lexers))
        if n is None: return
        
        do_export(folder, lexers[n])
