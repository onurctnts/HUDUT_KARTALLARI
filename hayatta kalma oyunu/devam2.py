import pygame
import sys
import random


lives = 3
game_over = False


hearts = []
heart_spawn_delay = 500  # yaklaşık 8 saniyede bir
heart_timer = 0


fastfires = []
fastfire_timer = 0
fastfire_spawn_delay = 700  # 10 saniyede bir düşebilir
fastfire_active = False
fastfire_duration = 300  # 5 saniye boyunca hızlı ateş
fastfire_counter = 0


shields = []
shield_timer = 0
shield_spawn_delay = 1000  # yaklaşık 15–20 saniyede bir
shield_active = False


def show_menu():
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 20))  # koyu mavi arka plan
        title = font.render("HUDUT KARTALLARI", True, (255, 255, 255))
        start = font.render("BAŞLAMAK İÇİN [SPACE]", True, (0, 255, 0))
        quit_text = font.render("ÇIKMAK İÇİN [ESC]", True, (255, 0, 0))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 250))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()



# Pygame başlat
pygame.init()

shoot_sound = pygame.mixer.Sound(r"C:\Users\Onur\OneDrive\Desktop\grafikler\086553_bullet-hit-39853.wav")
explosion_sound = pygame.mixer.Sound(r"C:\Users\Onur\OneDrive\Desktop\grafikler\large-underwater-explosion-190270.wav")



# Ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hudut Kartalları")
clock = pygame.time.Clock()
FPS = 60

# Görseller (Görselleri uygun boyuta scale ediyoruz)
player_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\BAYRAKTARSON.png")
player_img = pygame.transform.scale(player_img, (50, 50))  # Oyuncu uzay gemisi

bullet_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\0a777a72-26e4-46d3-87d2-070eb48744c03.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))  # Mermi

enemy_img = pygame.image.load(r"C:\Users\Onur\Downloads\mq9_reaper_rotated.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))  # Düşman gemisi

# Yeni düşman görselleri
enemy_img_1 = pygame.image.load(r"C:\Users\Onur\Downloads\enemy_realistic_1.png")
enemy_img_1 = pygame.transform.scale(enemy_img_1, (60, 60))

enemy_img_2 = pygame.image.load(r"C:\Users\Onur\Downloads\enemy_realistic_2.png")
enemy_img_2 = pygame.transform.scale(enemy_img_2, (60, 60))

enemy_img_3 = pygame.image.load(r"C:\Users\Onur\Downloads\enemy_realistic_3.png")
enemy_img_3 = pygame.transform.scale(enemy_img_3, (60, 60))

enemy_images = [enemy_img,enemy_img_1, enemy_img_2, enemy_img_3]

enemy_bullet_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\0a777a72-26e4-46d3-87d2-070eb48744c03.png")  # Kendine bir görsel seçebilirsin
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (10, 20))  # Boyutunu ayarla

enemy_bullets = []


background_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\background1.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

heart_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\heartson.png")
heart_img = pygame.transform.scale(heart_img, (30, 30))

fastfire_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\fastfireson.png")
fastfire_img = pygame.transform.scale(fastfire_img, (30, 30))

shield_img = pygame.image.load(r"C:\Users\Onur\OneDrive\Desktop\grafikler\shieldson.png")
shield_img = pygame.transform.scale(shield_img, (30, 30))



# Oyuncu
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 20
player_speed = 5

# Mermi
bullets = []
bullet_speed = 7

# Düşman
enemies = []  # Her biri sözlük olacak: {"image": ..., "rect": ...}
enemy_speed = 3
enemy_spawn_delay = 30  # Her kaç framede bir düşman gelsin
enemy_timer = 0

# Skor
score = 0
font = pygame.font.SysFont(None, 36)
high_score = 0

# Oyunun başında high_score.txt dosyasından oku
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0


# Ana oyun döngüsü

show_menu()
running = True
while running:
    clock.tick(FPS)
    enemy_timer += 1


    fastfire_timer += 1
    if fastfire_timer >= fastfire_spawn_delay:
        ff_rect = fastfire_img.get_rect()
        ff_rect.x = random.randint(0, WIDTH - ff_rect.width)
        ff_rect.y = -ff_rect.height
        fastfires.append(ff_rect)
        fastfire_timer = 0


    heart_timer += 1
    if heart_timer >= heart_spawn_delay:
                    if fastfire_active:
                        fastfire_counter += 1
                        if fastfire_counter >= fastfire_duration:
                            fastfire_active = False

                    heart_rect = heart_img.get_rect()
                    heart_rect.x = random.randint(0, WIDTH - heart_rect.width)
                    heart_rect.y = -heart_rect.height
                    hearts.append(heart_rect)
                    heart_timer = 0  
    shield_timer += 1
    if shield_timer >= shield_spawn_delay:
        shield_rect = shield_img.get_rect()
        shield_rect.x = random.randint(0, WIDTH - shield_rect.width)
        shield_rect.y = -shield_rect.height
        shields.append(shield_rect)
        shield_timer = 0
                 
               

    for heart in hearts[:]:
        heart.y += 2  # yavaş yavaş iner
        if heart.top > HEIGHT:
            hearts.remove(heart)

    for shield in shields[:]:
        shield.y += 2
        if shield.top > HEIGHT:
            shields.remove(shield)
        elif shield.colliderect(player_rect):
            shields.remove(shield)
            shield_active = True
        

    for ff in fastfires[:]:
        ff.y += 2
        if ff.top > HEIGHT:
            fastfires.remove(ff)
        elif ff.colliderect(player_rect):
            fastfires.remove(ff)
            fastfire_active = True
            fastfire_counter = 0
       


    for heart in hearts[:]:
        if heart.colliderect(player_rect):
            hearts.remove(heart)
            if lives < 5:  # maksimum 5 can olsun
                lives += 1
       


    # --- Olaylar ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = bullet_img.get_rect()
                bullet_rect.centerx = player_rect.centerx
                bullet_rect.bottom = player_rect.top

                # SHIFT basılıysa mermi hızı yüksek olsun
                bullet = {
                    "rect": bullet_rect,
                    "speed": bullet_speed * 3 if fastfire_active else bullet_speed * 2 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else bullet_speed
                }
                bullets.append(bullet)
                shoot_sound.play()

               


    # --- Tuşlar ---
    keys = pygame.key.get_pressed()
    speed = player_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        speed *= 2  # Shift basılıysa hız 2 katı olsun

    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += speed



    # --- Mermi güncelle ---

    for bullet in bullets[:]:
        bullet["rect"].y -= bullet["speed"]
        if bullet["rect"].bottom < 0:
            bullets.remove(bullet)

    # --- Düşman mermilerini güncelle ---
    for bullet in enemy_bullets[:]:
        bullet.y += 5  # düşman mermisinin hızı
        if bullet.top > HEIGHT:
            enemy_bullets.remove(bullet)
        

    # --- Düşman oluştur ---
    if enemy_timer >= enemy_spawn_delay:
        chosen_img = random.choice(enemy_images)  # 3 yeni düşman görselinden biri
        enemy_rect = chosen_img.get_rect()
        enemy_rect.x = random.randint(0, WIDTH - enemy_rect.width)
        enemy_rect.y = -enemy_rect.height

        enemy = {
            "image": chosen_img,
            "rect": enemy_rect,
            "x_speed": random.choice([-2, -1, 0, 1, 2])  # sağ-sol hareket hızı
        }
        enemies.append(enemy)
        enemy_timer = 0



    # --- Düşman güncelle ---
    for enemy in enemies[:]:
        enemy["rect"].y += enemy_speed
        enemy["rect"].x += enemy["x_speed"]  # sağa-sola kayma eklendi

        # --- Düşman mermisi ateşlemesi ---
        if random.randint(0, 100) < 2:  # %2 ihtimalle her frame mermi atabilir (istersen ayarlarız)
            enemy_bullet_rect = enemy_bullet_img.get_rect()
            enemy_bullet_rect.centerx = enemy["rect"].centerx
            enemy_bullet_rect.top = enemy["rect"].bottom
            enemy_bullets.append(enemy_bullet_rect)


        # Ekrandan çıkıyorsa yönü tersine çevir
        if enemy["rect"].left < 0 or enemy["rect"].right > WIDTH:
            enemy["x_speed"] *= -1

        if enemy["rect"].top > HEIGHT:
            enemies.remove(enemy)


        # --- Oyuncuya çarpma kontrolü ---
    for enemy in enemies[:]:
        if enemy["rect"].colliderect(player_rect):
            enemies.remove(enemy)

            if shield_active:
                shield_active = False 
            else:
                lives -= 1
                if lives <= 0:
                    game_over = True

        

    # --- Çarpışma kontrolü ---
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet["rect"].colliderect(enemy["rect"]): 
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                explosion_sound.play()
                break  # Bu break, aynı merminin birden fazla düşmanı vurmasını engeller

    for bullet in enemy_bullets[:]:
        if bullet.colliderect(player_rect):
            enemy_bullets.remove(bullet)
            if shield_active:
                shield_active = False  # Kalkan varsa korur
            else:
                lives -= 1
                if lives <= 0:
                    game_over = True
        


       # --- Ekranı çiz ---
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, player_rect)

    for bullet in bullets:
         screen.blit(bullet_img, bullet["rect"])


    for enemy in enemies:
        screen.blit(enemy["image"], enemy["rect"])


    for heart in hearts:
        screen.blit(heart_img, heart)

    for shield in shields:
        screen.blit(shield_img, shield)

    # --- Düşman mermilerini çiz ---
    for bullet in enemy_bullets:
        screen.blit(enemy_bullet_img, bullet)
    

    

    score_text = font.render(f"Skor: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"En Yüksek Skor: {high_score}", True, (255, 255, 0))



    # Skoru sol üst köşeye koy
    screen.blit(score_text, (10, 10))

    for heart in hearts:
     screen.blit(heart_img, heart)

    for ff in fastfires:
     screen.blit(fastfire_img, ff)

    # Can yazısı (sağ üst köşe)
    lives_text = font.render(f"Can: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (WIDTH - 120, 10))
 


    # En yüksek skoru biraz sağa koy (örnek: x=250)
    screen.blit(high_score_text, (250, 10))



    # Can yazısı
    lives_text = font.render(f"Can: {lives}", True, (255, 255, 255))
    if shield_active:
        shield_text = font.render("KALKAN AKTİF", True, (0, 200, 255))
        screen.blit(shield_text, (WIDTH - 180, 40))


    # Game Over ekranı
    if game_over:
        over_text = font.render("GAME OVER - Yeniden başlamak için SPACE'e bas", True, (255, 50, 50))
        screen.blit(over_text, (WIDTH // 2 - 300, HEIGHT // 2))
        pygame.display.flip()

        # Yeni skor rekoru kırdıysa kaydet
      
        if score > high_score:
            high_score = score
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))



        # Yeniden başlat bekle
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shoot_sound.play()  # 🔊 Mermi sesi

                        # Her şeyi sıfırla
                        bullets.clear()
                        enemies.clear()
                        score = 0
                        lives = 3
                        game_over = False
                        player_rect.centerx = WIDTH // 2
                        player_rect.bottom = HEIGHT - 20
                        waiting = False

    pygame.display.flip()
