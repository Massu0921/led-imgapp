from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import argparse


class Base():
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-r", "--led-rows", action="store",
                                 help="LEDのパネルのドッド行. Default: 32", default=32, type=int)
        self.parser.add_argument("--led-cols", action="store",
                                 help="LEDパネルのドット列. Default: 32", default=32, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store",
                                 help="LEDのチェーン. row*colをいくつ繋いだか. Default: 1", default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store",
                                 help="LEDを並行に何枚繋ぐか. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store",
                                 help="ビットが使用するPWM. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store",
                                 help="LEDの明るさ. 1~100. Default: 50", default=50, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping", help="外部ハードウェア使用時: regular, adafruit-hat, adafruit-hat-pwm",
                                 choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("-s", "--led-slowdown-gpio", action="store",
                                 help="gpioの速度を落とす. 0~4. Default: 1", default=1, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true",
                                 help="リフレッシュレート表示")
        self.parser.add_argument("--led-rgb-sequence", action="store",
                                 help="LEDのRGBの順番が異なる場合は設定変更する. Default: RGB", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store",
                                 help="ピクセルマッパーを適用. 例 \"Rotate:90\"", default="", type=str)

    def setup(self):
        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper

        options.row_address_type = 0
        options.multiplexing = 0
        options.show_refresh_rate = 0
        options.disable_hardware_pulsing = 1

        if self.args.led_show_refresh:
          options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio

        self.matrix = RGBMatrix(options=options)
