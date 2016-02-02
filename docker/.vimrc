set nocompatible

" size of a hard tabstop
set tabstop=4

" size of an "indent"
set shiftwidth=4

" a combination of spaces and tabs are used to simulate tab stops at a width
" other than the (hard)tabstop
set softtabstop=4

" make "tab" insert indents instead of tabs at the beginning of a line
set smarttab

" always do not use tabexpansion
set noexpandtab

"autocmd Filetype make setlocal noexpandtab
autocmd Filetype python setlocal expandtab

syntax on

set wrap

set textwidth=1000
