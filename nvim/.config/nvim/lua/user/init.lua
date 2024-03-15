return {
    colorscheme = "astrodark",
    mappings = {
        n = {
            ["<A-j>"] = {":m+<CR>"},
            ["<A-k>"] = {":m-2<CR>"},
            ["<leader>hw"] = {":HopWord<CR>", desc = "Hop Word"},
            ["<leader>hc"] = {":HopChar1<CR>", desc = "Hop one character"},
            ["<leader>ht"] = {":HopChar2<CR>", desc = "Hop two characters"},
            ["<leader>hp"] = {":HopPattern<CR>", desc = "Hop two pattern"}
        }
    },
    polish = function()
        require "user.configs.cmake-tools"
        require "user.configs.gitignore"
        require "user.configs.codeium"
        require "user.configs.hop"
    end
}
