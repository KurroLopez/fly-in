import pygame
from pygame.surface import Surface
from map import Map
from entities import Hub, ZoneType, Drone
import assets
from pathlib import Path
from pygame import Vector2
from process import Process
from typing import List, Generator


class Graph:
    # Define your minimum window size
    MIN_WIDTH = 1408
    MIN_HEIGHT = 768

    INITIAL_WIDTH = 1408
    INITIAL_HEIGHT = 768

    HUB_SIZE = 80
    CONNECTION_WIDTH = 6
    GRID_SIZE = 150

    __map: Map | None = None
    __bg: Surface | None = None
    __process: Process | None = None
    __imgs: dict[str, Surface] = {}
    __auto: bool = False
    __has_finised: bool = False

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
        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_mode((width, height), pygame.RESIZABLE)
        assets.load_image(Path("assets"))
        self.__map = map
        self.__process = Process(map) if map is not None else None
        if self.__process is not None:
            self.__process.calculate_moves()
            self.__process.restart_drones()
        self.__imgs = assets.IMG
        icon = self.__imgs.get("icon")
        if icon is not None:
            pygame.display.set_icon(icon)
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
        bg = self.__imgs.get("background")
        if bg is not None:
            self.__bg = bg
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

        grid_size: int = self.GRID_SIZE
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

        border_offset: float = self.HUB_SIZE / (2 * max(abs(direction.x),
                                                abs(direction.y)))
        start_point: Vector2 = start_center + (direction * border_offset)
        end_point: Vector2 = end_center - (direction * border_offset)

        pygame.draw.line(screen, "white",
                         start_point, end_point, width=self.CONNECTION_WIDTH)
        pygame.draw.line(screen, "black",
                         start_point, end_point,
                         width=self.CONNECTION_WIDTH - 2)

        if capacity <= 1:
            return

        font = assets.FONT
        if font is None:
            return

        label = font.render(str(capacity), True, "white", "black")
        label_rect = label.get_rect(center=((start_point.x + end_point.x) / 2,
                                            (start_point.y + end_point.y) / 2))
        screen.blit(label, label_rect)

    def __display_hub(self, hub: Hub) -> Vector2:
        """
        Display a hub on the screen.

        :param hub: The hub to display.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return Vector2(0, 0)

        grid_size: int = self.GRID_SIZE
        posX: int = hub.properties.posX
        posY: int = hub.properties.posY
        center_x: int = 90  # screen.get_width() // 10
        center_y: int = screen.get_height() // 2
        hub_center: Vector2 = Vector2(center_x + (posX * grid_size),
                                      center_y + (posY * grid_size))

        img: Surface = assets.get_square_color(hub.properties.color,
                                               self.HUB_SIZE)
        rect = img.get_rect(center=hub_center)
        screen.blit(img, rect)
        pygame.draw.rect(screen, "black", rect, width=2)

        font = assets.FONT
        if font is None:
            return Vector2(0, 0)

        font_color: str = "white"
        background_color: str = "black"

        if hub.properties.type == ZoneType.PRIORITY:
            font_color = "black"  # Black for priority zones
            background_color = "green"  # Green for priority zones
        if hub.properties.type == ZoneType.RESTRICTED:
            font_color = "black"  # Black for restricted zones
            background_color = "yellow"  # Yellow for restricted zones
        if hub.properties.type == ZoneType.BLOCKED:
            background_color = "red"  # Red for blocked zones
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
        return hub_center

    def __display_map(self) -> None:
        """
        Display the entire map, including hubs and connections.
        """
        if self.__map is None:
            return

        self.__draw_background()
        self.__display_menu()
        start_hub: Hub | None = None
        end_hub: Hub | None = None
        position: Vector2 | None = None

        start_hub = self.__map.start_hub
        if start_hub is not None:
            position = self.__display_hub(start_hub)
            start_hub.position = position
        end_hub = self.__map.end_hub
        if end_hub is not None:
            position = self.__display_hub(end_hub)
            end_hub.position = position
        for hub in self.__map.hubs.values():
            position = self.__display_hub(hub)
            hub.position = position

        for connection in self.__map.connections.values():
            start_hub = connection.origin
            end_hub = connection.destination
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

        font = assets.FONT
        if font is None:
            return

        font_big = assets.FONT_BIG
        if font_big is None:
            return

        # Draw the menu background
        width: int = screen.get_width()
        mid_x: int = (width // 2) - 250
        surface1 = Surface((500, 300))
        surface1.fill(color="white")
        surface_rect = surface1.get_rect(topleft=(mid_x + 20, 20),
                                         bottomright=(mid_x + 520, 320))
        screen.blit(surface1, surface_rect)
        surface2 = Surface((500, 300))
        surface2.fill(color="blue")
        surface_rect = surface2.get_rect(topleft=(mid_x, 0),
                                         bottomright=(mid_x + 500, 300))
        screen.blit(surface2, surface_rect)

        line_start: tuple[int, int] = (mid_x, 75)
        line_end: tuple[int, int] = (mid_x + 500, 75)
        pygame.draw.line(screen, "white", line_start, line_end, width=4)

        # Draw the menu title
        title: Surface = font_big.render("-= Fly-in =-", True, "white", "blue")
        title_rect = title.get_rect(center=(mid_x + 250, 35))
        screen.blit(title, title_rect)

        opt1: Surface = font.render("ESC: Exit", True, "white", "blue")
        opt1_rect = opt1.get_rect(topleft=(mid_x + 20, 100))
        screen.blit(opt1, opt1_rect)

        self.__display_auto_option()
        self.__display_next_step_option()
        self.__update_display_turn()

    def __disable_turn(self) -> None:
        """
        Disable turn option because the process has finished
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        width: int = screen.get_width()
        mid_x: int = (width // 2) - 250

        font = assets.FONT
        if font is None:
            return
        text: str = "A: Auto OFF"
        opt1: Surface = font.render(text, True, "dimgray", "blue")
        opt1_rect = opt1.get_rect(topleft=(mid_x + 20, 150))
        screen.blit(opt1, opt1_rect)
        opt2: Surface = font.render("SPACE: Next step", True,
                                    "dimgray", "blue")
        opt2_rect = opt2.get_rect(topleft=(mid_x + 20, 200))
        screen.blit(opt2, opt2_rect)

    def __display_auto_option(self) -> None:
        """
        Display the "Auto" option on the screen.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        width: int = screen.get_width()
        mid_x: int = (width // 2) - 250

        font = assets.FONT
        if font is None:
            return

        forecolor: str = "white"
        if self.__auto:
            forecolor = "green"  # Green for auto mode enabled
        text: str = "A: Auto ON " if self.__auto else "A: Auto OFF"
        opt1: Surface = font.render(text, True, forecolor, "blue")
        opt1_rect = opt1.get_rect(topleft=(mid_x + 20, 150))
        screen.blit(opt1, opt1_rect)

    def __display_next_step_option(self) -> None:
        """
        Display the "Next Step" option on the screen.

        :param mid_x: The x-coordinate of the middle of the screen.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        width: int = screen.get_width()
        mid_x: int = (width // 2) - 250

        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        font = assets.FONT
        if font is None:
            return

        forecolor: str = "white"
        if self.__auto:
            forecolor = "dimgray"  # Gray if auto mode is enabled
        opt2: Surface = font.render("SPACE: Next step", True,
                                    forecolor, "blue")
        opt2_rect = opt2.get_rect(topleft=(mid_x + 20, 200))
        screen.blit(opt2, opt2_rect)

    def __update_display_turn(self) -> None:
        """
        Update the display to show the current turn number.
        """
        screen: Surface | None = pygame.display.get_surface()
        if screen is None:
            return

        font = assets.FONT_BIG
        if font is None:
            return

        width: int = screen.get_width()
        mid_x: int = (width // 2) - 250

        current_turn: int = self.__process.turn if self.__process else 0
        turn_label = font.render(f"Move {current_turn}", True,
                                 "white", "blue")
        turn_label_rect = turn_label.get_rect(center=(mid_x + 250, 260))
        screen.blit(turn_label, turn_label_rect)

    def __display_drones(self) -> None:
        """
        Display all drones on the screen.
        """
        if self.__process is None:
            return

        for drone in self.__process.drones:
            drone.draw(pygame.display.get_surface())

    def __next(self):
        move_info: List[Drone, Hub, Hub, bool]
        event: Generator[List[Drone, Hub, Hub, bool],
                         None, None] = self.__process.generator_next()
        try:
            move_info = next(event)
            for drone, _, _, _ in move_info:
                drone.print()
            self.__display_drones()
            self.__update_display_turn()
        except GeneratorExit:
            self.__auto = 0
            self.__has_finised = True
            self.__disable_turns()

    def run(self) -> None:
        """
        Run the main loop of the graph.
        """
        running: bool = True
        clock = pygame.time.Clock()
        self.__display_map()
        auto_play: int = 0
        self.__display_drones()
        while running:
            clock.tick(60)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if not self.__has_finised:
                            if not self.__auto and self.__process is not None:
                                self.__next()
                    if event.key == pygame.K_a:
                        if not self.__has_finised:
                            self.__auto = not self.__auto
                            self.__display_auto_option()
                            self.__display_next_step_option()
                            auto_play = 0
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
            if not self.__has_finised:
                if self.__auto and self.__process is not None:
                    auto_play -= clock.get_time()
                    if auto_play <= 0:
                        self.__next()
                        auto_play = 250
        pygame.quit()
