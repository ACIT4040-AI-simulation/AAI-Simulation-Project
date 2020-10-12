import json

class agent_1():
    def __init__(self, name, age, sex, status, mask, antibac, socialDistance):
        self.name = name
        self.age = age
        self.sex = sex
        self.status = status #infected, recoverd, normal, exposed, dead,
        self.mask = mask
        self.antibac = antibac #rate 1-6
        self.socilDistance = socialDistance # rate setted with local agency
        # print("agents class design is under development")
    
    def tostring(self):
        print(self.name)
        print(self.age)
        print(self.sex)
        print(self.status)
        print(self.mask)
        print(self.antibac)
        print(self.socilDistance)
        print("----------------------------")

# class agent_2(agent_1):
#     def method1(self):
#         agent_1.method1(self)
#         print("call agent_1 methods inside agent_2 class")
    
#     def method2(self, params):
#         print("parameters in agent_2: " + params)



def main():

    agenList = json.load(open("agentdata.json"))

    for agent in agenList:
        temp = agent_1(agent['name'], agent['age'], agent['gender'], agent['status'], agent['mask'], agent['antibact'], agent['socialDistance'])
        print(temp.tostring())


  

    # c = agent_1()
    # c.method1()
    # c.method2("This is parametes variable")

    # c2 = agent_2()
    # c2.method1()
    # c2.method2("These are parameters in method 2 class agent_2")


if __name__ == "__main__":
    main()

