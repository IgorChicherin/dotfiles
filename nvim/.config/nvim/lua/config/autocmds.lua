vim.api.nvim_create_autocmd({ "BufWritePre" }, {
	group = "insert_jk_delete",
	callback = function(event)
		vim.keymap.del("i", "<A-j>")
		vim.keymap.del("i", "<A-k>")
	end,
})
