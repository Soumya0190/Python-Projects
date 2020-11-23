import collections

class Assignment:
    def __init__(self, name, earnedPts, possiblePts):
        self.description = name
        self.score = earnedPts
        self.total = possiblePts

    def getDescription(self) -> str:
        #returns description of assignment
        return str(self.description)
    
    def getScore(self) -> float:
        #returns total points earned by student
        return float(self.score)
    
    def getTotal(self) -> float:
        #returns total points possible for assignment
        return float(self.total)
    
    def changeScore(self, score: float):
        #changes total points earned by student
        self.score = float(score)
        return None

class CategoryAssignment(Assignment):   
    def __init__(self, description1, category1, score1, total1):
        super().__init__(description1, score1, total1)
        self.category = category1
        

    def getCategory(self) -> str:
        #returns category of assignment
        return self.category

class Student:     
    def __init__(self, ID: int):
        self.lst = list()
        self.id = ID

    def getId(self) -> int:
        #returns student ID number
        return int(self.id)

    def getScore(self, assignmentName: str) -> float:
        #searches assignment description for assignmentName
        #returns score of assignment 
        #if assignment not found, nothing returned
        for assignment in self.lst:
            if assignment.getDescription() == assignmentName:
                return float(assignment.getScore())
        return None

    def addAssignment(self, score: Assignment):
        #adds a score to the list
        self.lst.append(score)
        

    def changeScore(self, assignmentName: str, score: float):
        #searches for the assignmentName in the list
        #If it is found, the score is updated to score
        #If it is not found, nothing happens
        for assignment in self.lst:
            if assignment.getDescription() == assignmentName:
                assignment.score = score
                return self.lst
        return None

    def removeScore(self, assignmentName: str):
        #removes an assignment from the list if found
        #if not found, nothing happens
        for assignment in self.lst:
            if assignment.getDescription() == assignmentName:
                self.lst.remove(assignment)
                return self.lst
        return None

    def getScores(self) -> list:  
          return list(self.lst)

class Gradebook:
    def __init__(self):
        self.lst = list()
        self.gradebook = dict()
    
    def addStudent(self, student: Student):
        #adds student object to gradebook
        #(u may choose collection/data structure to represent gradebook)
        #Precondition: student is not currently in the gradebook.
        #Student ID numbers are unique- no 2 students can have same ID number
        
        for studentID in self.gradebook.keys():
            if studentID == student.getId():
                raise Exception('Student already in gradebook')
                    
        self.gradebook[student.getId()] = student
       
    
    def dropStudent(self, id: int):
        #searches for student object by ID number
        #if found, remove them from gradebook
        for studentID in self.gradebook.keys():
            if studentID == id:
                del self.gradebook[studentID]
                return self.gradebook
        return None
    
    def search(self, id: int) -> Student:
        #searches for a student using their ID number.
        #Returns the Student if found
        #if not found, does nothing.
        for studentID in self.gradebook.keys():
            if studentID == id:
                return self.gradebook[studentID]
        return None
    
    def addAssignment(self, id: int, score: Assignment):
        #adds score to a student given an id.
        #If id not found in gradebook, nothing happens.
        #If the assignment description already exists:
            #it will remove old assignment and replace with score.
        for studentID in self.gradebook.keys():
            if studentID == id:
                self.gradebook[id].addAssignment(score)
        return None

class TotalPointsGradebook(Gradebook):
    #subclass of Gradebook
    #uses the total points system of calculating grades

    def __init__(self):
        self.IdLst = list()
        self.gradebook = Gradebook().gradebook
        

    def writeGradebookRecord(self, id: int, fileName: str):
        #will write gradebook summary for single student
        try:
            file = open(fileName, 'w')
            lst = fileName.split('.')
            filesname = ".".join(lst[0:-1])
            file.write("{}\n".format(filesname))

            
            for studentID, student in self.gradebook.items():
                self.IdLst.append(studentID)    
                
            if id in self.IdLst:
                EarnedPts = 0
                TotalPts = 0

                for assignment in self.gradebook[id].getScores():
                    name = assignment.getDescription()
                    assignmentEarnedPts = assignment.getScore()
                    assignmentTotalPts = assignment.getTotal()
                    
                    fraction = "{}/{}".format(assignmentEarnedPts, assignmentTotalPts)
                        
                    EarnedPts += assignmentEarnedPts
                    TotalPts += assignmentTotalPts
                            
                    file.write("{}\n".format(name))                
                    file.write("{}\n".format(fraction))


                totalFraction = "{}/{}".format(EarnedPts, TotalPts)
                file.write("Total: {}\n".format(totalFraction))
                file.write("Percentage: {}".format(EarnedPts/TotalPts * 100)) 
                
            else:
                file.write("Student Not Found")

            file.close()
            
        except FileNotFoundError:
            return "File Not Found"
        except:
            return "Error"
        #finally:
           #file.close()



    def classAverage(self) -> float:
        #returns class percentage average for all students in gradebook
        EarnedPts = 0
        TotalPts = 0
        for student in self.gradebook.values():
            for assignment in student.getScores():
                EarnedPts += assignment.getScore()
                TotalPts += assignment.getTotal()
        avg = ((EarnedPts / TotalPts) * 100)
        return avg


class CategoryGradebook(Gradebook):
    #subclass of Gradebook
    #uses weighted category system of calculating grades
    #need to keep track of different categories & their weighted value
    
    def __init__(self):
        self.gradebook = Gradebook().gradebook
        self.Lst = list()
        self.categories = dict()
        self.records = dict()
        self.sums = list()

    def addCategory(self, description: str, weight: float):
        #adds a category to a collection
        self.categories[description] = weight
        
    
    def isBalanced(self) -> bool:
        #returns True if category weights add up to 100, false otherwise
        total = 0
        for weight in self.categories.values():
            total += weight
        if total == 100:
            return True
        return False

    def writeGradebookRecord(self, id: int, fileName: str):
        try:
            files = fileName.split('.')
            file = open(fileName, 'w')
            file.write("{}\n".format(files[0]))
            
            for name in self.gradebook.keys():
                if name == id:
                    assignment = self.gradebook[name]
                
                    for assignments in assignment.getScores():
                        category = assignments.getCategory()
                        name = assignments.getDescription()
                        earned = assignments.getScore()
                        total = assignments.getTotal()

                        heading = "{}: {}".format(category, name)
                        fraction = "{}/{}".format(earned, total)

                        file.write("{}\n".format(heading))
                        file.write("{}\n".format(fraction))

                        percentage = earned / total

                        if (self.records.get(category) is not None):
                            self.records[category] = ((self.records.get(category) + percentage) / 2)               
                        else:
                            self.records[category] = percentage
                    
            for assignment, percentage in self.records.items():
                percent = percentage * 100
                file.write("{}: {}\n".format(assignment, percent))

            suma = 0
            for category in self.records.keys():
                for name in self.categories.keys():
                    if category == name:
                        weight = self.categories[name]
                        percentage = self.records[category]
                        total = weight * percentage
                        suma += total
            file.write("Percentage: {}".format(suma))
            
            file.close()
            
        except FileNotFoundError:
            return "File Not Found"
        except:
            return "Error"
        #finally:
           #file.close()
          

    def classAverage(self) -> float:
        self.classPercents = dict()
        percent = 0
        points = collections.namedtuple('points', 'EarnedPts, TotalPts')
        section = collections.namedtuple('section', 'Category Weight')
       
        for name in self.gradebook.keys(): #ID nums, student objects
            student = self.gradebook[name]
            
            for assignment in student.getScores():
                category = assignment.getCategory()
                
                for Category, percentage in self.categories.items(): #Category, percentage
                    if Category == category:
                        key = section(Category, percentage)
                        earnedPts = assignment.getScore()
                        totalPts = assignment.getTotal()
                        value = points(earnedPts, totalPts)
                    
                        
                        if (self.classPercents.get(key) is not None):
                            earnedPoints = self.classPercents.get(key).EarnedPts + earnedPts
                            totalPoints = self.classPercents.get(key).TotalPts + totalPts
                            self.classPercents[key] = points(earnedPoints, totalPoints) 
                        else:
                            self.classPercents[key] = value
           
        for key, value in self.classPercents.items():
            weightage = key.Weight/100
            earnage = value.EarnedPts
            totalage = value.TotalPts
            fraction = earnage / totalage
            percentage = fraction * 100 * weightage
            percent += percentage

        return percent
