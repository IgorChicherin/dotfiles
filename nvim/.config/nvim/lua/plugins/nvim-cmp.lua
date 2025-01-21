return {
	{
		"rsh7th/nvim-cmp",
		opts = function(_, opts)
			local keys = require("lazyvim.plugins.lsp.keymaps").get()
			local cmp = require("cmp")
			opts.mapping = cmp.mapping({
				["<A-j>"] = cmp.mapping.select_prev_item(),
				["<A-k>"] = cmp.mapping.select_next_item(),
				["<A-l>"] = cmp.mapping.confirm({ select = true }),

				["<C-e>"] = cmp.mapping({
					i = cmp.mapping.abort(),
					c = cmp.mapping.close(),
				}),

				["<C-d>"] = cmp.mapping.scroll_docs(-4),
				["<C-f>"] = cmp.mapping.scroll_docs(4),

				["<A-Space>"] = cmp.mapping(cmp.mapping.complete(), { "i", "c" }),
				["<CR>"] = cmp.mapping.confirm({
					select = false,
				}),
				["<Tab>"] = cmp.mapping(function(fallback)
					if cmp.visible() then
						cmp.confirm({ behavior = cmp.ConfirmBehavior.Insert, select = true })
					elseif require("luasnip").expand_or_jumpable() then
						vim.fn.feedkeys(
							vim.api.nvim_replace_termcodes("<Plug>luasnip-expand-or-jump", true, true, true),
							""
						)
					else
						fallback()
					end
				end, { "i", "s" }),
			})
		end,
	},
}
