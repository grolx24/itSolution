import os
import numpy as np
from moviepy.editor import VideoClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import cv2
import pygame
import sys
import shutil
from django.conf import settings
import subprocess

class VideoGenerator:

    def __init__(self, text = "Хеллоу мир!"):
        self.video_duration = 3  # Продолжительность видео в секундах
        self.video_size = (100, 100)  # Размер видео (ширина, высота)
        self.fps = 25 # кадров в секунду
        self.background_color = (255, 0, 255) 
        self.text_fontsize = 69
        self.text = text  # Текст бегущей строки
        self.pathMoviePy = "C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"
        self.output_path = self.get_output_path()

        if not os.path.exists(self.output_path + "/out"):
            os.makedirs(self.output_path + "/out")

        # Проверка наличия программ
        self.check_imagemagick()
        self.check_ffmpeg()

    def get_output_path(self):
        try:
            return str(settings.BASE_DIR)

        except:
            return os.getcwd()


    def check_imagemagick(self):
        if not shutil.which("magick") and not shutil.which("convert"):
            raise EnvironmentError("ImageMagick is not installed or not found in the system PATH.")

    def check_ffmpeg(self):
        if not shutil.which("ffmpeg"):
            raise EnvironmentError("FFmpeg is not installed or not found in the system PATH.")

    def generate_with_moviepy(self, output_path=None):
        #change_settings({"IMAGEMAGICK_BINARY": self.pathMoviePy}) #местоположение ImageMagick
        if output_path is None:
           output_path = self.output_path + "/out/moviepy_output.mp4"

        self.background_color = (255, 0, 255)  # magenta
        text_color = 'white'

        # Функция для создания фона
        def make_frame(t):
            return np.full((self.video_size[1], self.video_size[0], 3), self.background_color, dtype=np.uint8)

        # Создаем фоновый клип
        background_clip = VideoClip(make_frame, duration=self.video_duration)
        # Создаем текстовый клип
        text_clip = TextClip(self.text, fontsize=self.text_fontsize, color=text_color)

        # Определяем начальные и конечные координаты текста
        text_width, text_height = text_clip.size
        start_pos = (self.video_size[0], self.video_size[1]//2 -  text_height//2)
        end_pos = (-text_width-self.video_size[0], start_pos[1])

        print(start_pos[1], text_height)
        # Анимация движения текста
        text_clip = text_clip.set_position(lambda t: (
            int(start_pos[0] + (end_pos[0] - start_pos[0]) * t /  self.video_duration), start_pos[1]
        )).set_duration(self.video_duration)

        # Комбинируем фоновый клип и текстовый клип
        final_clip = CompositeVideoClip([background_clip, text_clip])

        # Сохраняем финальное видео
        final_clip.write_videofile(output_path, fps=25)

    def generate_with_opencv(self, output_path = None):
        if output_path is None:
            output_path = self.output_path + "/out/opencv_output.mp4"
        text_color = (255, 255, 255)  # Цвет текста (BGR)
        text_fontscale = 2  # Размер шрифта текста
        text_thickness = 3  # Толщина текста

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, self.video_size)

        num_frames = self.video_duration * self.fps
        text_size = cv2.getTextSize(
            self.text, cv2.FONT_HERSHEY_COMPLEX, text_fontscale, text_thickness)[0]
        text_width = text_size[0]

        for i in range(num_frames):
            # рисуем фон
            frame = np.full((self.video_size[1], self.video_size[0], 3), self.background_color, dtype=np.uint8)
            # вычисляем коорд-ы текста
            x = int(self.video_size[0] - (text_width + self.video_size[0]) * (i / num_frames))
            y = self.video_size[1]  - text_size[1]
            # рисуем            
            cv2.putText(frame, self.text, (x, y), cv2.FONT_HERSHEY_COMPLEX, text_fontscale, text_color, text_thickness)
            # пишем
            out.write(frame)

        out.release()

    def generate_with_ffmpeg(self, output_path=None):
            if output_path is None:
                output_path = os.path.join(self.output_path, "out", "ffmpeg_output.mp4")
            
            cmd = [
                'ffmpeg',
                '-y',
                '-i', os.path.join(self.output_path, 'data', 'background.mp4'),
                '-r', str(self.fps),
                '-vf', (
                    f"drawtext=fontfile='{os.path.join(self.output_path, 'data', 'arial.ttf')}':"
                    f"text='{self.text}':"
                    f"fontcolor=white:fontsize={self.text_fontsize}:"
                    f"x='w + n/({self.video_duration * self.fps}) * (-w-tw)':"
                    f"y=-(line_h/2)+h/2"
                ),
                output_path
            ]
            
            # Encode the command using UTF-8
            encoded_cmd = [arg.encode('utf-8') if isinstance(arg, str) else arg for arg in cmd]
            
            try:
                result = subprocess.run(encoded_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print("Video generated successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e.stderr.decode('utf-8')}")

    def generate_with_pygame(self, output_path=None):
        if output_path is None:
            output_path = self.output_path + "/out/pygame_output.mp4"
        background_color = (255, 0, 255)  # Цвет фона (RGB) magenta       
        text_color = (255, 255, 255)  # Цвет текста (RGB) white

        pygame.init()
        screen = pygame.Surface(self.video_size)
        # clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, self.text_fontsize)
        text_surface = font.render(self.text, True, text_color)
        text_width, text_height = text_surface.get_size()
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, self.video_size)
        
        num_frames = self.video_duration * self.fps
        
        for i in range(num_frames):
            # вычисляем кадр
            screen.fill(self.background_color)
            x = int(self.video_size[0] - (text_width + self.video_size[0]) * (i / num_frames))
            y = self.video_size[1]//2 - text_height//2
            # рисуем
            screen.blit(text_surface, (x, y))
            
            # записываем
            frame = np.array(pygame.surfarray.array3d(screen))
            frame = np.transpose(frame, (1, 0, 2))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
        
        out.release()
        pygame.quit()

if __name__ == "__main__":
    VG = VideoGenerator()
    VG.generate_with_moviepy()
    VG.generate_with_pygame()
    VG.generate_with_ffmpeg()
    VG.generate_with_opencv()
    
