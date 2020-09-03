import time
from base import Base
from PIL import Image


class LEDCtrl(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ledloop = False

    def loadimg(self, imgpath):
        img = Image.open(imgpath).convert("RGB")

        # LEDサイズに画像をリサイズ(固定比)
        w, h = img.size
        re_width = int((self.matrix.height * w) / h)
        img = img.resize((re_width, self.matrix.height))

        return img

    def setup(self):
        super().setup()
        self.canvas = self.matrix.CreateFrameCanvas()

    def clear(self):
        '''LED表示をクリア
        '''
        self.canvas.Clear()
        self.matrix.SwapOnVSync(self.canvas)

    def stop(self):
        '''LED表示を停止
        '''
        self.ledloop = False
        self.clear()

    def showimage(self, pil_img, x=0, y=0):
        '''画像を表示

        Args:
            pil_img (PIL.Image.Image image mode=RGB): PILで開いた画像
            x (int): x座標
            y (int): y座標

        '''
        self.canvas.SetImage(pil_img, x, y, unsafe=self.unsafe)
        self.matrix.SwapOnVSync(self.canvas)

    def scrollimage(self, pil_img, sleep=0.01):
        '''画像をスクロール

        pixel-mapperのオプションによって縦・横向きは自動で決定

        Args:
            pil_img (PIL.Image.Image image mode=RGB): PILで開いた画像
            sleep (float): 待機時間(スクロール速度) default=0.01s

        '''
        x = 0
        y = 0
        self.ledloop = True

        while self.ledloop:
            
            # 縦向き, PIN_INが下の場合
            if "Rotate:-90" in self.args.led_pixel_mapper or "Rotate:270" in self.args.led_pixel_mapper:
                y -= 1

                if y <= -(pil_img.size[1]):
                    y = self.canvas.height

            # 横向き(default)
            else:
                x -= 1

                if x <= -(pil_img.size[0]):
                    x = self.canvas.width

            self.canvas.SetImage(pil_img, x, y, unsafe=self.unsafe)
            self.matrix.SwapOnVSync(self.canvas)
            time.sleep(sleep)

        self.clear()


if __name__ == "__main__":
    pass