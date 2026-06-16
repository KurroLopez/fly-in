import pygame
from pygame.surface import Surface
from map import Map
from entities import Hub, ZoneType
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
        """
        Draw the background image on the screen.
        """
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
        """
        Initialize the background by loading the assets and
        setting the background image.
        """
        assets.load_image(Path("assets"))
        self.__bg = assets.IMG.get("background")
        self.__draw_background()

    def __display_connection(self, start_hub: Hub, end_hub: Hub,
                             capacity: int) -> None:
        """
        Display a connection between two hubs on the screen.

        :param start_hub: The starting hub.
        :param end_hub: The ending hub.
        :param capacity: The capacity of the connection.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        grid_size: int = 150
        hub_size: int = 50
        start_posX: int = start_hub.properties.posX
        start_posY: int = start_hub.properties.posY
        end_posX: int = end_hub.properties.posX
        end_posY: int = end_hub.properties.posY

        center_x: int = 90  # screen.get_width() // 10
        center_y: int = screen.get_height() // 2

        start_center: Vector2 = Vector2(center_x + (start_posX * grid_size),
                                        center_y + (start_posY * grid_size))
        end_center: Vector2 = Vector2(center_x + (end_posX * grid_size),
                                      center_y + (end_posY * grid_size))
        direction: Vector2 = end_center - start_center
        if direction.length_squared() == 0:
            return

        border_offset: float = hub_size / (2 * max(abs(direction.x),
                                                   abs(direction.y)))
        start_point: Vector2 = start_center + (direction * border_offset)
        end_point: Vector2 = end_center - (direction * border_offset)

        pygame.draw.line(screen, (255, 255, 255),
                         start_point, end_point, width=6)
        pygame.draw.line(screen, (0, 0, 0),
                         start_point, end_point, width=4)

        if capacity <= 1:
            return

        font = assets.FONT
        if font is None:
            return

        label = font.render(str(capacity), True, (255, 255, 255), (0, 0, 0))
        label_rect = label.get_rect(center=((start_point.x + end_point.x) / 2,
                                            (start_point.y + end_point.y) / 2))
        screen.blit(label, label_rect)

    def __display_hub(self, hub: Hub) -> None:
        """
        Display a hub on the screen.

        :param hub: The hub to display.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        grid_size: int = 150
        hub_size: int = 50
        posX: int = hub.properties.posX
        posY: int = hub.properties.posY
        center_x: int = 90  # screen.get_width() // 10
        center_y: int = screen.get_height() // 2
        hub_center: Vector2 = Vector2(center_x + (posX * grid_size),
                                      center_y + (posY * grid_size))

        img: Surface = assets.get_square_color(hub.properties.color, hub_size)
        rect = img.get_rect(center=hub_center)
        screen.blit(img, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, width=2)

        font = assets.FONT
        if font is None:
            return

        font_color: tuple[int, int, int] = (255, 255, 255)
        background_color: tuple[int, int, int] = (0, 0, 0)

        if hub.properties.type == ZoneType.PRIORITY:
            font_color = (0, 0, 0)  # Black for priority zones
            background_color = (0, 255, 0)  # Green for priority zones
        if hub.properties.type == ZoneType.RESTRICTED:
            font_color = (0, 0, 0)  # Black for restricted zones
            background_color = (255, 255, 0)  # Yellow for restricted zones
        if hub.properties.type == ZoneType.BLOCKED:
            background_color = (255, 0, 0)  # Red for blocked zones
        h_lbl = font.render(f" {hub.name} ", True, font_color,
                            background_color)
        if hub.properties.posX % 2 == 0:
            h_rec = h_lbl.get_rect(midtop=(rect.centerx, rect.top - 25))
        else:
            h_rec = h_lbl.get_rect(midbottom=(rect.centerx,
                                              rect.bottom + 25))
        screen.blit(h_lbl, h_rec)

        if hub.properties.max_drones > 1:
            md_lbl = font.render(f" ({hub.properties.max_drones}) ",
                                 True,
                                 font_color,
                                 background_color)
            if hub.properties.posX % 2 == 0:
                md_rec = md_lbl.get_rect(midbottom=(rect.centerx,
                                                    rect.bottom + 25))
            else:
                md_rec = md_lbl.get_rect(midtop=(rect.centerx, rect.top - 25))

            screen.blit(md_lbl, md_rec)

    def __display_map(self) -> None:
        """
        Display the entire map, including hubs and connections.
        """
        if self.__map is None:
            return

        self.__draw_background()

        start_hub: Hub | None = self.__map.start_hub
        if start_hub is not None:
            self.__display_hub(start_hub)
        end_hub: Hub | None = self.__map.end_hub
        if end_hub is not None:
            self.__display_hub(end_hub)
        for hub in self.__map.hubs.values():
            self.__display_hub(hub)

        for connection in self.__map.connections.values():
            start_hub: Hub | None = connection.origin
            end_hub: Hub | None = connection.destination
            if start_hub is None or end_hub is None:
                continue
            self.__display_connection(start_hub, end_hub,
                                      connection.properties.max_link_capacity)

        pygame.display.flip()
        pygame.display.update()

    def __display_menu(self) -> None:
        """
        Display the menu on the screen.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        font = assets.FONT_BIG
        if font is None:
            return

        surface = Surface((size, size))
        surface.fill(color)
        return surface

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
                    self.__display_map()
        pygame.quit()
