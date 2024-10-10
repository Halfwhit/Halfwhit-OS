if status is-interactive
    # Commands to run in interactive sessions can go here
    set ZELLIJ_AUTO_FOCUS true
    set ZELLIJ_AUTO_EXIT true
    eval (zellij setup --generate-auto-start fish | string collect)
end
starship init fish | source
