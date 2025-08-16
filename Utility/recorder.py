import subprocess
import os
import signal
import time
import sys
import platform


class FFmpegRecorder:
    def __init__(self, filename="recording.mp4", framerate=15):
        self.filename = os.path.abspath(filename)
        self.framerate = framerate
        self.process = None

    def _get_ffmpeg_command(self):
        # Check if ffmpeg is available
        try:
            subprocess.run(["which", "ffmpeg"], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            raise RuntimeError("ffmpeg is not installed or not in PATH. Please install ffmpeg first.")

        system = platform.system().lower()
        
        if system == "windows":
            return [
                "ffmpeg",
                "-y",
                "-f", "gdigrab",
                "-framerate", str(self.framerate),
                "-i", "desktop",
                self.filename,
            ]
        elif system == "darwin":  # macOS
            return [
                "ffmpeg",
                "-y",
                "-f", "avfoundation",
                "-i", "1",  # 1 is typically the screen capture device on macOS
                "-pix_fmt", "yuv420p",
                "-r", str(self.framerate),
                self.filename,
            ]
        else:  # Linux
            return [
                "ffmpeg",
                "-y",
                "-video_size", "1920x1080",
                "-framerate", str(self.framerate),
                "-f", "x11grab",
                "-i", ":0.0",
                self.filename,
            ]

    def start(self):
        cmd = self._get_ffmpeg_command()
        print(f"Running command: {' '.join(cmd)}")
        self.process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        # Give FFmpeg a moment to start and report any errors
        time.sleep(1)
        if self.process.poll() is not None:  # Process has already terminated
            _, stderr = self.process.communicate()
            raise RuntimeError(f"FFmpeg failed to start. Error: {stderr}")

    def stop(self):
        if self.process:
            if os.name == "nt":  # Windows
                self.process.send_signal(signal.CTRL_C_EVENT)
            else:
                self.process.terminate()
            self.process.wait()
