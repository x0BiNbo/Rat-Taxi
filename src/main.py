import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import sys as _sys
from src.city import City
from src.player import Player
from src.fare import Fare, FareManager
from src.upgrade import UpgradeManager
from src.subway import Subway
from src.ui import draw_minimap, draw_fare_meter, load_and_render_svg
import random
import time

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Rat Taxi')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    city = City()
    tile_size = 40
    # Find a valid road tile for player spawn
    grid = city.get_grid()
    spawn_pos = None
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile in (0, 1, 2, 5, 6, 7, 8):
                spawn_pos = (x, y)
                break
        if spawn_pos:
            break
    player = Player(city_width=city.width, city_height=city.height, spawn_pos=spawn_pos)
    fare_manager = FareManager(city_width=city.width, city_height=city.height, city_grid=city.get_grid(), max_fares=3)
    selected_fare_idx = 0
    show_fare_menu = False
    cheese = 0
    upgrades = UpgradeManager(cheese)
    show_upgrade_menu = False
    upgrade_options = ['engine', 'tires', 'seats', 'fare']
    selected_upgrade = 0
    # Subway system
    # Place subway stations at the first and last valid road tiles on each edge
    def find_edge_road(grid, width, height, edge):
        if edge == 'top':
            for x in range(width):
                if grid[0][x] in (0, 1, 2, 5, 6, 7, 8):
                    return (x, 0)
        elif edge == 'bottom':
            for x in range(width):
                if grid[height-1][x] in (0, 1, 2, 5, 6, 7, 8):
                    return (x, height-1)
        elif edge == 'left':
            for y in range(height):
                if grid[y][0] in (0, 1, 2, 5, 6, 7, 8):
                    return (0, y)
        elif edge == 'right':
            for y in range(height):
                if grid[y][width-1] in (0, 1, 2, 5, 6, 7, 8):
                    return (width-1, y)
        return None
    subway_stations = [
        find_edge_road(grid, city.width, city.height, 'top'),
        find_edge_road(grid, city.width, city.height, 'bottom'),
        find_edge_road(grid, city.width, city.height, 'left'),
        find_edge_road(grid, city.width, city.height, 'right'),
    ]
    subway_stations = [s for s in subway_stations if s is not None]
    subway = Subway(subway_stations, cooldown=5.0)
    show_subway_menu = False
    selected_station = 0
    # Smooth movement variables
    velocity_x = 0.0
    velocity_y = 0.0
    acceleration = 0.2
    max_speed = 1.0

    # SVG surface cache
    svg_surface_cache = {}
    def get_svg_surface(svg_path, size):
        key = (svg_path, size)
        if key not in svg_surface_cache:
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            load_and_render_svg(svg_path, surf)
            svg_surface_cache[key] = surf.copy()
        return svg_surface_cache[key]

    # Add new prop SVGs and hazard/pickup SVGs
    prop_svgs = [
        'assets/svg/tree.svg',
        'assets/svg/bench.svg',
        'assets/svg/streetlight.svg',
        'assets/svg/trashcan.svg',
        'assets/svg/mailbox.svg',
        'assets/svg/cone.svg',
        'assets/svg/car.svg',
        'assets/svg/fire_hydrant.svg',
    ]
    hazard_svgs = [
        'assets/svg/pothole.svg',
        'assets/svg/puddle.svg',
        'assets/svg/rat_hazard.svg',
    ]
    ground_variants = {
        9: ['assets/svg/grass.svg', 'assets/svg/grass2.svg'],
        10: ['assets/svg/dirt.svg', 'assets/svg/dirt2.svg'],
    }
    # Place props, hazards, and pickups
    prop_layer = [[None for _ in range(city.width)] for _ in range(city.height)]
    hazard_layer = [[None for _ in range(city.width)] for _ in range(city.height)]
    pickup_layer = [[None for _ in range(city.width)] for _ in range(city.height)]
    road_tiles = [(x, y) for y, row in enumerate(grid) for x, tile in enumerate(row) if tile in (0, 1, 2, 5, 6, 7, 8)]
    used_tiles = set()
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == 3 and random.random() < 0.08:
                prop_layer[y][x] = random.choice(prop_svgs)
    # Place hazards and pickups only on road tiles, not overlapping
    random.shuffle(road_tiles)
    for rx, ry in road_tiles:
        if (rx, ry) not in used_tiles and random.random() < 0.03:
            hazard_layer[ry][rx] = random.choice(hazard_svgs)
            used_tiles.add((rx, ry))
    for rx, ry in road_tiles:
        if (rx, ry) not in used_tiles and random.random() < 0.01:
            pickup_layer[ry][rx] = 'assets/svg/cheese_pickup.svg'
            used_tiles.add((rx, ry))

    # Health mechanic
    max_health = 6  # 3 hearts (2 per heart)
    health = max_health
    invincibility_ticks = 0
    invincibility_duration = 10  # frames
    heart_svgs = [
        'assets/svg/heart_full.svg',
        'assets/svg/heart_half.svg',
        'assets/svg/heart_empty.svg',
    ]

    score = 0
    game_over = False
    spent_cheese = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_UP:
                        selected_upgrade = (selected_upgrade - 1) % len(upgrade_options)
                    elif event.key == pygame.K_DOWN:
                        selected_upgrade = (selected_upgrade + 1) % len(upgrade_options)
                    elif event.key == pygame.K_RETURN:
                        # Spend cheese on upgrades before restart if enough cheese
                        if upgrades.cheese >= 5:
                            if upgrades.purchase_upgrade(upgrade_options[selected_upgrade]):
                                setattr(player, f'{upgrade_options[selected_upgrade]}_level', getattr(player, f'{upgrade_options[selected_upgrade]}_level') + 1)
                                cheese = upgrades.cheese
                        else:
                            # If not enough cheese, treat as restart
                            upgrades.cheese += cheese
                            cheese = 0
                            health = max_health
                            score = 0
                            spent_cheese = 0
                            # Reset city, fares, pickups, hazards, player
                            city = City()
                            grid = city.get_grid()
                            player = Player(city_width=city.width, city_height=city.height, spawn_pos=spawn_pos)
                            # Set player upgrade levels from UpgradeManager
                            player.engine_level = upgrades.engine_level
                            player.tires_level = upgrades.tires_level
                            player.seats_level = upgrades.seats_level
                            player.fare_level = upgrades.fare_level
                            fare_manager = FareManager(city_width=city.width, city_height=city.height, city_grid=city.get_grid(), max_fares=3)
                            # Re-generate props, hazards, pickups
                            prop_layer = [[None for _ in range(city.width)] for _ in range(city.height)]
                            hazard_layer = [[None for _ in range(city.width)] for _ in range(city.height)]
                            pickup_layer = [[None for _ in range(city.width)] for _ in range(city.height)]
                            road_tiles = [(x, y) for y, row in enumerate(grid) for x, tile in enumerate(row) if tile in (0, 1, 2, 5, 6, 7, 8)]
                            used_tiles = set()
                            for y, row in enumerate(grid):
                                for x, tile in enumerate(row):
                                    if tile == 3 and random.random() < 0.08:
                                        prop_layer[y][x] = random.choice(prop_svgs)
                            random.shuffle(road_tiles)
                            for rx, ry in road_tiles:
                                if (rx, ry) not in used_tiles and random.random() < 0.03:
                                    hazard_layer[ry][rx] = random.choice(hazard_svgs)
                                    used_tiles.add((rx, ry))
                            for rx, ry in road_tiles:
                                if (rx, ry) not in used_tiles and random.random() < 0.01:
                                    pickup_layer[ry][rx] = 'assets/svg/cheese_pickup.svg'
                                    used_tiles.add((rx, ry))
                            game_over = False
                elif show_upgrade_menu:
                    if event.key == pygame.K_UP:
                        selected_upgrade = (selected_upgrade - 1) % len(upgrade_options)
                    elif event.key == pygame.K_DOWN:
                        selected_upgrade = (selected_upgrade + 1) % len(upgrade_options)
                    elif event.key == pygame.K_RETURN:
                        if upgrades.cheese >= 5:
                            if upgrades.purchase_upgrade(upgrade_options[selected_upgrade]):
                                setattr(player, f'{upgrade_options[selected_upgrade]}_level', getattr(player, f'{upgrade_options[selected_upgrade]}_level') + 1)
                                cheese = upgrades.cheese
                elif not show_upgrade_menu:
                    if not show_subway_menu and event.key == pygame.K_e and subway.at_station(player.get_position()) and subway.can_use():
                        subway.enter(player)
                        show_subway_menu = True
                        selected_station = 0
                    elif show_subway_menu:
                        if event.key == pygame.K_UP:
                            selected_station = (selected_station - 1) % len(subway_stations)
                        elif event.key == pygame.K_DOWN:
                            selected_station = (selected_station + 1) % len(subway_stations)
                        elif event.key == pygame.K_RETURN:
                            dest = subway_stations[selected_station]
                            if dest != player.get_position() and not subway.animating:
                                subway.exit(player, dest)
                                show_subway_menu = False
                                velocity_x = 0.0
                                velocity_y = 0.0
                        elif event.key == pygame.K_ESCAPE:
                            show_subway_menu = False
                    elif show_fare_menu:
                        if event.key == pygame.K_UP:
                            selected_fare_idx = (selected_fare_idx - 1) % len(fare_manager.fares)
                        elif event.key == pygame.K_DOWN:
                            selected_fare_idx = (selected_fare_idx + 1) % len(fare_manager.fares)
                        elif event.key == pygame.K_RETURN:
                            show_fare_menu = False
                        elif event.key == pygame.K_ESCAPE:
                            show_fare_menu = False
                    elif not show_fare_menu:
                        if event.key == pygame.K_TAB:
                            show_fare_menu = True
                            selected_fare_idx = 0

        upgrades.cheese = cheese

        # Trigger roguelike game over if health is depleted
        if health <= 0 and not game_over:
            game_over = True

        if game_over:
            screen.fill((20, 10, 30))
            # Left panel: game over info
            left_x = 60
            y0 = 80
            spacing = 48
            over_text = font.render('GAME OVER', True, (255, 80, 80))
            screen.blit(over_text, (left_x, y0))
            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            screen.blit(score_text, (left_x, y0 + spacing))
            cheese_text = font.render(f'Cheese: {cheese}', True, (255, 255, 200))
            screen.blit(cheese_text, (left_x, y0 + 2 * spacing))
            restart_text = font.render('Enter: Spend cheese on upgrade OR restart', True, (180, 180, 255))
            screen.blit(restart_text, (left_x, y0 + 3 * spacing))
            # Right panel: upgrade menu
            menu_x = 420
            menu_y = 80
            menu_w = 320
            menu_h = 260
            menu_bg = pygame.Surface((menu_w, menu_h))
            menu_bg.set_alpha(220)
            menu_bg.fill((40, 40, 60))
            screen.blit(menu_bg, (menu_x, menu_y))
            title = font.render('Upgrade Menu', True, (255, 255, 255))
            screen.blit(title, (menu_x + menu_w // 2 - title.get_width() // 2, menu_y + 20))
            for i, opt in enumerate(upgrade_options):
                color = (255, 255, 0) if i == selected_upgrade else (200, 200, 200)
                level = getattr(upgrades, f'{opt}_level')
                label = font.render(f'{opt.title()} (Lv {level}) - 5 Cheese', True, color)
                screen.blit(label, (menu_x + 30, menu_y + 70 + i * 40))
            cheese_label = font.render(f'Cheese: {upgrades.cheese}', True, (255, 255, 200))
            screen.blit(cheese_label, (menu_x + menu_w // 2 - cheese_label.get_width() // 2, menu_y + menu_h - 40))
            pygame.display.flip()
            clock.tick(10)
            continue
        if not show_upgrade_menu and not show_subway_menu and not show_fare_menu:
            keys = pygame.key.get_pressed()
            target_vx, target_vy = 0.0, 0.0
            speed = max_speed + player.engine_level * 0.2
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                target_vx = -speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                target_vx = speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                target_vy = -speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                target_vy = speed
            # Smooth acceleration
            velocity_x += (target_vx - velocity_x) * acceleration
            velocity_y += (target_vy - velocity_y) * acceleration
            # Only move if on a driveable tile
            new_fx = player.fx + velocity_x
            new_fy = player.fy + velocity_y
            new_x = int(round(new_fx)) % city.width
            new_y = int(round(new_fy)) % city.height
            if city.is_driveable(new_x, new_y):
                player.move(velocity_x, velocity_y)
                blocked = False
            else:
                velocity_x = 0.0
                velocity_y = 0.0
                blocked = True
                if invincibility_ticks == 0 and health > 0:
                    health -= 1
                    invincibility_ticks = invincibility_duration
            # Check for hazard collision
            pos = player.get_position()
            px, py = pos
            if hazard_layer[py][px] and invincibility_ticks == 0 and health > 0:
                health -= 1
                invincibility_ticks = invincibility_duration
            # Check for health pickup
            if pickup_layer[py][px] and health < max_health:
                health = min(max_health, health + 2)
                pickup_layer[py][px] = None

            pos = player.get_position()
            # Pickup fare
            picked_fare = fare_manager.pick_up_fare(pos)
            # Dropoff fare
            dropped_fare = fare_manager.dropoff_fare(pos)
            if dropped_fare:
                bonus = 1 + player.fare_level + (dropped_fare.bonus if dropped_fare.special else 0)
                cheese += bonus
                score += bonus
                fare_manager.generate_fares()

        if invincibility_ticks > 0:
            invincibility_ticks -= 1

        subway.update_animation()

        screen.fill((30, 30, 30))

        # Draw environment/city streets background
        environment_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        load_and_render_svg('assets/svg/environment.svg', environment_surface)
        screen.blit(environment_surface, (0, 0))

        # Draw city grid (ground tiles first)
        grid = city.get_grid()
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if tile in (9, 10):
                    tile_surface = get_svg_surface(random.choice(ground_variants[tile]), tile_size)
                elif tile == 3:
                    # Contextual sidewalk: use straight/corner/T/end SVGs based on neighbors
                    up = y > 0 and grid[y-1][x] == 3
                    down = y < city.height-1 and grid[y+1][x] == 3
                    left = x > 0 and grid[y][x-1] == 3
                    right = x < city.width-1 and grid[y][x+1] == 3
                    if up and down and left and right:
                        tile_surface = get_svg_surface('assets/svg/sidewalk.svg', tile_size)
                    elif (up and down and (left or right)) or (left and right and (up or down)):
                        tile_surface = get_svg_surface('assets/svg/sidewalk_t.svg', tile_size)
                    elif (up and left) or (down and right):
                        tile_surface = get_svg_surface('assets/svg/sidewalk_corner.svg', tile_size)
                    elif (up or down) and not (left or right):
                        tile_surface = get_svg_surface('assets/svg/sidewalk_straight.svg', tile_size)
                    elif (left or right) and not (up or down):
                        tile_surface = get_svg_surface('assets/svg/sidewalk_straight.svg', tile_size)
                    else:
                        tile_surface = get_svg_surface('assets/svg/sidewalk_end.svg', tile_size)
                elif tile == 0:
                    tile_surface = get_svg_surface('assets/svg/road_vertical.svg', tile_size)
                elif tile == 1:
                    tile_surface = get_svg_surface('assets/svg/road_horizontal.svg', tile_size)
                elif tile == 2:
                    tile_surface = get_svg_surface('assets/svg/road_cross.svg', tile_size)
                elif tile == 4:
                    tile_surface = get_svg_surface('assets/svg/building.svg', tile_size)
                elif tile == 41:
                    tile_surface = get_svg_surface('assets/svg/building1.svg', tile_size)
                elif tile == 42:
                    tile_surface = get_svg_surface('assets/svg/building2.svg', tile_size)
                elif tile == 5:
                    tile_surface = get_svg_surface('assets/svg/road_corner_tl.svg', tile_size)
                elif tile == 6:
                    tile_surface = get_svg_surface('assets/svg/road_corner_tr.svg', tile_size)
                elif tile == 7:
                    tile_surface = get_svg_surface('assets/svg/road_corner_bl.svg', tile_size)
                elif tile == 8:
                    tile_surface = get_svg_surface('assets/svg/road_corner_br.svg', tile_size)
                else:
                    tile_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                screen.blit(tile_surface, rect.topleft)

        # Draw hazards
        for y, row in enumerate(hazard_layer):
            for x, hazard in enumerate(row):
                if hazard:
                    hazard_icon = get_svg_surface(hazard, tile_size)
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    screen.blit(hazard_icon, rect.topleft)
        # Draw health pickups
        for y, row in enumerate(pickup_layer):
            for x, pickup in enumerate(row):
                if pickup:
                    pickup_icon = get_svg_surface(pickup, tile_size)
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    screen.blit(pickup_icon, rect.topleft)

        # Draw props
        for y, row in enumerate(prop_layer):
            for x, prop in enumerate(row):
                if prop:
                    prop_icon = get_svg_surface(prop, tile_size)
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    screen.blit(prop_icon, rect.topleft)

        # Draw subway stations
        subway_icon = get_svg_surface('assets/svg/subway.svg', tile_size - 24)
        for sx, sy in subway_stations:
            station_rect = pygame.Rect(sx * tile_size + 12, sy * tile_size + 12, tile_size - 24, tile_size - 24)
            screen.blit(subway_icon, station_rect.topleft)

        # Draw fare pickup and dropoff
        for fare in fare_manager.fares:
            if not fare.picked_up:
                fx, fy = fare.pickup
                pickup_rect = pygame.Rect(fx * tile_size + 8, fy * tile_size + 8, tile_size - 16, tile_size - 16)
                pickup_surface = pygame.Surface((pickup_rect.width, pickup_rect.height), pygame.SRCALPHA)
                load_and_render_svg('assets/svg/fare_pickup.svg', pickup_surface)
                screen.blit(pickup_surface, pickup_rect.topleft)
                pickup_pos = fare.pickup
                dropoff_pos = None
            elif fare.picked_up:
                fx, fy = fare.dropoff
                dropoff_rect = pygame.Rect(fx * tile_size + 8, fy * tile_size + 8, tile_size - 16, tile_size - 16)
                dropoff_surface = pygame.Surface((dropoff_rect.width, dropoff_rect.height), pygame.SRCALPHA)
                load_and_render_svg('assets/svg/fare_dropoff.svg', dropoff_surface)
                screen.blit(dropoff_surface, dropoff_rect.topleft)
                pickup_pos = None
                dropoff_pos = fare.dropoff

        # Draw player
        player_icon = get_svg_surface('assets/svg/player.svg', tile_size - 8)
        px, py = player.get_float_position()
        player_rect = pygame.Rect(int(px * tile_size) + 4, int(py * tile_size) + 4, tile_size - 8, tile_size - 8)
        player_surface = player_icon.copy()
        if 'blocked' in locals() and blocked:
            player_surface.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(player_surface, player_rect.topleft)

        # Draw Mini-Map (bottom right, semi-transparent)
        minimap_surface = pygame.Surface((160, 120), pygame.SRCALPHA)
        minimap_surface.set_alpha(180)
        draw_minimap(
            minimap_surface,
            player.get_position(),
            (city.width, city.height),
            subway_stations,
            pickup_pos,
            dropoff_pos
        )
        screen.blit(minimap_surface, (screen.get_width() - 170, screen.get_height() - 130))

        # Draw cheese currency (top left)
        cheese_text = font.render(f'Cheese: {cheese}', True, (255, 255, 200))
        screen.blit(cheese_text, (10, 10))

        # Draw Fare Meter (top right, semi-transparent)
        active_fares = [f for f in fare_manager.fares if not f.picked_up or not f.at_dropoff(f.dropoff)]
        fare_active = any(f.picked_up for f in active_fares)
        fare_bonus = 1 + player.fare_level + (active_fares[0].bonus if active_fares and active_fares[0].special else 0)
        fare_meter_surface = pygame.Surface((220, 50), pygame.SRCALPHA)
        fare_meter_surface.set_alpha(180)
        draw_fare_meter(fare_meter_surface, font, fare_active, fare_bonus, cheese)
        screen.blit(fare_meter_surface, (screen.get_width() - 230, 10))

        # Draw upgrade menu
        if show_upgrade_menu:
            menu_bg = pygame.Surface((320, 240))
            menu_bg.set_alpha(220)
            menu_bg.fill((40, 40, 60))
            screen.blit(menu_bg, (240, 120))
            title = font.render('Upgrade Menu', True, (255, 255, 255))
            screen.blit(title, (320, 140))
            for i, opt in enumerate(upgrade_options):
                color = (255, 255, 0) if i == selected_upgrade else (200, 200, 200)
                level = getattr(upgrades, f'{opt}_level')
                label = font.render(f'{opt.title()} (Lv {level}) - 5 Cheese', True, color)
                screen.blit(label, (260, 180 + i * 40))
            cheese_label = font.render(f'Cheese: {upgrades.cheese}', True, (255, 255, 200))
            screen.blit(cheese_label, (320, 340))

        # Draw subway animation overlay if animating
        if subway.animating:
            anim_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            anim_surface.fill((30, 30, 60, 180))
            anim_text = font.render('Traveling by Subway...', True, (255, 255, 255))
            anim_rect = anim_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            anim_surface.blit(anim_text, anim_rect)
            screen.blit(anim_surface, (0, 0))

        # Draw subway menu
        if show_subway_menu:
            menu_bg = pygame.Surface((320, 240))
            menu_bg.set_alpha(220)
            menu_bg.fill((60, 60, 100))
            screen.blit(menu_bg, (240, 120))
            title = font.render('Subway Stations', True, (255, 255, 255))
            screen.blit(title, (320, 140))
            for i, st in enumerate(subway_stations):
                color = (255, 255, 0) if i == selected_station else (200, 200, 200)
                label = font.render(f'Station {i+1}: {st}', True, color)
                screen.blit(label, (260, 180 + i * 40))
            cooldown_left = max(0, int(subway.cooldown - (time.time() - subway.last_used)))
            cooldown_text = font.render(f'Cooldown: {cooldown_left}s', True, (180, 180, 255))
            screen.blit(cooldown_text, (320, 320))
            info = font.render('Enter to travel, Esc to cancel', True, (180, 180, 255))
            screen.blit(info, (250, 340))

        # Draw health (hearts) at top left below cheese
        heart_x = 10
        heart_y = 40
        hearts = health // 2
        half = health % 2
        hearts_per_row = 10
        heart_rows = (max_health // 2 + hearts_per_row - 1) // hearts_per_row
        for i in range(max_health // 2):
            row = i // hearts_per_row
            col = i % hearts_per_row
            x = heart_x + col * 32
            y = heart_y + row * 32
            if i < hearts:
                heart_icon = get_svg_surface(heart_svgs[0], 28)
            elif i == hearts and half:
                heart_icon = get_svg_surface(heart_svgs[1], 28)
            else:
                heart_icon = get_svg_surface(heart_svgs[2], 28)
            screen.blit(heart_icon, (x, y))
        # Draw score below the last row of hearts
        score_text = font.render(f'Score: {score}', True, (200, 255, 255))
        score_y = heart_y + heart_rows * 32 + 4
        screen.blit(score_text, (10, score_y))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 