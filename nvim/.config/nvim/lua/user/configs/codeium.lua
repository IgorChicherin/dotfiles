local cmp = require("cmp")
local cfg = cmp.get_config()
table.insert(cfg.sources, { name = "codeium" })
cfg.formatting.format = require('lspkind').cmp_format({
    mode = "symbol",
    maxwidth = 50,
    ellipsis_char = '...',
    symbol_map = {
        Codeium = ""
    }
})
cmp.setup(cfg)
require("codeium").setup({})

