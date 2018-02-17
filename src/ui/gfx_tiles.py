import pygame
from pygame.sprite import Sprite

MAGENTA = (255, 0, 255)


class Tiles(Sprite):
  def __init__(self, filename, tile_size, margin=0):
    self.fn = filename
    self.tile_s = tile_size
    self.tile_m = margin
    self.image = pygame.image.load(filename)
    self.tiles = {}

  def get_tiles(self):
    img_w = self.image.get_width()
    img_h = self.image.get_height()
    sheet_w = img_w // (self.tile_s + self.tile_m)
    sheet_h = img_h // (self.tile_s + self.tile_m)
    tmp_surface = pygame.Surface((self.tile_s, self.tile_s))
    tmp_surface.set_colorkey(MAGENTA)

    for row in range(sheet_h):
      for column in range(sheet_w):
        # TODO: maybe not only quadrant tiles
        tile_rect =  (row * (self.tile_s + self.tile_m), column * (self.tile_s + self.tile_m), self.tile_s, self.tile_s)
        pygame.Surface.blit(self.image, tmp_surface, tile_rect)
        self.tiles.update({row * column: tmp_surface})


# this section only for testing
if __name__ == '__main__':
  MyTiles = Tiles(u"../../res/spritesheet_magenta.png", 16, 1)
  MyTiles.get_tiles()
  print(len(MyTiles.tiles))
  pygame.init()
  screen =pygame.display.set_mode((600, 400))
  screen.blit(MyTiles.tiles[1], (100,100))
  pygame.display.update()
