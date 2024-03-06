return {
        colorscheme = "astrodark",
        mappings = {
            n = {
                        ["<A-j>"] = {":m+<CR>"},
                        ["<A-k>"] = {":m-2<CR>"},
            }
        },
        polish = function()
		local gitignore = require("gitignore")
                require("cmake-tools").setup {}
                vim.keymap.set("n", "<leader>gi", gitignore.generate, {desc = "Gitignore generate"})
            end,
}
