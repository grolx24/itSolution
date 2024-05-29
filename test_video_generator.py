import unittest
import os

class TestVideoGenerator(unittest.TestCase):

    def setUp(self):
        self.test_text = "тест TEST"
        self.output_path = "test_output"

    def tearDown(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def test_generate_with_moviepy(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_moviepy(output_path=os.path.join(self.output_path, "moviepy_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "moviepy_output.mp4")))

    def test_generate_with_opencv(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_opencv(output_path=os.path.join(self.output_path, "opencv_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "opencv_output.mp4")))

    def test_generate_with_ffmpeg(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_ffmpeg(output_path=os.path.join(self.output_path, "ffmpeg_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "ffmpeg_output.mp4")))

    def test_generate_with_pygame(self):
        VG = VideoGenerator(text=self.test_text)
        VG.generate_with_pygame(output_path=os.path.join(self.output_path, "pygame_output.mp4"))
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "pygame_output.mp4")))

if __name__ == "__main__":
    unittest.main()
