  
import json

class classRoom():
    def __init__(self,class_id, class_type, length, width, sitting_capacity, cleaning_cycle, clean_status, antibac_dispenser,ventilation_grade):
        self.class_id = class_id
        self.class_type = class_type # office, commonarea, lab, lectureroom
        self.length = length
        self.width = width
        self.sitting_capacity= sitting_capacity
        self.cleaning_cycle = cleaning_cycle  #how offen the the room get clean
        self.clean_status = clean_status # boolian clean or not
        self.antibac_dispenser = antibac_dispenser #boolian has dispensor or not
        self.ventilation_grade = ventilation_grade # rate setted with local agency
        # print("agents class design is under development")
    
    def to_string(self):
        print(self.class_id)
        print(self.class_type)
        print(self.length)
        print(self.width)
        print(self.sitting_capacity)
        print(self.cleaning_cycle) 
        print(self.clean_status)
        print(self.antibac_dispenser) 
        print(self.ventilation_grade)
        print("----------------------------")
        

def main():

    classRoomList = json.load(open("classrooms.json"))

    for classroom in classRoomList:
        temp = classRoom(classroom['class_id'], classroom['class_type'], 
                         classroom['length'], classroom['width'], classroom['sitting_capacity'], 
                         classroom['cleaning_cycle'], classroom['clean_status'], classroom['antibac_dispenser'],
                         classroom['ventilation_grade'])
        print(temp.to_string())


if __name__ == "__main__":
    main()