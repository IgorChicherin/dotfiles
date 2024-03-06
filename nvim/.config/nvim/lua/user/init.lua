return {
        colorscheme = "astrodark",
        mappings = {
            n = {
            }
        },
        polish = function()
                require("cmake-tools").setup {}
		local gitignore = require("gitignore")
                vim.keymap.set("n", "<leader>gi", gitignore.generate, {desc = "Gitignore generate"})
            end,
}
