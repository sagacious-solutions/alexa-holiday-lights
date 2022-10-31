import time
from rpi_ws281x import Color, PixelStrip, ws
from colors import LedColor
from typing import List


class XmasString:
    def __init__(self) -> None:
        # LED strip configuration:
        LED_COUNT = 100  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0

        self.LEFT_SIDE_PIXELS = [i for i in range(32)]
        self.TOP_PIXELS = [i for i in range(33, 66)]
        self.RIGHT_SIDE_PIXELS = [i for i in range(67, 100)]

        # Create PixelStrip object with appropriate configuration.
        self.strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
        )
        self.strip.begin()

    def rain_drop(
        self,
        pixel_n: int,
        rain_direction: int = 1,
        length=5,
        color: Color = LedColor.blue,
    ):
        tail_direction = rain_direction * -1
        end_point = pixel_n + (length * tail_direction)
        color = self.get_rgb_value(color)

        # set first pixel of rain drop
        start_color = self.get_rgb_value(self.strip.getPixelColor(pixel_n))
        self.strip.setPixelColor(pixel_n, Color(*color))
        color_diff = []
        for i in range(3):
            color_diff.append((start_color[i] - color[i]) / length)
        # xmasTree.setSolid(color=LedColor.black)

        count = 0
        for i in range(end_point, pixel_n, tail_direction * -1):
            count += tail_direction
            new_color = []
            for j in range(3):
                new_color.append(
                    round(start_color[j] + (color_diff[j] * count))
                )
            print(f"count : {count} new_color : {new_color}")
            self.strip.setPixelColor(i, Color(*new_color))
        self.strip.show()

    def door_frame_rain(
        self,
        color: Color = LedColor.blue,
    ):
        for i in range(self.RIGHT_SIDE_PIXELS[0], self.RIGHT_SIDE_PIXELS[-1]):
            self.rain_drop(i, color=color)
            time.sleep(0.05)
        for i in range(self.LEFT_SIDE_PIXELS[-1], self.LEFT_SIDE_PIXELS[0], -1):
            self.rain_drop(i, color=color)
            time.sleep(0.05)

    def set_color_for_pixels(self, pixel_list: List[int], color: Color):
        for pixel_n in pixel_list:
            self.strip.setPixelColor(pixel_n, color)
        self.strip.show()

    def color_wipe_inside_out_reversed(
        self, color, wait_ms=50, *args, **kwargs
    ):
        """Wipe color across display a pixel at a time."""
        print("color_wipe_inside_out_reversed")
        half = int(self.strip.numPixels() / 2)
        for i in range(half):
            self.strip.setPixelColor(0 + i, color)
            self.strip.setPixelColor(self.strip.numPixels() - i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def random_colors(self, *args, **kwargs):
        """Wipe color across display a pixel at a time."""
        print("color_wipe_inside_out_reversed")
        half = int(self.strip.numPixels() / 2)
        for i in range(half):
            self.strip.setPixelColor(0 + i, LedColor.get_random())
            self.strip.setPixelColor(
                self.strip.numPixels() - i, LedColor.get_random()
            )
            self.strip.show()
            time.sleep(40 / 1000.0)

    def color_wipe_inside_out(self, color, wait_ms=50, *args, **kwargs):
        """Wipe color across display a pixel at a time."""
        print(f"color_wipe_inside_out")
        half = int(self.strip.numPixels() / 2)
        for i in range(half):
            self.strip.setPixelColor(half - i, color)
            self.strip.setPixelColor(half + i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    # Define functions which animate LEDs in various ways.
    def color_wipe(self, color, wait_ms=50, reverse=False, **kwargs):
        """Wipe color across display a pixel at a time."""
        print(f"Colorwipe - Reversed:{reverse}")
        wipe_direction = (
            (self.strip.numPixels(), 0, -1)
            if reverse
            else (0, self.strip.numPixels())
        )
        for i in range(*wipe_direction):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def setSolid(self, color: Color):
        """Set to a solid color"""
        print("Setting to solid color")

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def nightRider(self, wait_ms=50, iterations=20, *args):
        print("nightRider")

        cl_ray = [0, 255, 0]

        for i in range(iterations):
            if i == 0:
                self.color_wipe(
                    color=Color(
                        cl_ray[(0 + i) % 3],
                        cl_ray[(1 + i) % 3],
                        cl_ray[(2 + i) % 3],
                    ),
                    wait_ms=1,
                )
            for j in range(self.strip.numPixels()):
                if j > 0:
                    self.strip.setPixelColor(j - 1, Color(0, 0, 0))

                self.strip.setPixelColor(
                    j,
                    Color(
                        cl_ray[(1 + i) % 3],
                        cl_ray[(2 + i) % 3],
                        cl_ray[(0 + i) % 3],
                    ),
                )
                self.strip.show()
                time.sleep(wait_ms / 1000)

            for j in range(self.strip.numPixels()):
                if j > 0:
                    self.strip.setPixelColor(
                        self.strip.numPixels() - j + 1,
                        Color(
                            cl_ray[(2 + i) % 3],
                            cl_ray[(0 + i) % 3],
                            cl_ray[(1 + i) % 3],
                        ),
                    )

                self.strip.setPixelColor(
                    self.strip.numPixels() - j, Color(255, 0, 0)
                )
                self.strip.show()
                time.sleep(wait_ms / 1000)

    def theater_chase(self, color, wait_ms=50, iterations=10, **kwargs):
        """Movie theater light style chaser animation."""
        print("theaterChase()")
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1, **kwargs):
        """Draw rainbow that fades across all pixels at once."""
        print("rainbow")
        print(wait_ms)
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        print("Rainbow Cycle")
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i,
                    self.wheel(
                        (int(i * 256 / self.strip.numPixels()) + j) & 255
                    ),
                )
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def transition_colors(self, c1, c2, time_ms=1000):
        c1 = self.get_rgb_value(c1)
        c2 = self.get_rgb_value(c2)
        # difference between colors
        dif = [c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2]]
        for j in range(time_ms):
            new_color = [
                round(c1[0] + dif[0] * (j / time_ms)),
                round(c1[1] + dif[1] * (j / time_ms)),
                round(c1[2] + dif[2] * (j / time_ms)),
            ]
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(*new_color))
            self.strip.show()

            time.sleep(0.001)

    def transition_to_color(self, color, time_ms=1000):
        current_color = self.get_rgb_value(self.strip.getPixelColor(0))
        color = self.get_rgb_value(color)
        # difference between colors
        dif = [
            color[0] - current_color[0],
            color[1] - current_color[1],
            color[2] - current_color[2],
        ]
        for j in range(time_ms):
            new_color = [
                round(current_color[0] + dif[0] * (j / time_ms)),
                round(current_color[1] + dif[1] * (j / time_ms)),
                round(current_color[2] + dif[2] * (j / time_ms)),
            ]
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(*new_color))
            self.strip.show()

            time.sleep(0.001)

    @staticmethod
    def get_rgb_value(color_int):
        r = color_int >> 16 & 0xFF
        g = color_int >> 8 & 0xFF
        b = color_int & 0xFF

        return [r, g, b]

    def loop_random_color_transition(
        self, interval_sec: float = 0, transition_time: int = 1000
    ):
        while True:
            self.transition_to_color(
                LedColor.get_random(), time_ms=transition_time
            )
            time.sleep(interval_sec)


xmasTree = XmasString()
