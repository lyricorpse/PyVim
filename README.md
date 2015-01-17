# PyVim -- The Automatic Vim Configuration System with Python

## Introduction

This is a easy tool to configurate your vim.
By default, the vim mode is Python.

## Requirement

+ Python 3
+ [colors](https://github.com/verigak/colors)

## Usage

To cleanup:

``` bash
./pyvim.py clean -t vimrc plugins
```

To deploy:

``` bash
./pyvim.py deploy -t vimrc pathogen <other-plugins>
```

## Plugins

+ [Pathogen](https://github.com/tpope/vim-pathogen)
+ [NerdCommenter](https://github.com/scrooloose/nerdcommenter)
+ [NerdTree](https://github.com/scrooloose/nerdtree)
+ [PythonMode](https://github.com/klen/python-mode)
+ [SnipMate](https://github.com/msanders/snipmate.vim)
+ [CtrlP](https://github.com/kien/ctrlp.vim)
+ [AirLine](https://github.com/bling/vim-airline)
+ [Wombat256](https://github.com/vim-scripts/wombat256.vim)

## About

Author: Feng Zhu

License: BSD
