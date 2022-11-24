import time


class Alarm:
    def __init__(self, area, pic_path):
        self.time = time.localtime()
        self.message = ""
        self.area = area
        self.type = ""
        self.pic_path = pic_path

    def get_message(self) -> str:
        self.make_message()
        return self.message

    def make_message(self) -> None:
        if self.area > 10000:
            self.type = " big "
        else:
            self.type = " small "

        self.message = "ALARM " + self.type + "with area  = " + str(self.area) \
                       + " at time: " + time.asctime(self.time)

    def add_alarm(self):
        alarms = open("alarms.txt", "a")
        alarms.write(self.get_message() + "\n")
        alarms.close()
        pics = open("alarm_pic_paths.txt", "a")
        pics.write(self.pic_path + "\n")
        pics.close()
