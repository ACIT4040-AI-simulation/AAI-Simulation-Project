#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:30:26 2020

@author: kassahundegena
"""

  
import json
import itertools

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
        self.agentsList = []
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
    classAgentsList = []

    for classroom in classRoomList:
        temp = classRoom(classroom['class_id'], classroom['class_type'], classroom['length'], classroom['width'], classroom['sitting_capacity'], classroom['cleaning_cycle'], classroom['clean_status'], classroom['antibac_dispenser'], classroom['ventilation_grade'])
        classAgentsList.append(temp)
        tostr = temp.to_string()
        print(tostr)
    print(test(classRoomList,classAgentsList))
        
def test(classRoomList, classAgentsList):
    testResult = '!faild'
    if len(classRoomList) == len(classAgentsList):
        for (classroom, classagents) in zip(classRoomList, classAgentsList):
                
            if(
                classroom['class_id'] ==classagents.class_id and
                classroom['class_type']== classagents.class_type and
                classroom['length'] == classagents.length and
                classroom['width']== classagents.width and
                classroom['sitting_capacity']== classagents.sitting_capacity and
                classroom['cleaning_cycle']== classagents.cleaning_cycle and
                classroom['clean_status']== classagents.clean_status and
                classroom['antibac_dispenser']== classagents.antibac_dispenser and
                classroom['ventilation_grade']== classagents.ventilation_grade):
                continue
            else:
                return testResult
        testResult = 'Test has passed No data integrity issue'
    return testResult
           

if __name__ == "__main__":
    main()