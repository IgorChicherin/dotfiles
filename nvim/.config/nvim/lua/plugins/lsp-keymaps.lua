return {
	{
		"neovim/nvim-lspconfig",
		opts = function()
			local keys = require("lazyvim.plugins.lsp.keymaps").get()
			local cmp = require("cmp")
			-- change a keymap
			keys[#keys + 1] = { "<A-j>", cmp.mapping.select_prev_item() }
			keys[#keys + 1] = { "<A-k>", cmp.mapping.select_next_item() }
			keys[#keys + 1] = { "<A-l>", cmp.mapping.confirm({ select = true }) }
			keys[#keys + 1] = { "<A-e>", cmp.mapping({
				i = cmp.mapping.abort(),
				c = cmp.mapping.close(),
			}) }
			keys[#keys + 1] = { "<CR>", cmp.mapping.confirm({ select = false }) }
			-- disable a keymap
			-- keys[#keys + 1] = { "K", false }
			-- add a keymap
		end,
	},
}
