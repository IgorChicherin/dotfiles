-- Pull in the wezterm API
local wezterm = require("wezterm")

-- This will hold the configuration.
local config = wezterm.config_builder()

local is_darwin = wezterm.target_triple:find("darwin") ~= nil
local is_linux = wezterm.target_triple:find("linux") ~= nil
local is_windows = wezterm.target_triple:find("windows") ~= nil

if is_linux then
	-- Hyprland fix
	config.enable_wayland = false
end

if is_windows then
	config.default_prog = { "powershell" }
end

-- Window decoration
config.window_decorations = "RESIZE"

-- Tab bar configuration
config.tab_bar_at_bottom = true
config.hide_tab_bar_if_only_one_tab = true
config.use_fancy_tab_bar = false
config.warn_about_missing_glyphs = false

-- Color scheme
local function scheme_for_appearance(appearance)
	if appearance:find("Dark") then
		return "Tokyo Night"
	else
		return "Tokyo Night Day"
	end
end

wezterm.on("window-config-reloaded", function(window, pane)
	local overrides = window:get_config_overrides() or {}
	local appearance = window:get_appearance()
	local scheme = scheme_for_appearance(appearance)
	if overrides.color_scheme ~= scheme then
		overrides.color_scheme = scheme
		local s = wezterm.color.get_builtin_schemes()[scheme]
		s.tab_bar.background = s.background
		s.tab_bar.new_tab.bg_color = s.background
		overrides.colors = s
		window:set_config_overrides(overrides)
	end
end)
config.tab_max_width = 10000

-- and finally, return the configuration to wezterm
return config
