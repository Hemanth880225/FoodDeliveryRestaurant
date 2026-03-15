import re

# Menu HTML
with open('jinja_ext_menu.txt', 'r', encoding='utf-8') as f:
    menu_ext = f.read()

with open('foodMenuWebsite/templates/menu.html', 'r', encoding='utf-8') as f:
    menu_html = f.read()

# find the single {% endif %} that matches the huge block.
# Since there are multiple endifs, we look for the one right before `<img src="{{ image_url }}"`
menu_html_patched = menu_html.replace(
    "{% endif %}\n\n            <img src=\"{{ image_url }}\"",
    menu_ext + "            {% endif %}\n\n            <img src=\"{{ image_url }}\""
)

with open('foodMenuWebsite/templates/menu.html', 'w', encoding='utf-8') as f:
    f.write(menu_html_patched)

# Cart HTML
with open('jinja_ext_cart.txt', 'r', encoding='utf-8') as f:
    cart_ext = f.read()

with open('foodMenuWebsite/templates/cart.html', 'r', encoding='utf-8') as f:
    cart_html = f.read()

cart_html_patched = cart_html.replace(
    "{% endif %}\n\n                        <img src=\"{{ image_url }}\"",
    cart_ext + "            {% endif %}\n\n                        <img src=\"{{ image_url }}\""
)

with open('foodMenuWebsite/templates/cart.html', 'w', encoding='utf-8') as f:
    f.write(cart_html_patched)

print("Injected successfully.")
