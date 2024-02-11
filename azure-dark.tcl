# sberbank-style.tcl
ttk::style theme create sberbank -parent clam -settings {
    # Define colors
    set bg #ffffff
    set fg #000000
    set select_bg #0066cc
    set select_fg #ffffff
    set entry_bg #f2f2f2
    set entry_fg #000000
    set entry_border #d9d9d9
    set button_bg #0066cc
    set button_fg #ffffff
    set button_border #0066cc
    set button_text_color #ffffff
    set messagebox_bg #ffffff
    set messagebox_fg #000000

    # Set theme elements
    ttk::style configure TButton \
        -background $button_bg \
        -foreground $button_fg \
        -padding "10" \
        -borderwidth 2 \
        -relief flat \
        -font {Arial 10 bold} \
        -anchor center \
        -justify center
    ttk::style map TButton \
        -background [list active $select_bg pressed $select_bg]

    ttk::style configure TEntry \
        -fieldbackground $entry_bg \
        -foreground $entry_fg \
        -borderwidth 2 \
        -relief sunken \
        -font {Arial 10} \
        -selectforeground $select_fg \
        -selectbackground $select_bg
    ttk::style map TEntry \
        -background [list active $select_bg]

    ttk::style configure TLabel \
        -foreground $fg \
        -background $bg \
        -font {Arial 10 bold}
    ttk::style configure TFrame \
        -background $bg

    ttk::style configure TMessage \
        -background $messagebox_bg \
        -foreground $messagebox_fg \
        -font {Arial 10} \
        -justify center \
        -padding "10"
}
