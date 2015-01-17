#!/usr/bin/env python3

import os
import argparse
import subprocess
import colors

home_dir = os.getenv('HOME')
work_dir = os.path.dirname(os.path.realpath(__file__))

vimrc_src = os.path.join(work_dir, 'vimrc')
vimrc_tgt = os.path.join(home_dir, '.vimrc')
vimrc_bak = os.path.join(work_dir, 'vimrc_basic')

plugins = {
    'vimrc': '',
    'pathogen': 'https://tpo.pe/pathogen.vim',
    'wombat256': 'https://github.com/vim-scripts/wombat256.vim.git',
    'nerdcommenter': 'https://github.com/scrooloose/nerdcommenter.git',
    'nerdtree': 'https://github.com/scrooloose/nerdtree.git',
    'ctrlp': 'https://github.com/kien/ctrlp.vim.git',
    'airline': 'https://github.com/bling/vim-airline.git ',
    'snipmate': 'https://github.com/msanders/snipmate.vim.git',
    'pythonmode': 'https://github.com/klen/python-mode.git',
    'ncl': '',
}

configs = {
    'pathogen': '''
    "---------------------------------------
    " Plugin - Pathogen
    "---------------------------------------
    execute pathogen#infect()
    execute pathogen#helptags()
    ''',

    'wombat256': '''
    "---------------------------------------
    " Plugin - Wombat256
    "---------------------------------------
    color wombat256mod
    highlight ColorColumn ctermbg=233
    ''',

    'nerdcommenter': '''
    "---------------------------------------
    " Plugin - NerdCommenter
    "---------------------------------------
    map <c-h> ,c<space>
    map <c-l> ,cl<space>
    let NERDSpaceDelims=1
    ''',

    'nerdtree': '''
    "---------------------------------------
    " Plugin - NerdTree
    "---------------------------------------
    map <C-n> :NERDTreeToggle<CR>
    ''',

    'airline': '''
    "---------------------------------------
    " Plugin - AirLine
    "---------------------------------------
    set laststatus=2
    set encoding=utf-8

    let g:airline_theme='powerlineish'

    if !exists('g:airline_symbols')
      let g:airline_symbols = {}
    endif

    " old vim-powerline symbols
    let g:airline_left_sep = '⮀'
    let g:airline_left_alt_sep = '⮁'
    let g:airline_right_sep = '⮂'
    let g:airline_right_alt_sep = '⮃'
    let g:airline_symbols.branch = '⭠'
    let g:airline_symbols.readonly = '⭤'
    let g:airline_symbols.linenr = '⭡'
    ''',

    'pythonmode': '''
    "---------------------------------------
    " Plugin - PythonMode
    "---------------------------------------
    let g:pymode = 1
    let g:pymode_python = 'python3'
    let g:pymode_run_bind = '<leader>r'
    ''',

    'ncl': '''
    "---------------------------------------
    " Plugin - NCL
    "---------------------------------------
    au BufRead,BufNewFile *.ncl set filetype=ncl
    au! Syntax newlang source $VIM/ncl.vim

    set complete-=k complete+=k
    set wildmode=list:full
    set wildmenu
    au BufRead,BufNewFile *ncl set dictionary=~/.vim/dictionary/ncl.dic.
    ''',
}


def add_vimrc(strings):

    if not os.path.exists(vimrc_tgt):
        print(colors.red('You need to deploy vimrc first!'))
        exit()
    else:
        print(colors.green('Add configurations into vimrc...'))
        for line in strings.splitlines():
            new_line = line.lstrip()

            print(colors.yellow(new_line))
            with open(vimrc_tgt, 'a') as file_tmp:
                file_tmp.write(new_line + '\n')


def install(plugin):

    if plugin in plugins:

        if plugin == 'vimrc':

            deploy_plugin = 'cp ' + vimrc_src + ' ' + vimrc_tgt

        elif plugin == 'pathogen':

            deploy_plugin = '''
                mkdir -p ~/.vim/autoload ~/.vim/bundle && \
                curl -LSso ~/.vim/autoload/pathogen.vim ''' + plugins[plugin] + '''
            '''

        elif plugin == 'ncl':

            deploy_plugin = '''
                mkdir -p ~/.vim/syntax ~/.vim/dictionary && \
                wget http://www.ncl.ucar.edu/Applications/Files/ncl3.vim \
                    -O ~/.vim/syntax/ncl.vim && \
                wget http://www.ncl.ucar.edu/Applications/Files/ncl.dic \
                    -O ~/.vim/dictionary/ncl.dic && \
                cd ~/.vim/bundle/nerdcommenter/plugin && \
                sed 's/'ncf'/'ncl'/g' NERD_commenter.vim &> tmp && \
                mv tmp NERD_commenter.vim && \
                cd -
            '''

        else:

            deploy_plugin = '''
                cd ~/.vim/bundle && \
                git clone ''' + plugins[plugin] + ''' && \
                cd -
            '''

        subprocess.call(deploy_plugin, shell=True)

    else:

        print(colors.red('Unknown plugin!'))
        exit()


def config(plugin):

    if plugin in configs:
        add_vimrc(configs[plugin])


def deploy(args):

    # plugins
    for plugin in args.target:
        print(colors.green('\nDeploying ' + plugin + '...\n'))
        install(plugin)
        config(plugin)

    # backup vimrc
    print(colors.green('Backup updated vimrc...'))
    backup_vimrc = 'cp ' + vimrc_tgt + ' ' + vimrc_src
    subprocess.call(backup_vimrc, shell=True)


def clean(args):

    clean_vimrc = 'rm -f ~/.vimrc'
    reset_vimrc = 'cp ' + vimrc_bak + ' ' + vimrc_src
    clean_plugins = 'rm -rf ~/.vim'

    tmp_cmds = []

    if 'vimrc' in args.target:
        print(colors.red('Cleanning vimrc...'))
        tmp_cmds.append(clean_vimrc)
        tmp_cmds.append(reset_vimrc)

    if 'plugins' in args.target:
        print(colors.red('Cleanning plugins...'))
        tmp_cmds.append(clean_plugins)

    for tmp_cmd in tmp_cmds:
        subprocess.call(tmp_cmd, shell=True)


def main():

    parser = argparse.ArgumentParser(
        description='PyVim: Python-Vim Deploy Script')

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.01')

    subparsers = parser.add_subparsers(help='running mode')
    subparsers.required = True
    subparsers.dest = 'mode'

    parser_clean = subparsers.add_parser(
        'clean',
        help='Cleanup the original Vim plugins and configures.')

    parser_clean.add_argument(
        '-t', '--target',
        required=True,
        nargs='*',
        choices=['vimrc', 'plugins'],
        help='The target to clean.')

    parser_deploy = subparsers.add_parser(
        'deploy',
        help='Deploy your plugins and vimrc.')

    parser_deploy.add_argument(
        '-t', '--target',
        required=True,
        nargs='*',
        help='The target to deploy.')

    args = parser.parse_args()

    if args.mode == 'clean':
        clean(args)

    elif args.mode == 'deploy':
        deploy(args)

if __name__ == '__main__':
    main()
