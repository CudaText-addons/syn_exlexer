import os
from sw import *
from .zip_proc import *

def do_export(folder, lexer):
    lexer_ = lexer
    for s in '/\|`~$^&*=;:\'"<>?':
        lexer_ = lexer_.replace(s, '_') #for lexer filename (don't replace space)
    lexer__ = lexer_.replace(' ', '_') #for zip filename (replace space)
    
    links = lexer_proc(LEXER_GET_LINKS, lexer)
                                       
    fn_lex = os.path.join(app_exe_dir(), 'Data', 'lexlib', lexer_+'.lcf')
    fn_lexmap = os.path.join(app_exe_dir(), 'Data', 'lexlib', lexer_+'.cuda-lexmap')
    fn_acp = os.path.join(app_exe_dir(), 'Data', 'autocomplete', lexer_+'.acp')
    fn_inf = os.path.join(folder, 'install.inf')
    fn_zip = os.path.join(folder, 'lexer.%s.zip' % lexer__)
    
    if os.path.isfile(fn_inf):
        os.remove(fn_inf)
    if os.path.isfile(fn_zip):
        os.remove(fn_zip)

    zip_list = [fn_lex, fn_inf]
    if os.path.isfile(fn_acp):
        zip_list += [fn_acp]
    if os.path.isfile(fn_lexmap):
        zip_list += [fn_lexmap]                      
    
    with open(fn_inf, 'w') as f:
        f.write('[info]\n')
        f.write('title=%s\n' % lexer)
        f.write('type=lexer\n')
        f.write('subdir=-\n\n')
        
        lexer_index=1
        #export disabled sublexers, and increment lexer_index, 
        #and append lexers names to zip_list
        if links:
            for link in links:
                if not lexer_proc(LEXER_GET_ENABLED, link):
                    link_ = link.replace('/', '_')
                    fn_link_lex = os.path.join(app_exe_dir(), 'Data', 'lexlib', link_+'.lcf')
                    fn_link_lexmap = os.path.join(app_exe_dir(), 'Data', 'lexlib', link_+'.cuda-lexmap')
                    fn_link_acp = os.path.join(app_exe_dir(), 'Data', 'autocomplete', link_+'.acp')
                    #lexer_proc(LEXER_EXPORT, link+';'+fn_link_lex)
                    
                    if not fn_link_lex in zip_list:
                        f.write('[lexer%d]\n' % lexer_index)
                        f.write('file=%s\n' % link_)
                        
                        lexer_index += 1
                        zip_list += [fn_link_lex]
                        if os.path.isfile(fn_link_lexmap):
                            zip_list += [fn_link_lexmap]
                        if os.path.isfile(fn_link_acp):
                            zip_list += [fn_link_acp]
                
        f.write('[lexer%d]\n' % lexer_index)
        f.write('file=%s\n' % lexer_)
        if links:
            for i, link in enumerate(links):
                f.write('link%d=%s\n' % (i+1, link))
                

    #print('zip_list:', zip_list)
    make_zip_file(fn_zip, zip_list)
    
    #delete temp files
    os.remove(fn_inf)
    
    msg_box(MSG_INFO, 'Lexer exported to zip:\n'+fn_zip)
