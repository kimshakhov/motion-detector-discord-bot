from pathlib import Path
import cv2
import time
import multiprocessing

import alarm_bot
from camera import start_cam


class Process(multiprocessing.Process):
    def __init__(self, proc_id):
        super(Process, self).__init__()
        self.id = proc_id

    def run(self):
        time.sleep(1)
        if self.id == 1:
            alarm_bot.run_discord_bot()


def file_cleanup(f_path):
    with open(f_path, 'r+') as file:
        file.truncate(0)


def pics_cleanup():
    print("cleaning pictures")

    [f.unlink() for f in Path("photos").glob("*") if f.is_file()]


if __name__ == '__main__':
    print("welcome to Kim's motion detection system")

    bot_process = Process(1)
    bot_process.start()
    start_cam()
    bot_process.join()

    print("do you want to clean the pictures? Y/N")
    if input() == "Y":
        pics_cleanup()

    file_cleanup("alarms.txt")
    file_cleanup("alarm_pic_paths.txt")

    print("finished both processes")
