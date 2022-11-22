from pathlib import Path
import cv2
import time
import multiprocessing

import alarm_bot
import alarm_class


def say_alarm(statement):
    print("adding " + statement)


def do_alarm(area, pic_path):
    new_alarm = alarm_class.Alarm(area, pic_path)
    msg = new_alarm.get_message()
    new_alarm.add_alarm()
    say_alarm(msg)


def start_camera(cap):
    status, start_frame = cap.read()
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
    return start_frame


def get_contours(start_frame, frame):
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bw = cv2.GaussianBlur(frame_bw, (21, 21), 0)
    difference = cv2.absdiff(frame_bw, start_frame)
    threshold = cv2.threshold(difference, 70, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    contours, res = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def do_camera(cap):
    print("starting the camera")
    start_frame = start_camera(cap)
    last_update_frame = start_frame
    last_update_time = time.time()

    last_alarm_time = time.time() - 3
    alarm_mode = False
    alarm_counter = 0
    alarm_area = 0
    print("starting surveillance system")
    while True:
        status, frame = cap.read()
        if alarm_mode:

            if last_update_time + 3 < time.time():
                last_update_frame = start_camera(cap)
                last_update_time += 3

            red_contours = get_contours(last_update_frame, frame)
            green_contours = get_contours(start_frame, frame)

            for contour in red_contours:
                if cv2.contourArea(contour) < 3000:
                    continue
                (x, y, x2, y2) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + x2, y + y2), (0, 0, 255), 3)
                alarm_counter += 1
                alarm_area += cv2.contourArea(contour)

            for contour in green_contours:
                if cv2.contourArea(contour) < 10000:
                    continue
                (x, y, x2, y2) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + x2, y + y2), (0, 255, 0), 3)
                alarm_counter += 0

        key = cv2.waitKey(25)
        cv2.imshow("Cam", frame)

        if alarm_counter > 0 and last_alarm_time + 3 < time.time():
            pic_name = str(alarm_area) + ".jpg"
            print("pic name is : " + pic_name)
            pic_path = "photos/" + pic_name
            cv2.imwrite(pic_path, frame)
            do_alarm(alarm_area, pic_path)
            alarm_area, alarm_counter = 0, 0
            last_alarm_time = time.time()

        if key == ord("t"):
            alarm_mode = not alarm_mode
            print("CHANGING ALARM MODE")
            alarm_counter = 0
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


class Process(multiprocessing.Process):
    def __init__(self, proc_id):
        super(Process, self).__init__()
        self.id = proc_id

    def run(self):
        time.sleep(1)
        if self.id == 0:
            url = 'rtsp://admin:ODDHUW@192.168.8.35:554/Streaming/Channels/101'
            network_cam = cv2.VideoCapture(0)
            do_camera(network_cam)
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

    p0 = Process(0)
    p0.start()
    p1 = Process(1)
    p1.start()
    p0.join()
    p1.join()

    print("do you want to clean the pictures? Y/N")

    if input() == "Y":
        pics_cleanup()

    file_cleanup("alarms.txt")
    file_cleanup("alarm_pic_paths.txt")

    print("finished both processes")
