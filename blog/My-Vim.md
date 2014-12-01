# My-Vim

- time: 2014-09-09 12:00
- tags: Linux, Tools

---

## Plugin Manager --- [Vundle](https://github.com/gmarik/Vundle.vim)

Vundle, a Plugin Manager, makes Plugin Install&Update&Search&Clean easier. 

1.Set Up 

`$ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim`

2.Configure

在你的`.vimrc`首部添加如下信息：

``bash
set nocompatible              " be iMproved, required  
filetype off                  " required  

" set the runtime path to include Vundle and initialize  
set rtp+=~/.vim/bundle/Vundle.vim  
call vundle#begin()  
" alternatively, pass a path where Vundle should install plugins  
"call vundle#begin('~/some/path/here')  

" let Vundle manage Vundle, required  
Plugin 'gmarik/Vundle.vim'  

" The following are examples of different formats supported.  
" Keep Plugin commands between vundle#begin/end.  
" plugin on GitHub repo  
Plugin 'tpope/vim-fugitive'  
" plugin from http://vim-scripts.org/vim/scripts.html  
Plugin 'L9'  
" Git plugin not hosted on GitHub  
Plugin 'git://git.wincent.com/command-t.git'  
" git repos on your local machine (i.e. when working on your own plugin)  
Plugin 'file:///home/gmarik/path/to/plugin'  
" The sparkup vim script is in a subdirectory of this repo called vim.  
" Pass the path to set the runtimepath properly.  
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}  
" Avoid a name conflict with L9  
Plugin 'user/L9', {'name': 'newL9'}  

" All of your Plugins must be added before the following line  
call vundle#end()            " required  
filetype plugin indent on    " required  
" To ignore plugin indent changes, instead use:  
"filetype plugin on  
"  
" Brief help  
" :PluginList       - lists configured plugins  
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate  
" :PluginSearch foo - searches for foo; append `!` to refresh local cache  
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal  
"  
" see :h vundle for more details or wiki for FAQ  
" Put your non-Plugin stuff after this line
```

3.Install Plugin 

如果欲安装的插件在Github上有其仓库，比如[vim-markdown](https://github.com/plasticboy/vim-markdown).

只需vim your `.vimrc`, 在里头添加一行Plugin 'plasticboy/vim-markdown'

之后vim命令行模式下,`:PluginInstall`

（当然安装插件也支持非Github库，具体看刚刚粘帖的配置文件，以及无用插件清除:PluginClean等命令都可以在刚刚的配置文件中查看）

## Vim配色-Molokai

将下载的molokai.vim放入~/.vim/color

vim `.vimrc`, 添加

```bash
syntax enabl  
set t_Co=256
colorscheme molokai
```

代码缩进显示-[vim-indent-guides](https://github.com/nathanaelkane/vim-indent-guides)

安装见Github链接，看一下`.vimrc`下的配置：

```bash
" vim-indent-guides
let g:indent_guides_enable_on_vim_startup = 1
let g:indent_guides_auto_colors = 0
let g:indent_guides_guide_size = 1
autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=red   ctermbg=3
autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=green ctermbg=4
hi IndentGuidesOdd guibg=red ctermbg=3
hi IndentGuidesEven guibg=green ctermbg=4
```

## 目录树插件-NERDTree

![Vim目录树插件](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/NERDTree.png)

Vim命令行模式下`:NERDTree`,窗口切换`ctrl+w+h/l`

## Vim补全

网络上都推荐YCM代码补全超级插件,安装和配置都好繁琐,而且平时不写C-Family代码,Vim主要用来写py,所以用了安装简便的[jedi-vim](https://github.com/davidhalter/jedi-vim)

当然可以用Vundle安装,而且也不需要`.vimrc`的配置

![Vim代码补全](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/jedi-vim.png)

(全文完-2014-09-09)
