# deoplete-solargraph

[deoplete.nvim](https://github.com/Shougo/deoplete.nvim) source for Ruby with [solargraph](https://github.com/castwide/solargraph).  

[![asciicast](https://asciinema.org/a/GWeqELfs2dyftEe5BHnAUjIhm.png)](https://asciinema.org/a/GWeqELfs2dyftEe5BHnAUjIhm)  

## Require

* [neovim](https://github.com/neovim/neovim)
* [deoplete.nvim](https://github.com/Shougo/deoplete.nvim)
* [solargraph](https://github.com/castwide/solargraph)
* [solargraph-utils.py](https://github.com/uplus/solargraph-utils.py)


#### Install and Setup

Install  `solargraph` and `solargraph-utils.py`.  

```bash
gem install solargraph
pip install solargraph-utils.py --user
```

Setup `solargraph`(`yard`).

```bash
yard gems 
yard config --gem-install-yri 
```

## Q&A

Q: The completion candidate is not displayed.  
A: Please execute `yard gems`.  
