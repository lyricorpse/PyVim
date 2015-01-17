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


def deploy(args):

    tmp_cmds = []

    deploy_vimrc = 'cp ' + vimrc_src + ' ' + vimrc_tgt
    backup_vimrc = 'cp ' + vimrc_tgt + ' ' + vimrc_src

    if 'vimrc' in args.target:
        print(colors.green('Deploying vimrc...'))
        subprocess.call(deploy_vimrc, shell=True)

    # plugin manager
    deploy_pathogen = '''
            mkdir -p ~/.vim/autoload ~/.vim/bundle && \
            curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
            '''

    if 'pathogen' in args.target:
        print(colors.green('Deploying pathogen...'))
        tmp_cmds.append(deploy_pathogen)
        add_vimrc('''
        "---------------------------------------
        " Plugin - Pathogen
        "---------------------------------------
        execute pathogen#infect()
        execute pathogen#helptags()
        ''')

    # plugins
    #
    deploy_wombat256 = '''
            cd ~/.vim/bundle && \
            git clone https://github.com/vim-scripts/wombat256.vim.git && \
            cd -
            '''

    if 'wombat256' in args.target:
        print(colors.green('Deploying wombat256...'))
        tmp_cmds.append(deploy_wombat256)
        add_vimrc('''
        "---------------------------------------
        " Plugin - Wombat256
        "---------------------------------------
        color wombat256mod
        highlight ColorColumn ctermbg=233
        ''')
    #
    deploy_nerdcommenter = '''
            cd ~/.vim/bundle && \
            git clone https://github.com/scrooloose/nerdcommenter.git && \
            cd -
            '''

    if 'nerdcommenter' in args.target:
        print(colors.green('Deploying nerdcommenter...'))
        tmp_cmds.append(deploy_nerdcommenter)
        add_vimrc('''
        "---------------------------------------
        " Plugin - NerdCommenter
        "---------------------------------------
        map <c-h> ,c<space>
        let NERDSpaceDelims=1
        ''')

    #
    deploy_ctrlp = '''
            cd ~/.vim/bundle && \
            git clone https://github.com/kien/ctrlp.vim.git && \
            cd -
            '''

    if 'ctrlp' in args.target:
        print(colors.green('Deploying ctrlp...'))
        tmp_cmds.append(deploy_ctrlp)

    #
    deploy_airline = '''
            cd ~/.vim/bundle && \
            git clone https://github.com/bling/vim-airline.git && \
            cd -
            '''

    if 'airline' in args.target:
        print(colors.green('Deploying airline...'))
        tmp_cmds.append(deploy_airline)
        add_vimrc('''
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
        ''')

    #
    deploy_pythonmode = '''
            cd ~/.vim/bundle && \
            git clone https://github.com/klen/python-mode.git && \
            cd -
            '''

    if 'pythonmode' in args.target:
        print(colors.green('Deploying pythonmode...'))
        tmp_cmds.append(deploy_pythonmode)
        add_vimrc('''
        "---------------------------------------
        " Plugin - PythonMode
        "---------------------------------------
        let g:pymode = 1
        ''')

    print(colors.green('Backup updated vimrc...'))
    subprocess.call(backup_vimrc, shell=True)

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
