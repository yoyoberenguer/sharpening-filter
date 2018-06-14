import pygame
import numpy
import time
import math

__author__ = "Yoann Berenguer"
__copyright__ = "Copyright 2007."
__credits__ = ["Yoann Berenguer"]
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Yoann Berenguer"
__email__ = "yoyoberenguer@hotmail.com"
__status__ = "Demo"

class Sharpen2:

    def __init__(self, surface_, array_):

        self.sharpen_kernel = \
            numpy.array(([0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0])).astype(dtype=numpy.float)
        self.kernel_half = 1
        self.surface = surface_
        self.array = array_
        self.shape = array_.shape
        self.source_array = numpy.zeros((self.shape[0], self.shape[1], 3))
        self.kernel_length = len(self.sharpen_kernel)
        self.kernel_weight = numpy.sum(self.sharpen_kernel)
        assert self.kernel_weight != 0, 'Kernel weight should not be zero.'

    def run(self):

        for y in range(0, self.shape[1]):

            for x in range(0, self.shape[0]):
                r, g, b = 0, 0, 0
                # Apply both kernels at once for each pixels
                try:

                    data = self.array[x - 1:x + 2, y - 1:y + 2, :]

                    r = sum(numpy.multiply(data[:, :, 0], self.sharpen_kernel).reshape(9))
                    g = sum(numpy.multiply(data[:, :, 1], self.sharpen_kernel).reshape(9))
                    b = sum(numpy.multiply(data[:, :, 2], self.sharpen_kernel).reshape(9))

                except:
                   s2 = 0
                self.source_array[x, y] = (r / self.kernel_weight, g / self.kernel_weight, b / self.kernel_weight)
        # cap the values
        numpy.putmask(self.source_array, self.source_array > 255, 255)
        numpy.putmask(self.source_array, self.source_array < 0, 0)
        return self.source_array


class Sharpen:

    def __init__(self, surface_, array_):

        self.sharpen_kernel = \
            numpy.array(([0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0])).astype(dtype=numpy.float)
        self.kernel_half = 1
        self.surface = surface_
        self.array = array_
        self.shape = array_.shape
        self.source_array = numpy.zeros((self.shape[0], self.shape[1], 3))
        self.kernel_length = len(self.sharpen_kernel)
        self.kernel_weight = numpy.sum(self.sharpen_kernel)
        assert self.kernel_weight != 0, 'Kernel weight should not be zero.'

    def run(self):

        for y in range(0, self.shape[1]):

            for x in range(0, self.shape[0]):

                r, g, b = 0, 0, 0

                for kernel_offset_y in range(-self.kernel_half, self.kernel_half + 1):

                    for kernel_offset_x in range(-self.kernel_half, self.kernel_half + 1):

                        xx = x + kernel_offset_x
                        yy = y + kernel_offset_y

                        try:
                            color = self.surface.get_at((xx, yy))
                            k = self.sharpen_kernel[kernel_offset_y + self.kernel_half,
                                                    kernel_offset_x + self.kernel_half]

                            r += color[0] * k / self.kernel_weight
                            g += color[1] * k / self.kernel_weight
                            b += color[2] * k / self.kernel_weight

                        except IndexError:

                            k = self.sharpen_kernel[kernel_offset_y + self.kernel_half,
                                                    kernel_offset_x + self.kernel_half]
                            r += 128 * k / self.kernel_weight
                            g += 128 * k / self.kernel_weight
                            b += 128 * k / self.kernel_weight

                self.source_array[x][y] = (r, g, b)
        numpy.putmask(self.source_array, self.source_array > 255, 255)
        numpy.putmask(self.source_array, self.source_array < 0, 0)
        return self.source_array


if __name__ == '__main__':
    numpy.set_printoptions(threshold=numpy.nan)

    SIZE = (800, 600)
    SCREENRECT = pygame.Rect((0, 0), SIZE)
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.RESIZABLE, 32)
    TEXTURE1 = pygame.image.load("Assets\\Graphics\\seychelles.jpg").convert()
    TEXTURE1 = pygame.transform.smoothscale(TEXTURE1, (SIZE[0], SIZE[1] >> 1))
    # Texture re-scale to create extra data (padding) on each sides
    PADDING = pygame.transform.smoothscale(TEXTURE1, (SIZE[0] + 8, (SIZE[1] >> 1) + 8))

    # 8.9 seconds for 800x300
    # Sharp = Sharpen(TEXTURE1, pygame.surfarray.array3d(TEXTURE1))
    # 9.5 seconds for 800x300
    Sharp = Sharpen2(TEXTURE1, pygame.surfarray.array3d(TEXTURE1))

    t = time.time()
    array = Sharp.run()
    print(time.time() - t)

    FRAME = 0
    clock = pygame.time.Clock()
    STOP_GAME = False
    PAUSE = False

    while not STOP_GAME:

        pygame.event.pump()

        while PAUSE:
            event = pygame.event.wait()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_PAUSE]:
                PAUSE = False
                pygame.event.clear()
                keys = None
            break

        for event in pygame.event.get():

            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                print('Quitting')
                STOP_GAME = True

            elif event.type == pygame.MOUSEMOTION:
                MOUSE_POS = event.pos

            elif keys[pygame.K_PAUSE]:
                PAUSE = True
                print('Paused')

        surface = pygame.surfarray.make_surface(array)

        SCREEN.fill((0, 0, 0, 0))
        SCREEN.blit(TEXTURE1, (0, 0))
        SCREEN.blit(surface, (0, SIZE[1] // 2))

        pygame.display.flip()
        TIME_PASSED_SECONDS = clock.tick(120)
        FRAME += 1

    pygame.quit()
