return {
	{
		"neovim/nvim-lspconfig",
		opts = function()
			local keys = require("lazyvim.plugins.lsp.keymaps").get()
			-- local cmp = require("cmp")
			-- change a keymap
			keys[#keys + 1] = { "<CR>", "<cmd>:lua cmp.mapping.confirm({select = true})<cr>" }
			keys[#keys + 1] = { "<C-n>", false }
			keys[#keys + 1] = { "<C-p>", false }
			-- keys[#keys + 1] = { "<A-j>", cmp.mapping.select_next_item }
		end,
	},
}
