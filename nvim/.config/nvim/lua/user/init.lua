return {
    colorscheme = "astrodark",
    mappings = {
        n = {
            ["<A-j>"] = {":m+<CR>"},
            ["<A-k>"] = {":m-2<CR>"},
            ["<leader>hw"] = {":HopWord<CR>", desc = "Hop Word"},
            ["<leader>hc"] = {":HopChar1<CR>", desc = "Hop one character"},
            ["<leader>ht"] = {":HopChar2<CR>", desc = "Hop two characters"},
            ["<leader>hp"] = {":HopPattern<CR>", desc = "Hop two pattern"},
            ["<tab>"] = {
                function()
                    require("astronvim.utils.buffer").nav(vim.v.count > 0 and
                                                              vim.v.count or 1)
                end,
                desc = "Next buffer"
            },
            ["<S-tab>"] = {
                function()
                    require("astronvim.utils.buffer").nav(
                        -(vim.v.count > 0 and vim.v.count or 1))
                end,
                desc = "Previous buffer"
            }
        }
    },
    polish = function()
        require "user.configs.cmake-tools"
        require "user.configs.gitignore"
        require "user.configs.codeium"
        require "user.configs.hop"
    end
}
