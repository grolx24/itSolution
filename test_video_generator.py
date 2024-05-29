import unittest
import os
import shutil
from VideoGenerator import VideoGenerator

class TestVideoGenerator(unittest.TestCase):

    def setUp(self):
        self.test_text = "тест TEST"
        self.output_path = os.getcwd()

    def tearDown(self):
        if os.path.exists(self.output_path + "/out"):
            shutil.rmtree(self.output_path + "/out")
            os.mkdir(self.output_path + "/out")

    def test_generate_with_moviepy(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_moviepy(output_path=os.path.join(self.output_path, "/out/moviepy_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "/out/moviepy_output.mp4")))

    def test_generate_with_opencv(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_opencv(output_path=os.path.join(self.output_path, "/out/opencv_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "/out/opencv_output.mp4")))

    def test_generate_with_ffmpeg(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_ffmpeg(output_path=os.path.join(self.output_path, "/out/ffmpeg_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "/out/ffmpeg_output.mp4")))

    def test_generate_with_pygame(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_pygame(output_path=os.path.join(self.output_path, "/out/pygame_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "/out/pygame_output.mp4")))

if __name__ == "__main__":
    unittest.main()
