class agent_1():
    def method1(self):
        print("agents class design is under development")
    
    def method2(self, params):
        print("my parameters: " + params)

class agent_2(agent_1):
    def method1(self):
        agent_1.method1(self)
        print("call agent_1 methods inside agent_2 class")
    
    def method2(self, params):
        print("parameters in agent_2: " + params)

def main():

    c = agent_1()
    c.method1()
    c.method2("This is parametes variable")

    c2 = agent_2()
    c2.method1()
    c2.method2("These are parameters in method 2 class agent_2")


if __name__ == "__main__":
    main()

