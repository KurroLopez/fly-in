import pygame
from pygame.surface import Surface
from map import Map
from entities import Hub
import assets
from pathlib import Path
from pygame import Vector2


class Graph:
    # Define your minimum window size
    MIN_WIDTH = 1408
    MIN_HEIGHT = 768

    INITIAL_WIDTH = 1408
    INITIAL_HEIGHT = 768

    __map: Map | None = None
    __bg: Surface | None = None

    def __init__(self, title: str = "Fly-in",
                 width: int = INITIAL_WIDTH,
                 height: int = INITIAL_HEIGHT,
                 map: Map | None = None):
        """
        Initialize the Graph class.

        :param title: The title of the window.
        :param width: The width of the window.
        :param height: The height of the window.
        :param map: The map to be displayed.
        """
        self.__map = map
        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.Surface((1, 1)))  # Set a blank icon
        self.__init_background()

    def __draw_background(self) -> None:
        if self.__bg is None:
            return

        surface = pygame.display.get_surface()
        if surface is None:
            return

        size = surface.get_size()
        bg_scaled: Surface = pygame.transform.smoothscale(self.__bg, size)
        surface.blit(bg_scaled, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def __init_background(self) -> None:
        assets.load_image(Path("assets"))
        self.__bg = assets.IMG.get("background")
        self.__draw_background()

    def __display_hubs(self, hub: Hub, camera: Vector2) -> None:
        posX: int = hub.properties.posX
        posY: int = hub.properties.posY
        screen: Surface = pygame.display.get_surface()

        vect: Vector2 = Vector2(posX * 128,
                                posY * 128)
        img: Surface = assets.get_square_color(hub.properties.color, 50)
        rect = img.get_rect(center=vect)
        font = assets.FONT
        if font is None:
            return
        nametext = font.render(hub.name, True,
                               (255, 255, 255),
                               (0, 0, 0))
        nametext_rect = nametext.get_rect(center=(800, 1100))
        labeltext = font.render(str(hub.properties.max_drones), True,
                                (255, 255, 255),
                                (0, 0, 0))
        labeltext_rect = labeltext.get_rect(left=posX + 16, top=posY + 19)

        screen.blit(img, rect.move(camera))
        screen.blit(nametext, nametext_rect.move(camera))
        screen.blit(labeltext, labeltext_rect.move(camera), (0, 0, 128, 21))

    def __display_map(self) -> None:
        s_with: int = pygame.display.get_surface().get_width()
        s_height: int = pygame.display.get_surface().get_height()
        camera: Vector2 = Vector2(s_with / 2, s_height / 2)

        if self.__map is None:
            return
        for hub in self.__map.hubs.keys():
            self.__display_hubs(self.__map.hubs[hub], camera)

    def run(self) -> None:
        """
        Run the main loop of the graph.
        """
        running: bool = True
        clock = pygame.time.Clock()
        self.__display_map()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    if width < self.MIN_WIDTH:
                        width = self.MIN_WIDTH
                        pygame.display.set_mode((width, height),
                                                pygame.RESIZABLE)
                    if height < self.MIN_HEIGHT:
                        height = self.MIN_HEIGHT
                        pygame.display.set_mode((width, height),
                                                pygame.RESIZABLE)
                    self.__draw_background()
        pygame.quit()
