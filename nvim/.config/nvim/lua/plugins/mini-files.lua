return {
	{
		"echasnovski/mini.files",
		version = false,
		init = function()
			require("mini.files").setup()
			local map = LazyVim.safe_keymap_set

			map("n", "<leader>e", "<cmd>lua MiniFiles.open()<CR>", { desc = "Open file explorer" })
		end,
	},
}
