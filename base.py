import argparse
import subprocess

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


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
        self.parser.add_argument("-ns", "--led-pwm-lsb-nanoseconds", action="store",
                                 help="最下位有効ビットのオンタイムの基準時間単位(ns). Default: 130", default=130, type=int)
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
        self.parser.add_argument("-pm", "--led-pixel-mapper", action="store",
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
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper

        options.row_address_type = 0
        options.multiplexing = 0
        options.show_refresh_rate = 0
        options.disable_hardware_pulsing = 0

        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        # ラズパイ判別
        model = subprocess.run(
            ["cat", "/proc/device-tree/model"], encoding='utf-8', stdout=subprocess.PIPE)
        # Pi4の場合, SetImageのunsafeを有効, gpio速度低下
        if "Raspberry Pi 4" in model.stdout:
            self.unsafe = False
            
            if self.args.led_slowdown_gpio < 2:
                options.gpio_slowdown = 3
            else:
                options.gpio_slowdown = self.args.led_slowdown_gpio

        else:
            self.unsafe = True
            options.gpio_slowdown = self.args.led_slowdown_gpio

        self.matrix = RGBMatrix(options=options)