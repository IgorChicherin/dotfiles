-- LSP keymaps
return {
	{
		"neovim/nvim-lspconfig",
		opts = function()
			local keys = require("lazyvim.plugins.lsp.keymaps").get()
			-- change a keymap
			keys[#keys + 1] = { "<CR>", "<cmd>:lua cmp.mapping.confirm({select = true})<cr>" }
			keys[#keys + 1] = { "<C-n>", false }
			keys[#keys + 1] = { "<C-p>", false }
		end,
	},
}
