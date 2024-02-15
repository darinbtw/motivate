import tkinter.ttk as ttk

def apply_custom_style():
    # Определение пользовательского стиля
    style = ttk.Style()
    style.theme_create('sber_style', parent='clam', settings={
        "TButton": {
            "configure": {
                "background": "#67b83b",
                "foreground": "white",
                "padding": 5,
                "font": ("Helvetica", 10),
                "highlightthickness": 0
            },
            "map": {
                "background": [("active", "#ff8f1c")]
            }
        }
    })
    style.theme_use('sber_style')
