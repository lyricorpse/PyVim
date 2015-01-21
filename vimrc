"=======================================
" Vim Config
"---------------------------------------
" Author: Feng Zhu
" Update: 2014-02-18 22:34:31
" Version: 1.2.0
"=======================================

"---------------------------------------
" Basic settings
"---------------------------------------
set nocompatible

" Disable backup and swp
set nobackup
set noswapfile
set nowritebackup

" Leader key
let mapleader=","

" Highlignting
syntax on
filetype plugin indent on

" Ctags
set tags+=^tags

" Remember last position
autocmd BufReadPost *
        \ if line("'\"") > 0 && line("'\"") <= line("$") |
        \   exe "normal g`\"" |
        \ endif

set autochdir

" Show whitespace
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
au InsertLeave * match ExtraWhitespace /\s\+$/

" Color scheme
set t_Co=256

" Show command
set showcmd
set scrolloff=6

" Lines
set number
set tw=79
set nowrap
set fo-=t " don't automatically wrap text when typing
set colorcolumn=90

" Formatting of paragraphs
vmap Q gq
nmap Q gqap

" Undo
set history=700
set undolevels=700

" Indent
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4

vnoremap < <gv
vnoremap > >gv

" Chinese encoding
set ambiwidth=double
set fencs=utf-8,gb18030,utf-16,big5

" Searching
set ignorecase
set smartcase
set wrapscan
set incsearch
set hlsearch

noremap <Leader>n :nohl<CR>
vnoremap <Leader>n :nohl<CR>
inoremap <Leader>n :nohl<CR>

" Tabs
noremap ct :tabnew<CR>

" Windows
"map <c-j> <c-w>j
"map <c-k> <c-w>k
"map <c-l> <c-w>l
"map <c-h> <c-w>h

" Pairing
inoremap ( ()<ESC>i
inoremap ) <c-r>=ClosePair(')')<CR>
inoremap { {}<ESC>i
inoremap } <c-r>=ClosePair('}')<CR>
inoremap [ []<ESC>i
inoremap ] <c-r>=ClosePair(']')<CR>

function ClosePair(char)
if getline('.')[col('.') - 1] == a:char
        return "\<Right>"
else
	return a:char
endif
endfunction

" Inserting system time
nmap <silent><leader>t i <c-r>=strftime("%Y-%m-%d %H:%M:%S")<cr>

" Sort
vnoremap <Leader>s :sort<CR>


"---------------------------------------
" Plugin - Pathogen
"---------------------------------------
execute pathogen#infect()
execute pathogen#helptags()


"---------------------------------------
" Plugin - Wombat256
"---------------------------------------
color wombat256mod
highlight ColorColumn ctermbg=233


"---------------------------------------
" Plugin - NerdCommenter
"---------------------------------------
map <c-h> ,c<space>
map <c-l> ,cl<space>
let NERDSpaceDelims=1


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


"---------------------------------------
" Plugin - PythonMode
"---------------------------------------
let g:pymode = 1
let g:pymode_python = 'python3'
let g:pymode_run_bind = '<leader>r'
let g:pymode_folding = 0
let g:pymode_rope_complete_on_dot = 0


"---------------------------------------
" Plugin - NerdTree
"---------------------------------------
map <C-n> :NERDTreeToggle<CR>


"---------------------------------------
" Plugin - Markdown
"---------------------------------------
let g:vim_markdown_folding_disabled=1
let g:vim_markdown_math=1
let g:vim_markdown_frontmatter=1
let g:vim_markdown_no_default_key_mappings=1


"---------------------------------------
" Plugin - NCL
"---------------------------------------
au BufRead,BufNewFile *.ncl set filetype=ncl
au! Syntax newlang source $VIM/ncl.vim

set complete-=k complete+=k
set wildmode=list:full
set wildmenu
au BufRead,BufNewFile *ncl set dictionary=~/.vim/dictionary/ncl.dic

