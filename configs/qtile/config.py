# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
#from qtile_extras.widget import StatusNotifier
import colours

mod = "mod4"
terminal = "alacritty"
browser = "librewolf"
emacs = "emacsclient -c -a 'emacs' "

colours = colours.DoomOne

widget_defaults = dict(
    font="sans",
    fontsize=18,
    padding=5,
)

extension_defaults = widget_defaults.copy()

layout_theme = {"border_width": 2,
                "margin": 12,
                "border_focus": colours[8],
                "border_normal": colours[0]
                }

keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun"), desc='Run Launcher'),
    Key([mod], "w", lazy.spawn(browser), desc='Web browser'),
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.spawn("dm-logout -r"), desc="Logout menu"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Grow/shrink windows left/right.
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    # Key([mod], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    # Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord([mod],"e", [
        Key([], "e", lazy.spawn(emacs), desc='Emacs Dashboard'),
        Key([], "a", lazy.spawn(emacs + "--eval '(emms-play-directory-tree \"~/Music/\")'"), desc='Emacs EMMS'),
        Key([], "b", lazy.spawn(emacs + "--eval '(ibuffer)'"), desc='Emacs Ibuffer'),
        Key([], "d", lazy.spawn(emacs + "--eval '(dired nil)'"), desc='Emacs Dired'),
        Key([], "i", lazy.spawn(emacs + "--eval '(erc)'"), desc='Emacs ERC'),
        Key([], "s", lazy.spawn(emacs + "--eval '(eshell)'"), desc='Emacs Eshell'),
        Key([], "v", lazy.spawn(emacs + "--eval '(vterm)'"), desc='Emacs Vterm'),
        Key([], "w", lazy.spawn(emacs + "--eval '(eww \"distro.tube\")'"), desc='Emacs EWW'),
        Key([], "F4", lazy.spawn("killall emacs"),
                      lazy.spawn("/usr/bin/emacs --daemon"),
                      desc='Kill/restart the Emacs daemon')
    ]),
    # Dmenu/rofi scripts launched using the key chord SUPER+p followed by 'key'
    #KeyChord([mod], "p", [
    #    Key([], "h", lazy.spawn("dm-hub -r"), desc='List all dmscripts'),
    #    Key([], "a", lazy.spawn("dm-sounds -r"), desc='Choose ambient sound'),
    #    Key([], "b", lazy.spawn("dm-setbg -r"), desc='Set background'),
    #    Key([], "c", lazy.spawn("dtos-colours -r"), desc='Choose colour scheme'),
    #    Key([], "e", lazy.spawn("dm-confedit -r"), desc='Choose a config file to edit'),
    #    Key([], "i", lazy.spawn("dm-maim -r"), desc='Take a screenshot'),
    #    Key([], "k", lazy.spawn("dm-kill -r"), desc='Kill processes '),
    #    Key([], "m", lazy.spawn("dm-man -r"), desc='View manpages'),
    #    Key([], "n", lazy.spawn("dm-note -r"), desc='Store and copy notes'),
    #    Key([], "o", lazy.spawn("dm-bookman -r"), desc='Browser bookmarks'),
    #    Key([], "p", lazy.spawn("rofi-pass"), desc='Logout menu'),
    #    Key([], "q", lazy.spawn("dm-logout -r"), desc='Logout menu'),
    #    Key([], "r", lazy.spawn("dm-radio -r"), desc='Listen to online radio'),
    #    Key([], "s", lazy.spawn("dm-websearch -r"), desc='Search various engines'),
    #    Key([], "t", lazy.spawn("dm-translate -r"), desc='Translate text')
    #])
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
#group_labels = ["", "", "", "", "", "", "", "", "",]

group_layouts = ["columns", "columns", "columns", "columns", "columns", "columns", "columns", "columns", "columns"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend(
        [
            # mod1 + number of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + number of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(border_width = 0, margin = 0),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(**layout_theme, num_stacks=2),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    layout.Tile(shift_windows = True, border_width = 0, margin = 0, ratio = 0.335),
    # layout.TreeTab(),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

def init_top_widgets():
    top_widgets_list = [
        # Set background using WordClock widget (qtile_extras)
        widget.WordClock(fontsize=70),
        widget.Image(
                 filename = "~/.config/qtile/images/logo.png",
                 scale = "False",
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)},
                 ),
        widget.Prompt(),
        widget.GroupBox(
                 fontsize = 16,
                 margin_y = 4,
                 margin_x = 5,
                 padding_y = 0,
                 padding_x = 4,
                 borderwidth = 3,
                 active = colours[8],
                 inactive = colours[1],
                 rounded = False,
                 highlight_color = colours[2],
                 highlight_method = "line",
                 this_current_screen_border = colours[7],
                 this_screen_border = colours [4],
                 other_current_screen_border = colours[7],
                 other_screen_border = colours[4],
                 disable_drag = True
                 ),
        widget.CurrentLayout(
                 foregroung = colours[1],
                 padding = 5
                 ),
        widget.Spacer(),
        widget.WindowName(),
        widget.Spacer(),
        widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
        ]
    return top_widgets_list

def init_bottom_widgets():
    bottom_widgets_list = [
        widget.TextBox(
                 "Halfwhit OS", name="system",
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show drun")}),
        widget.Spacer(),
        widget.Prompt(),
        widget.Chord(
                 chords_colours={"launch": ("#ff0000", "#ffffff"),},
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.QuickExit(),
    ]
    return bottom_widgets_list

screens = [
    Screen(
        top=bar.Bar(widgets=init_top_widgets(), size=36, margin=[0,0,5,0]),
        bottom=bar.Bar(widgets=init_bottom_widgets(), size=36, margin=[0,0,5,0])
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
wmname = "Hivemind:connected"
