scriptencoding utf-8
"=============================================================================
"
" Fichier de configuration VIM personnalisé (meilleur pour la programmation,
" raccourcis clavier utiles, etc. pour mieux profiter de cet excellent
" éditeur).
"
" Auteur : Achraf cherti (aka Asher256)
" Email  : achraf at cherti dot name
"
" Licence : GPL
"
" Site: http://achraf.cherti.name/
"
"=============================================================================

" Options {{{1

" Options Internes {{{2

" Mode non compatible avec Vi
set nocompatible 

" Le backspace
set backspace=indent,eol,start

" Activer la sauvegarde
set backup

" un historique raisonnable
set history=100

" undo, pour revenir en arrière
set undolevels=150

" Suffixes à cacher
set suffixes=.jpg,.png,.jpeg,.gif,.bak,~,.swp,.swo,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc,.pyc,.pyo

" Backup dans ~/.vim/backup
if filewritable(expand("~/.vim/backup")) == 2
    " comme le répertoire est accessible en écriture,
    " on va l'utiliser.
	set backupdir=$HOME/.vim/backup
else
	if has("unix") || has("win32unix")
        " C'est c'est un système compatible UNIX, on
        " va créer le répertoire et l'utiliser.
		call system("mkdir $HOME/.vim/backup -p")
		set backupdir=$HOME/.vim/backup
	endif
endif

" Inclusion d'un autre fichier avec des options
if filereadable(expand("~/.vimrc_local.vim"))
    source ~/.vimrc_local.vim
endif

" Activation de la syntaxe
if has("syntax")
    syntax on
endif

" Quand un fichier est changé en dehors de Vim, il est relu automatiquement
set autoread

" Aucun son ou affichage lors des erreurs
set errorbells
set novisualbell
set t_vb=

" Quand une fermeture de parenthèse est entrée par l'utilisateur,
" l'éditeur saute rapidement vers l'ouverture pour montrer où se
" trouve l'autre parenthèse. Cette fonction active aussi un petit
" beep quand une erreur se trouve dans la syntaxe.
set showmatch
set matchtime=2

" Afficher la barre d'état
set laststatus=2

" }}}2

" Options de recherche {{{2 

" Tout ce qui concerne la recherche. Incrémentale
" avec un highlight. Elle prend en compte la
" différence entre majuscule/minuscule.
set incsearch
set noignorecase
set infercase

" Quand la rechercher atteint la fin du fichier, pas
" la peine de la refaire depuis le début du fichier
set hlsearch

" }}}2

" Options d'affichage texte {{{2

" Ne pas nous afficher un message quand on enregistre un readonly
set writeany

" Afficher les commandes incomplètes
set showcmd

" Afficher la position du curseur
set ruler

" Désactiver le wrapping
set nowrap

" Options folding
set foldmethod=marker

" Un petit menu qui permet d'afficher la liste des éléments
" filtrés avec un wildcard
set wildmenu
set wildignore=*.o,*#,*~,*.dll,*.so,*.a
set wildmode=full

" Format the statusline
set statusline=%F%m\ %r\ Line:%l\/%L,%c\ %p%%

" }}}2

" Options d'affichage GUI {{{2

" Configuration de la souris en mode console
" ="" pas de souris par défaut
set mouse=a

" Améliore l'affichage en disant à vim que nous utilisons un terminal rapide
set ttyfast

" Lazy redraw permet de ne pas mettre à jour l'écran
" quand un script vim est entrain de faire une opération
set lazyredraw

if has("gui_running")
	map <S-Insert> <MiddleMouse>
	map <S-Insert> <MiddleMouse>

	set mousehide " On cache la souris en mode gui
	set ch=2 " ligne de commande dans deux ligne
endif

" }}}2

" Noms des fichiers {{{2

" faire en sorte que le raccourci CTRL-X-F
" marche même quand le fichier est après
" le caractère égal. Comme : 
" variable=/etc/<C-XF>
set isfname-==

" }}}2

" }}}1

" Autocmd {{{1

set cindent
"set autoindent
"set smartindent

if has("autocmd")
	" Détection auto du format
	" + activer indent
	filetype plugin indent on

    augroup divers " {{{2
        au!
		" Textwidth de 78 pour tous les fichiers texte
		autocmd FileType text setlocal textwidth=78
		
		" Remet la position du curseur comme elle était avant
		autocmd BufReadPost *
		\ if line("'\"") > 0 && line("'\"") <= line("$") |
		\   exe "normal g`\"" |
		\ endif

        " La valeur des tabs par défaut
        autocmd BufNewFile,BufRead * call ChangeTabSize(4, 0)

		" Ne pas faire de wrap dans les fichiers ChangeLog
		autocmd BufNewFile,BufRead ChangeLog set nowrap textwidth=0
		autocmd BufNewFile,BufRead ChangeLog call ChangeTabSize(8, 0)

        " PKGBUILD
		autocmd BufNewFile,BufRead PKGBUILD set syntax=sh
    augroup END " }}}2

    augroup python "{{{2
        au!
        autocmd BufRead,BufNewFile *.py,*pyw set shiftwidth=4
        autocmd BufRead,BufNewFile *.py,*.pyw set expandtab
        
    augroup END "}}}2

    augroup pdf " {{{2
        au!
		autocmd BufReadPre *.pdf set ro
		autocmd BufReadPost *.pdf %!pdftotext -nopgbrk "%" - | fmt -csw78
    augroup END " }}}2
endif

" }}}1

" Fonctions {{{1

" Fonctions utilisée par vimrc {{{2

function! ChangeTabSize(tab_size, expandtab)
    execute("set tabstop=".a:tab_size." softtabstop=".a:tab_size." shiftwidth=".a:tab_size)

    if a:expandtab != 0
        execute("set expandtab")
    else
        execute("set noexpandtab")
    endif
endfunction

" }}}2

" Les fonctions utiles pour l'utilisateur {{{2

" Aller dans le répertoire du fichier édité.
function! ChangeToFileDirectory()
	if bufname("") !~ "^ftp://" " C'est impératif d'avoir un fichier local !
		lcd %:p:h
	endif
endfunction

map ,fd :call ChangeToFileDirectory()<CR>

" Entrer la commande ":e" dans le répertiore du fichier édité
if has("unix")
    map ,e :e <C-R>=expand("%:p:h") . "/" <CR>
else
    map ,e :e <C-R>=expand("%:p:h") . "\" <CR>
endif

" }}}2

" }}}1

" Raccourcis clavier {{{1

" Vim 7 spell checker
if has("spell")
    setlocal spell spelllang=
    " Language : FR
    map ,lf :setlocal spell spelllang=fr<cr>
    " Language : EN
    map ,le :setlocal spell spelllang=en<cr>
    " Language : Aucun
    map ,ln :setlocal spell spelllang=<cr>
endif

set spellsuggest=5
autocmd BufEnter *.txt set spell
autocmd BufEnter *.txt set spelllang=fr

" Tabs
map ,t :tabnew<cr>
map ,w :tabclose<cr>
imap <C-t> <Esc><C-t>
imap <C-w> <Esc><C-w>
map <tab> gt 

" Cacher le menu
map ,m :set guioptions=+M<cr>

" Mode normal
map ,mn :set guifont=<cr>

" Mode programmation
map ,mp :set guifont=Monospace\ 9<cr>

" Sélectionner tout
map <C-a> ggVG

" Copier (le gv c'est pour remettre le sélection)
map <C-c> "+ygv

" Couper
map <C-x> "+x

" Coller
map <C-p> "+gP

" Désactiver le highlight (lors d'une recherche par exemple)
map <F2> :let @/=""<cr>

" Convertir un html
map ,h :runtime syntax/2html.vim<cr>

" encoder rapidement
map ,c ggVGg?

" }}}1

" Les plugins Vim et leurs options {{{1

" Gérer les fichiers man
runtime ftplugin/man.vim 

" }}}1

" vim:ai:et:sw=4:ts=4:sts=4:tw=78:fenc=utf-8:foldmethod=marker
