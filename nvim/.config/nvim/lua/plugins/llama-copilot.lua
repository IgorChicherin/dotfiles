return {
  {
    "Faywyn/llama-copilot.nvim",
    requires = "nvim-lua/plenary.nvim",
    opts = {
      host = "localhost",
      port = "11434",
      model = "codellama:13b",
      max_completion_size = 15, -- use -1 for limitless
      debug = false,
    },
  },
}
