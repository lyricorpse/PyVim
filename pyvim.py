#!/usr/bin/env python3

import os
import argparse
import subprocess
import colors

home_dir = os.getenv('HOME')
work_dir = os.path.dirname(os.path.realpath(__file__)) 

vimrc_src = os.path.join(work_dir, 'vimrc')
vimrc_tgt = os.path.join(home_dir, '.vimrc')

def clean(args):

    clean_vimrc = 'rm -f ~/.vimrc'
    clean_plugins = 'rm -rf ~/.vim'

    tmp_cmds = []

    if 'vimrc' in args.target:
        print(colors.red('Cleanning vimrc...'))
        tmp_cmds.append(clean_vimrc)

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
        new_strings = []
        for line in strings.splitlines():
            new_line = line.lstrip()

            print(colors.yellow(new_line))
            with open(vimrc_tgt, 'a') as file_tmp:
                file_tmp.write(new_line + '\n')

def deploy(args):

    deploy_vimrc = 'cp ' + vimrc_src + ' ' + vimrc_tgt

    deploy_pathogen = '''
            mkdir -p ~/.vim/autoload ~/.vim/bundle && \
            curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
            '''

    tmp_cmds = []

    if 'vimrc' in args.target:
        print(colors.green('Deploying vimrc...'))
        tmp_cmds.append(deploy_vimrc)

    if 'pathogen' in args.target:
        print(colors.green('Deploying pathogen...'))
        tmp_cmds.append(deploy_pathogen)
        add_vimrc('''
        "---------------------------------------
        " Pathogen
        "---------------------------------------
        execute pathogen#infect()
        ''')

    for tmp_cmd in tmp_cmds:
        subprocess.call(tmp_cmd, shell=True)

def main():
    parser = argparse.ArgumentParser(description='PyVim: Python-Vim Deploy Script')

    parser.add_argument('-v', '--version',
            action='version',
            version='%(prog)s 0.01')

    subparsers = parser.add_subparsers(help='running mode')
    subparsers.required = True
    subparsers.dest = 'mode'

    parser_clean = subparsers.add_parser('clean',
            help='Cleanup the original Vim plugins and configures.')

    parser_clean.add_argument('-t', '--target',
            required=True,
            nargs='*',
            choices=['vimrc', 'plugins'],
            help='The target to clean.')

    parser_deploy = subparsers.add_parser('deploy',
            help='Deploy your plugins and vimrc.')

    parser_deploy.add_argument('-t', '--target',
            required=True,
            nargs='*',
            choices=['vimrc', 'pathogen'],
            help='The target to deploy.')

    args = parser.parse_args()

    if args.mode == 'clean':
        clean(args)

    elif args.mode == 'deploy':
        deploy(args)

if __name__ == '__main__':
    main()
