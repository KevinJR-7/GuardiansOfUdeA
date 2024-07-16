import pygame
import os
import cv2
import mediapipe as mp
import random

# Dimensiones largo y ancho la ventana del juego y la ventana de la detección de manos
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Inicialización de Pygame
pygame.init()

# Creación de la ventana del juego
game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("GALAXY PDI")

# Cargar sonido en el juego
pygame.mixer.init()
background_sound_path = os.path.join("cancion_distrit.wav")
background_sound = pygame.mixer.Sound(background_sound_path)
background_sound.set_volume(0.3)

# Reproducir el sonido en bucle
background_sound.play(loops=-1)



# Inicialización de Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

#Creamos la funcion del menu inicio
def menu_inicio():
    #Cargamos la imagen del cursor
    cursor_image_path = os.path.join("cursor.png")
    cursor_img = pygame.image.load(cursor_image_path)
    #Escalamos el tamaño del cursor
    cursor_img = pygame.transform.scale(cursor_img, (50, 70))
    # Abstraemos el largo y ancho del cursor para crear un rectangulo
    cursor_width, cursor_height = cursor_img.get_rect().size
    # Cargamos una posicion inicial para el cursor
    cursor_x = WINDOW_WIDTH // 2 - cursor_width // 2
    cursor_y = WINDOW_HEIGHT // 2 - cursor_height // 2
    # Cargar la imagen de fondo para el menú de inicio
    menu_background_img = pygame.image.load("menu_background.jpg")
    menu_background_img = pygame.transform.scale(menu_background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Definir las fuentes para el texto
    font = pygame.font.SysFont(None, 50)

    # Variable para almacenar la opción seleccionada
    selected_option = None
    # Capturamos lo que nos muestre el vídeo
    capture = cv2.VideoCapture(0)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"  # Si el usuario cierra la ventana, salimos del juego
        #capturamos frame a frame en la variable image
        ret, image = capture.read()
        # Invertimos la imagen para dar el efecto de espejo
        image = cv2.flip(image, 1)
        if not ret:
            continue
        #Pasamos a un formato que trabaje mediapipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #La variable results almacenará los resultados obtenidos del procesamiento de la imagen
        results = hands.process(image_rgb)

        #Creamos el rectangulo del boton star
        start_button_rect = pygame.Rect(300, 500, 200, 50)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #nos devuelve la altura y el ancho de la imagen capturada
                image_height, image_width, _ = image.shape

                # Dibujar círculos para todos los landmarks en rojo
                for landmark in hand_landmarks.landmark:
                    x = int(landmark.x * image_width)
                    y = int(landmark.y * image_height)
                    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

                # Obtener las coordenadas del índice (landmark número 8)
                index_x = int(hand_landmarks.landmark[8].x * image_width)
                index_y = int(hand_landmarks.landmark[8].y * image_height)

                # Dibujar un círculo naranja en la posición del índice
                cv2.circle(image, (index_x, index_y), 10, (0, 255, 0), -1)

                # Mostrar las coordenadas del índice en la ventana de detección de manos
                cv2.putText(image, f"Coordenadas del índice: ({index_x}, {index_y})", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Mapear las coordenadas del índice al movimiento del cursor
                cursor_x = int((index_x / image_width) * WINDOW_WIDTH)
                cursor_y = int((index_y / image_height) * WINDOW_HEIGHT)
                #Ubicamos las coordenadas de start para calcular la colision
                start_area_x = 300
                start_area_y = 500
                start_area_width = 200
                start_area_height = 50
                # si colisiona el juego inicia
                if (start_area_x <= cursor_x <= start_area_x + start_area_width and
                        start_area_y <= cursor_y <= start_area_y + start_area_height):
                    selected_option = "start"
                    break



        # Mostramos el seguimiento de manos
        cv2.imshow("Seguimientos de manos para cursor", image)


        # Actualizar la pantalla del juego
        pygame.display.update()


        # Dibujar la pantalla del menú de inicio con el fondo y los botones
        game_screen.blit(menu_background_img, (0, 0))

        # Dibujar el texto de los botones
        start_img = pygame.image.load("start.png")
        start_img = pygame.transform.scale(start_img, (200, 50))
        game_screen.blit(start_img, (300, 500))
        game_screen.blit(cursor_img, (cursor_x, cursor_y))
        pygame.display.update()
        #si se activó start se destruyen las ventanas y se retorna start
        if selected_option:
            cv2.destroyAllWindows()
            return selected_option

# Menu seleccion de arma
def select_arm():
    cv2.destroyAllWindows()
    cursor_image_path = os.path.join("cursor.png")
    cursor_img = pygame.image.load(cursor_image_path)
    cursor_img = pygame.transform.scale(cursor_img, (50, 70))
    cursor_width, cursor_height = cursor_img.get_rect().size
    cursor_x = WINDOW_WIDTH // 2 - cursor_width // 2
    cursor_y = WINDOW_HEIGHT // 2 - cursor_height // 2
    # Cargar la imagen de fondo para el menú de inicio
    arm_background_img = pygame.image.load("arm_background.jpg")
    arm_background_img = pygame.transform.scale(arm_background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
    capture = cv2.VideoCapture(0)
    # Cargar imágenes de los diferentes tipos de sables de luz
    sable_luz_img = pygame.image.load("sable_luz.png")
    sable_luz_img = pygame.transform.scale(sable_luz_img, (100, 150))
    sele_img = pygame.image.load("select_arms.png")
    sele_img = pygame.transform.scale(sele_img, (400, 50))

    thanos_img = pygame.image.load("thanos.png")
    thanos_img = pygame.transform.scale(thanos_img, (100, 150))

    godslayer_img = pygame.image.load("godslayer.png")
    godslayer_img = pygame.transform.scale(godslayer_img, (100, 150))

    selected_sable = None  # Variable para almacenar el sable seleccionado

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        ret, image = capture.read()
        image = cv2.flip(image, 1)
        if not ret:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)
        start_button_rect = pygame.Rect(300, 500, 200, 50)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                image_height, image_width, _ = image.shape

                # Dibujar círculos para todos los landmarks en rojo
                for landmark in hand_landmarks.landmark:
                    x = int(landmark.x * image_width)
                    y = int(landmark.y * image_height)
                    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

                # Obtener las coordenadas del índice (landmark número 8)
                index_x = int(hand_landmarks.landmark[8].x * image_width)
                index_y = int(hand_landmarks.landmark[8].y * image_height)

                # Dibujar un círculo naranja en la posición del índice
                cv2.circle(image, (index_x, index_y), 10, (0, 255, 0), -1)

                # Mostrar las coordenadas del índice en la ventana de detección de manos
                cv2.putText(image, f"Coordenadas del indice: ({index_x}, {index_y})", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Mapear las coordenadas del índice al movimiento del cursor
                cursor_x = int((index_x / image_width) * WINDOW_WIDTH)
                cursor_y = int((index_y / image_height) * WINDOW_HEIGHT)

                #Se verifica cada una de las colisiones para las diferentes armas
                if (150 <= cursor_x <= 250 and
                        300 <= cursor_y <= 400):
                    selected_sable = "Sable de luz"
                    break
                elif (350 <= cursor_x <= 450 and
                      300 <= cursor_y <= 400):
                    selected_sable = "Guante del infinito"
                    break
                elif (550 <= cursor_x <= 650 and
                      300 <= cursor_y <= 400):
                    selected_sable = "God Slayer"
                    break
        #Mostramos de nuevo el indice para tener una idea
        cv2.imshow("Seguimientos de manos para cursor", image)



        # Dibujar la pantalla del menú de inicio con el fondo
        game_screen.blit(arm_background_img, (0, 0))
        game_screen.blit(sable_luz_img, (150, 300))
        game_screen.blit(thanos_img, (350, 300))
        game_screen.blit(godslayer_img, (550, 300))
        game_screen.blit(sele_img, (200, 100))
        game_screen.blit(cursor_img, (cursor_x, cursor_y))
        pygame.display.update()
        #al elegir un sable se retorna el resultado y se destruyen las ventanas
        if selected_sable:
            cv2.destroyAllWindows()
            return selected_sable


# Menu Inicio
# Llamar a la función menu_inicio para que el jugador seleccione una opción
selected_option = menu_inicio()

#inicia el juego al dar start
if selected_option == "start":
    # Iniciar el juego
    sable_seleccionado = select_arm()
    # llama al menu para seleccionar arma
    # Cargar la imagen del arma selecionada
    if sable_seleccionado == "Sable de luz":
        sable_image_path = os.path.join("sable_luz.png")
    elif sable_seleccionado == "Guante del infinito":
        sable_image_path = os.path.join("thanos.png")
    else:
        sable_image_path = os.path.join("godslayer.png")

# Carga imagen arma
sable_img = pygame.image.load(sable_image_path)
sable_img = pygame.transform.scale(sable_img, (100, 150))  # Ajustar el tamaño del arma

# Cargar las imágenes de la explosión
explosion_images = [pygame.image.load("destroy_0.png"), pygame.image.load("destroy_1.png"),
                    pygame.image.load("destroy_2.png"), pygame.image.load("destroy_3.png"),
                    pygame.image.load("destroy_4.png"), pygame.image.load("destroy_5.png"),
                    pygame.image.load("destroy_6.png"), pygame.image.load("destroy_7.png"),
                    pygame.image.load("destroy_8.png")]  # Ajusta la lista según tus imágenes

# Obtener las dimensiones del sable
sable_width, sable_height = sable_img.get_rect().size

# Posición inicial del sable
sable_x = WINDOW_WIDTH // 2 - sable_width // 2
sable_y = WINDOW_HEIGHT // 2 - sable_height // 2

# Variables para el puntaje y las vidas
score = 0
lives = 3
clock = pygame.time.Clock()
nivel = 1


# Definición de la clase Block
class Block(pygame.sprite.Sprite):
    def __init__(self):
        #Creamos el meteoro y le damos velocidades aleatorias
        super().__init__()
        self.image = meteoro_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = random.randint(2, 5)

    def update(self):
        #Se va actualizando frame a frame la  posicion del meteoro
        self.rect.y += self.speed
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
            self.speed = random.randint(2, 5)
            global lives
            lives -= 1
            #si sobrepasa el limite se resta una vida
            print("¡Bloque pasado! Vidas restantes:", lives)


class Explosion(pygame.sprite.Sprite):
    #Creamos la animacion de la destruccion de los bloques
    def __init__(self, x, y):
        super().__init__()
        #cargamos la lista de las imagenes que animan la explosion
        self.images = explosion_images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = 3
        self.counter = 0

    def update(self):
        #Actualizamos el bloque y vamos recorriendo la lista
        self.counter += 1
        if self.counter % self.duration == 0:
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                self.kill()


# Carga la imagen del corazón
corazon_img = pygame.image.load(
    "corazon.png")  # Asegúrate de que el archivo "corazon.png" existe y está en el directorio

# Escala la imagen del corazón al tamaño deseado
CORAZON_WIDTH, CORAZON_HEIGHT = 30, 30
corazon_img = pygame.transform.scale(corazon_img, (CORAZON_WIDTH, CORAZON_HEIGHT))


# Función para dibujar corazones en la pantalla
def dibujar_corazones(screen, num_vidas):
    x = 10
    y = 40
    for _ in range(num_vidas):
        screen.blit(corazon_img, (x, y))
        x += CORAZON_WIDTH + 5  # Espacio entre cada corazón


# Grupo de sprites para los bloques y explosiones
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Bucle principal del juego
running = True
capture = cv2.VideoCapture(0)

while running and lives > -1:
    #Creamos la forma de agregar niveles
    if score == 10:
        nivel += 1
    # Cargar la imagen de fondo del juego
    if nivel == 1:
        background_image_path = os.path.join("space.jpg")
        meteoro_image_path = os.path.join("meteoro.png")
    if nivel == 2:
        background_image_path = os.path.join("xandar.jpg")
        meteoro_image_path = os.path.join("nova.png")

    # cargamos el fondo
    background_img = pygame.image.load(background_image_path)
    background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # cargamos el enemigo
    meteoro_img = pygame.image.load(meteoro_image_path)
    meteoro_img = pygame.transform.scale(meteoro_img, (100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, image = capture.read()
    image = cv2.flip(image, 1)
    if not ret:
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # obtenemos el tamaño de la mano
            image_height, image_width, _ = image.shape

            # Dibujamos los puntos de las manos en rojo
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)
                cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

            # Calculamos el promedio de todas las coordenadas para saber el centro
            # la mano
            total_x = 0
            total_y = 0
            num_landmarks = len(hand_landmarks.landmark)
            for landmark in hand_landmarks.landmark:
                total_x += landmark.x
                total_y += landmark.y

            average_x = total_x / num_landmarks
            average_y = total_y / num_landmarks

            # Dibujar un círculo en la posición del centro de la mano (verde)
            center_x = int(average_x * image_width)
            center_y = int(average_y * image_height)
            cv2.circle(image, (center_x, center_y), 10, (0, 255, 0), -1)

            # Mostrar la coordenada del centro de la mano que mueve el sable en la ventana de detección de manos
            cv2.putText(image, f"Coordenadas del arma: ({center_x}, {center_y})", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mapear las coordenadas del centro de la mano al movimiento del sable
            sable_x = int((center_x / image_width) * WINDOW_WIDTH - sable_width // 2)
            sable_y = int((center_y / image_height) * WINDOW_HEIGHT - sable_height // 2)
    # Crear nuevos bloques aleatorios
    if random.randint(0, 100) < 3:
        block = Block()
        all_sprites.add(block)
        blocks.add(block)
    sable_rect = sable_img.get_rect(topleft=(sable_x, sable_y))

    # Actualizar la posición de los bloques y detectar colisiones con el sable
    for block in blocks:
        block.update()

        # Verificar colisión con el rectángulo del sable de luz
        if block.rect.colliderect(sable_rect):
            score += 1
            print("¡Bloque destruido!")
            # Crear una explosión en el lugar del bloque destruido
            explosion = Explosion(block.rect.centerx, block.rect.centery)
            explosions.add(explosion)

            blocks.remove(block)
            all_sprites.remove(block)

    # Actualizar la posición de las explosiones
    explosions.update()

    # Dibujar el fondo y el sable en la pantalla del juego
    game_screen.blit(background_img, (0, 0))
    game_screen.blit(sable_img, (sable_x, sable_y))

    # Dibujar y actualizar las explosiones
    explosions.draw(game_screen)

    # Dibujar y actualizar los bloques
    for block in blocks:
        game_screen.blit(block.image, block.rect)

    # Dibujar elementos en la pantalla

    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Puntaje: {score}", True, (0, 0, 0))
    game_screen.blit(score_text, (10, 10))
    cv2.imshow("Seguimientos de manos", image)

    # Dibujar los corazones de las vidas
    dibujar_corazones(game_screen, lives)

    # Actualizar la pantalla del juego
    pygame.display.update()

    # Controlar la velocidad del juego
    clock.tick(60)

# Terminar el juego si se quedan sin vidas
if lives == 0:
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    game_screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

# Liberar recursos
capture.release()
cv2.destroyAllWindows()
pygame.quit()