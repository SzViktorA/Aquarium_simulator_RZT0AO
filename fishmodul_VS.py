import pygame, random, math, os

class Fish_VS:
    def __init__(self, image_path, x, y, fish_type="predator"):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (100, 60))
        self.rect = self.image.get_rect(center=(x, y))

        self.x = float(x)
        self.y = float(y)
        self.vx = random.choice([-2, 2])
        self.vy = random.choice([-1, 1])
        self.fish_type = fish_type
        self.flipped = False

    def move(self, screen_width, screen_height, mouse_pos=None):
        if self.fish_type == "prey" and mouse_pos:
            dx = self.x - mouse_pos[0]
            dy = self.y - mouse_pos[1]
            dist = math.hypot(dx, dy)
            if dist < 200:
                if dist != 0:
                    self.vx += (dx / dist) * 0.3
                    self.vy += (dy / dist) * 0.3
        else:
            if random.random() < 0.02:
                self.vx += random.choice([-1, 0, 1]) * 0.3
                self.vy += random.choice([-1, 0, 1]) * 0.3

        speed = math.hypot(self.vx, self.vy)
        if speed > 4:
            self.vx *= 4 / speed
            self.vy *= 4 / speed

        self.x += self.vx
        self.y += self.vy

        half_w = self.rect.width / 2
        half_h = self.rect.height / 2

        if self.x - half_w < 0 or self.x + half_w > screen_width:
            self.vx *= -1
            self.flipped = not self.flipped
        if self.y - half_h < 0 or self.y + half_h > screen_height:
            self.vy *= -1

        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flipped, False)
        screen.blit(img, self.rect)


def check_mouse_proximity_VS(mouse_pos, fish, threshold=40):
    if fish.fish_type == "prey":
        return False
    distance = math.hypot(mouse_pos[0] - fish.rect.centerx, mouse_pos[1] - fish.rect.centery)
    return distance < threshold


def create_random_fish_VS(image_files=None, count=4, screen_size=(800, 600)):
    fishes = []
    if not image_files:
        raise FileNotFoundError("Nincs betölthető hal kép az assets mappában!")

    prey_images = [f for f in image_files if "1" in os.path.basename(f).lower() or "prey" in f.lower()]
    predator_images = [f for f in image_files if "2" in os.path.basename(f).lower() or "predator" in f.lower()]

    if not prey_images:
        prey_images = image_files
    if not predator_images:
        predator_images = image_files

    fishes.append(Fish_VS(random.choice(prey_images), random.randint(50, screen_size[0]-50), random.randint(50, screen_size[1]-50), "prey"))
    fishes.append(Fish_VS(random.choice(predator_images), random.randint(50, screen_size[0]-50), random.randint(50, screen_size[1]-50), "predator"))

    for _ in range(count - 2):
        fish_type = random.choice(["prey", "predator"])
        img = random.choice(prey_images if fish_type == "prey" else predator_images)
        fishes.append(Fish_VS(img, random.randint(50, screen_size[0]-50), random.randint(50, screen_size[1]-50), fish_type))

    return fishes
