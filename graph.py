import pygame
from pygame.surface import Surface
from map import Map
import assets
from pathlib import Path


class Graph:
    __map: Map | None = None
    __bg: Surface | None = None

    def __init__(self, title: str = "Fly-in",
                 width: int = 800, height: int = 600,
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

    def __display_map(self) -> None:
        if self.__map is not None:
            pass

    def run(self) -> None:
        """
        Run the main loop of the graph.
        """
        running: bool = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.__draw_background()
        pygame.quit()
