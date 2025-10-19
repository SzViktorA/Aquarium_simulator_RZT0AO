import os
import sys
import random
import pygame

from fishmodul_VS import (
    Fish_VS,
    check_mouse_proximity_VS,
    create_random_fish_VS,
)
from bubblemodul_VS import Bubble_VS

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_background_VS(path=None, size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
    if path and os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.smoothscale(img, size)
            return img
        except Exception as e:
            print(f"load_background_VS: Hiba a háttér betöltésekor: {e}")

    surf = pygame.Surface(size)
    surf.fill((10, 35, 80))
    return surf

def create_fish_list_VS(num=3):
    image_files = []
    if os.path.isdir(ASSETS_DIR):
        for name in os.listdir(ASSETS_DIR):
            if name.lower().endswith((".png", ".jpg", ".jpeg")) and "fish" in name.lower():
                image_files.append(os.path.join(ASSETS_DIR, name))

    return create_random_fish_VS(
        image_files if image_files else None,
        count=num,
        screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
    )

def try_load_cursor_image():
    candidates = ["finger_img.png"]
    for name in candidates:
        p = os.path.join(ASSETS_DIR, name)
        if os.path.isfile(p):
            try:
                img = pygame.image.load(p).convert_alpha()
                return img
            except Exception as e:
                print(f"Cursor betöltési hiba ({p}): {e}")
    return None

def run_app():
    pygame.init()

    try:
        pygame.mixer.init()
    except Exception:
        print("pygame.mixer nem inicializálható — hangok nem lesznek elérhetőek")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Akvárium Szimulátor VS")

    finger_img = None
    finger_img_raw = try_load_cursor_image()
    if finger_img_raw:
        try:
            finger_img = pygame.transform.smoothscale(finger_img_raw, (50, 50))
            pygame.mouse.set_visible(False)
            print("Egyéni kurzor betöltve.")
        except Exception as e:
            print("Kurzorkép betöltési/méretezési hiba:", e)
            finger_img = None
            pygame.mouse.set_visible(True)
    else:
        print("Nincs kurzorkép az assets-ben. A rendszerkurzor marad.")
        pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    bg = load_background_VS(os.path.join(ASSETS_DIR, "background.jpg"))

    fish_list = create_fish_list_VS(4)

    chomp_sound = None
    chomp_path = os.path.join(ASSETS_DIR, "chomp.mp3")
    if os.path.isfile(chomp_path):
        try:
            chomp_sound = pygame.mixer.Sound(chomp_path)
        except Exception as e:
            print(f"Nem sikerült hangot betölteni: {e}")

    running = True
    game_over = False

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 26)

    bubbles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                fish_list = create_fish_list_VS(4)
                bubbles.clear()
                game_over = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if not game_over:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(bg, (0, 0))

            for fish in fish_list:
                fish.move(SCREEN_WIDTH, SCREEN_HEIGHT, mouse_pos)
                spawn_chance = 0.01 if fish.fish_type == "predator" else 0.03
                if random.random() < spawn_chance:
                    bx = fish.x + random.uniform(-fish.rect.width/3, fish.rect.width/3)
                    by = fish.y + fish.rect.height/2 + random.uniform(2, 8)
                    bubbles.append(Bubble_VS(bx, by))

            for b in bubbles[:]:
                b.update()
                b.draw(screen)
                if b.is_dead(SCREEN_HEIGHT):
                    bubbles.remove(b)

            for fish in fish_list:
                fish.draw(screen)
                if fish.fish_type == "predator" and check_mouse_proximity_VS(mouse_pos, fish):
                    game_over = True
                    if chomp_sound:
                        try:
                            chomp_sound.play()
                        except Exception:
                            pass
                    break

            instr = small_font.render(
                "Mozgasd az egeret — ha túl közel viszed, a piranha meg fog enni. (R újrakezdés, ESC kilépés)",
                True, (255, 255, 255)
            )
            screen.blit(instr, (10, 10))

        else:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            text = font.render("A hal megevett!", True, (255, 255, 255))
            restart = small_font.render("Nyomj R-t az újraindításhoz. ESC kilépéshez.", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        if finger_img:
            finger_pos = pygame.mouse.get_pos()
            finger_rect = finger_img.get_rect(center=finger_pos)
            screen.blit(finger_img, finger_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
