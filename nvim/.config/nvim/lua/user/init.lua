
return {
    colorscheme = "astrodark",
    mappings = {
        n = {
            ["<A-j>"] = {":m+<CR>"},
            ["<A-k>"] = {":m-2<CR>"}
        }
    },
    polish = function()
        require "user.configs.cmake-tools"
        require "user.configs.gitignore"
        require "user.configs.autosave"
        require "user.configs.cmp"
    end
}
