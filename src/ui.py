import pygame
import cairosvg

def draw_minimap(surface, player_pos, city_size, stations, pickup, dropoff):
    surface.fill((0, 0, 0))
    w, h = surface.get_size()
    city_w, city_h = city_size
    scale_x = w / city_w
    scale_y = h / city_h
    # Draw subway stations
    for sx, sy in stations:
        x = int(sx * scale_x)
        y = int(sy * scale_y)
        pygame.draw.circle(surface, (100, 100, 255), (x, y), 5)
    # Draw fare pickup
    if pickup:
        x = int(pickup[0] * scale_x)
        y = int(pickup[1] * scale_y)
        pygame.draw.circle(surface, (40, 220, 40), (x, y), 5)
    # Draw fare dropoff
    if dropoff:
        x = int(dropoff[0] * scale_x)
        y = int(dropoff[1] * scale_y)
        pygame.draw.circle(surface, (220, 40, 40), (x, y), 5)
    # Draw player
    px, py = player_pos
    x = int(px * scale_x)
    y = int(py * scale_y)
    pygame.draw.circle(surface, (255, 220, 40), (x, y), 6)

def draw_fare_meter(surface, font, fare_active, fare_bonus, cheese):
    surface.fill((20, 30, 30))
    status = 'Active' if fare_active else 'Inactive'
    color = (40, 220, 40) if fare_active else (220, 40, 40)
    text = font.render(f'Fare: {status}', True, color)
    surface.blit(text, (10, 5))
    bonus_text = font.render(f'Bonus: x{fare_bonus}', True, (200, 255, 255))
    surface.blit(bonus_text, (10, 30))
    cheese_text = font.render(f'Cheese: {cheese}', True, (255, 255, 200))
    surface.blit(cheese_text, (10, 55))

def draw_upgrade_menu(surface, font, upgrades, selected, cheese):
    surface.fill((40, 40, 60))
    title = font.render('Upgrade Menu', True, (255, 255, 255))
    surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 20))
    upgrade_options = ['engine', 'tires', 'seats', 'fare']
    descriptions = {
        'engine': 'Increases taxi speed.',
        'tires': 'Improves turning.',
        'seats': 'Carry more customers.',
        'fare': 'Earn more cheese per fare.'
    }
    icon_colors = {
        'engine': (255, 80, 80),
        'tires': (80, 255, 80),
        'seats': (80, 80, 255),
        'fare': (255, 220, 40)
    }
    for i, opt in enumerate(upgrade_options):
        color = (255, 255, 0) if i == selected else (200, 200, 200)
        level = upgrades.get(opt, 0)
        # Draw icon (colored rectangle)
        icon_rect = pygame.Rect(10, 70 + i * 40, 16, 16)
        pygame.draw.rect(surface, icon_colors[opt], icon_rect)
        label = font.render(f'{opt.title()} (Lv {level}) - 5 Cheese', True, color)
        surface.blit(label, (30, 70 + i * 40))
    cheese_label = font.render(f'Cheese: {cheese}', True, (255, 255, 200))
    surface.blit(cheese_label, (surface.get_width() // 2 - cheese_label.get_width() // 2, 230))
    # Render description/tooltip for selected upgrade
    selected_opt = upgrade_options[selected]
    desc_text = descriptions[selected_opt]
    desc_label = font.render(desc_text, True, (180, 220, 255))
    surface.blit(desc_label, (30, 230))

def load_and_render_svg(svg_path, surface):
    # Try to load SVG and render to surface using cairosvg and pygame
    import io
    try:
        with open(svg_path, 'rb') as f:
            svg_data = f.read()
        png_bytes = cairosvg.svg2png(bytestring=svg_data, output_width=surface.get_width(), output_height=surface.get_height())
        png_image = pygame.image.load(io.BytesIO(png_bytes), 'png')
        surface.blit(png_image, (0, 0))
    except Exception:
        # Fallback: draw a magenta rectangle with an X
        surface.fill((200, 0, 200))
        pygame.draw.line(surface, (255, 255, 255), (0, 0), (surface.get_width(), surface.get_height()), 3)
        pygame.draw.line(surface, (255, 255, 255), (surface.get_width(), 0), (0, surface.get_height()), 3)

def handle_upgrade_menu_mouse(mouse_pos, mouse_click, upgrade_options, base_y=70, option_height=40, icon_height=16):
    """
    Returns the index of the upgrade option under the mouse, or None if none.
    If mouse_click is True, returns the index to select.
    """
    x, y = mouse_pos
    for i in range(len(upgrade_options)):
        rect = pygame.Rect(10, base_y + i * option_height, 300, icon_height)
        if rect.collidepoint(x, y):
            if mouse_click:
                return i
    return None 