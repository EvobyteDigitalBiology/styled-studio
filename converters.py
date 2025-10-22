def hex_with_alpha_to_hex(hex_color, bg_color="#FFFFFF"):
    """
    Convert a hex color with alpha (#RRGGBBAA) to a normal hex (#RRGGBB)
    by blending it over a background color (default white).
    """
    hex_color = hex_color.strip('#')
    bg_color = bg_color.strip('#')

    if len(hex_color) == 8:
        r_fg, g_fg, b_fg, a = [int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6)]
    elif len(hex_color) == 4:  # shorthand #RGBA
        r_fg, g_fg, b_fg, a = [int(hex_color[i]*2, 16) for i in range(4)]
    else:
        raise ValueError("Expected #RRGGBBAA or #RGBA format.")

    r_bg, g_bg, b_bg = [int(bg_color[i:i+2], 16) for i in (0, 2, 4)]

    alpha = a / 255.0
    r_out = round((1 - alpha) * r_bg + alpha * r_fg)
    g_out = round((1 - alpha) * g_bg + alpha * g_fg)
    b_out = round((1 - alpha) * b_bg + alpha * b_fg)

    return f"#{r_out:02X}{g_out:02X}{b_out:02X}"
