return {
	{
		"Faywyn/llama-copilot.nvim",
		requires = "nvim-lua/plenary.nvim",
		{
			host = "localhost",
			port = "11434",
			model = "deepseek-r1:14b",
			max_completion_size = 15, -- use -1 for limitless
			debug = false,
		},
	},
}
