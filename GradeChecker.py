import sys
import json
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


def createToolbar(parent, currentPage, hasPrevious=False, hasNext=False):
    border = QFrame(parent)
    border.setGeometry(0, 0, 800, 50)
    border.setStyleSheet("border-bottom: 1px solid grey;")

    if hasNext:
        nextPage = QPushButton('Next Page', parent)
        nextPage.setGeometry(715, 10, 75, 30)
        nextPage.clicked.connect(
            lambda: widget.setCurrentIndex(currentPage + 1))

    if hasPrevious:
        previousPage = QPushButton('Previous Page', parent)
        previousPage.setGeometry(10, 10, 100, 30)
        previousPage.clicked.connect(
            lambda: widget.setCurrentIndex(currentPage - 1))

    title = QLabel('Grade Checker', parent)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setGeometry(250, 10, 300, 30)
    title.setStyleSheet("font-size:14px;")


class GradeCheckerP1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #123456;")
        createToolbar(self, 0)

        classesLabel = QLabel('Classes', self)
        classesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        classesLabel.setGeometry(250, 80, 300, 30)
        classesLabel.setStyleSheet("font-size:20px;")

        baseY = 120
        for classData in classesData['classes']:
            classBtn = QPushButton(classData, self)
            classBtn.setGeometry(300, baseY, 200, 30)
            classBtn.setStyleSheet("background-color: #185D7A;")
            classBtn.pressed.connect(
                lambda cOut=classData: self.gotoPage2(cOut))
            baseY += 40

    def gotoPage2(self, classData):
        GradeCheckerP2.editData(classData)
        widget.setCurrentIndex(1)


class GradeCheckerP2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #123456;")
        createToolbar(self, 1, True)

        self.className = QLabel(self)
        self.className.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.className.setGeometry(250, 80, 300, 30)
        self.className.setStyleSheet("font-size:20px;")

        cycleGridFrame = QFrame(self)
        cycleGridFrame.setGeometry(100, 150, 490, 230)
        # cycleGridFrame.setStyleSheet("border:1px solid white;")

        self.cycleGrid = QGridLayout(cycleGridFrame)
        self.cycleGrid.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # cycle labels
        for column in range(1, 7):
            cycleBtns = QPushButton(f'Cycle {column}', self)
            cycleBtns.setStyleSheet(
                "color: white; background-color: transparent;")
            cycleBtns.setFixedSize(70, 20)
            self.cycleGrid.addWidget(cycleBtns, 0, column)

            gradeInput = QLineEdit(self)
            gradeInput.setPlaceholderText('Grade')
            gradeInput.setStyleSheet(
                "color: white; background-color: transparent; border: 1px solid white;")
            gradeInput.setFixedSize(70, 30)
            gradeInput.setStyleSheet("text-align: center;")
            self.cycleGrid.addWidget(gradeInput, 1, column)

        for row in range(2, 6):
            semesterDetails1 = QLabel(self)
            semesterDetails1.setStyleSheet(
                "color: white; background-color: transparent;")
            semesterDetails1.setFixedSize(230, 20)
            self.cycleGrid.addWidget(semesterDetails1, row, 1)
            semesterDetails2 = QLabel(self)
            semesterDetails2.setStyleSheet(
                "color: white; background-color: transparent;")
            semesterDetails2.setFixedSize(230, 20)
            self.cycleGrid.addWidget(semesterDetails2, row, 4)

        self.assignmentsPageBtn = QPushButton('Edit Assignments', self)
        self.assignmentsPageBtn.setGeometry(600, 170, 120, 30)
        self.calculateBtn = QPushButton(f'Calculate Grade', self)
        self.calculateBtn.setGeometry(600, 205, 100, 30)

    def editData(self, currentClass):
        with open("data.txt", "r") as file:
            classesData = json.loads(file.read())
        self.className.setText(currentClass)
        for colum in range(1, 7):
            currentCycle = classesData[currentClass][f"Cycle {colum}"]
            gradeInput = self.cycleGrid.itemAtPosition(1, colum).widget()

            if len(currentCycle['Assignments']) == 0 and len(currentCycle['Assessments']) == 0:
                gradeInput.setText("--")
            else:
                gradeInput.setText(str(currentCycle["Grade"]))

        self.calculateBtn.pressed.connect(
            lambda: self.calculateSemester(currentClass))
        self.assignmentsPageBtn.pressed.connect(
            lambda: self.goToP3(currentClass))
        self.calculateSemester(currentClass)

    def calculateSemester(self, currentClass):
        cycleGrades = [int(self.cycleGrid.itemAtPosition(1, col).widget().text()) if self.cycleGrid.itemAtPosition(
            1, col).widget().text() != "--" else None for col in range(1, 7)]
        desiredSemesterPoints = 210
        creditAwarded1 = False
        creditAwarded2 = False

        actualCycles1 = 0
        totalPointsActual1 = 0
        for i in range(3):
            if cycleGrades[i] is not None:
                actualCycles1 += 1
                totalPointsActual1 += cycleGrades[i]

        remainingPoints1 = max(0, desiredSemesterPoints - totalPointsActual1)
        creditAwarded1 = remainingPoints1 <= 0

        actualCycles2 = 0
        totalPointsActual2 = 0
        for i in range(3, 6):
            if cycleGrades[i] is not None:
                actualCycles2 += 1
                totalPointsActual2 += cycleGrades[i]

        remainingPoints2 = max(0, desiredSemesterPoints - totalPointsActual2)
        creditAwarded2 = remainingPoints2 <= 0

        if totalPointsActual1 + totalPointsActual2 > 420:
            remainingPoints1 = 0
            creditAwarded1 = True
            creditAwarded2 = True

        # print("Desired Semester Points: ", desiredSemesterPoints)
        self.cycleGrid.itemAtPosition(2, 1).widget().setText(
            f"Credit Awarded: {creditAwarded1}")
        self.cycleGrid.itemAtPosition(3, 1).widget().setText(
            f"Actual Cycles: {actualCycles1}")
        self.cycleGrid.itemAtPosition(4, 1).widget().setText(
            f"Total Points from Actual Cycles: {totalPointsActual1}")
        self.cycleGrid.itemAtPosition(5, 1).widget().setText(
            f"Points Needed for Credit: {remainingPoints1}")

        self.cycleGrid.itemAtPosition(2, 4).widget().setText(
            f"Credit Awarded: {creditAwarded2}")
        self.cycleGrid.itemAtPosition(3, 4).widget().setText(
            f"Actual Cycles: {actualCycles2}")
        self.cycleGrid.itemAtPosition(4, 4).widget().setText(
            f"Total Points from Actual Cycles: {totalPointsActual2}")
        self.cycleGrid.itemAtPosition(5, 4).widget().setText(
            f"Points Needed for Credit: {remainingPoints2}")

    def goToP3(self, currentClass):
        GradeCheckerP3.editData(currentClass)
        widget.setCurrentIndex(2)


class GradeCheckerP3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lastAssignment = 0
        self.lastAssessment = 0
        self.currentClass = ''

        self.totalAvg = 0
        self.assignments = []
        self.assessments = []
        self.setStyleSheet("background-color: #123456;")
        createToolbar(self, 2, True)
        self.className = QLabel(self)
        self.className.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.className.setGeometry(250, 80, 300, 30)
        self.className.setStyleSheet("font-size:20px;")

        cycleGridFrame = QFrame(self)
        cycleGridFrame.setGeometry(200, 140, 400, 20)
        # cycleGridFrame.setStyleSheet("border: 1px solid white;")

        self.cycleGrid = QGridLayout(cycleGridFrame)
        self.cycleGrid.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.cycleGrid.setContentsMargins(0, 0, 0, 0)

        # cycle labels
        for column in range(1, 7):
            cycleBtns = QPushButton(f'Cycle {column}', self)
            cycleBtns.setStyleSheet(
                "color: white; background-color: transparent;")
            cycleBtns.setFixedSize(60, 20)
            self.cycleGrid.addWidget(cycleBtns, 0, column)

        assignmentsLabel = QLabel('Assignments', self)
        assignmentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        assignmentsLabel.setStyleSheet("font-size: 15px")
        assignmentsLabel.setGeometry(50, 170, 185, 30)
        self.assignmentsGridFrame = QFrame(self)
        self.assignmentsGrid = QGridLayout(self.assignmentsGridFrame)
        self.assignmentsGrid.setContentsMargins(0, 0, 0, 0)
        self.assignmentsGrid.setSpacing(0)
        addBtnAssignment = QPushButton('Add Assignment', self)
        addBtnAssignment.setGeometry(50, 210, 185, 30)
        addBtnAssignment.pressed.connect(lambda: self.addAssignment())
        
        assessmentsLabel = QLabel('Assessments', self)
        assessmentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        assessmentsLabel.setStyleSheet("font-size: 15px")
        assessmentsLabel.setGeometry(307, 170, 185, 30)
        self.assessmentsGridFrame = QFrame(self)
        self.assessmentsGridFrame.setGeometry(307, 240, 185, 30)
        self.assessmentsGrid = QGridLayout(self.assessmentsGridFrame)
        self.assessmentsGrid.setContentsMargins(0, 0, 0, 0)
        self.assessmentsGrid.setSpacing(0)
        addBtnAssessments = QPushButton('Add Assessments', self)
        addBtnAssessments.setGeometry(307, 210, 185, 30)
        addBtnAssessments.pressed.connect(lambda: self.addAssessments())
        
        calculateLabel = QLabel("Grades", self)
        calculateLabel.setGeometry(564, 170, 185, 30)
        calculateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calculateLabel.setStyleSheet("font-size: 15px")
        calculateBtn = QPushButton('Calculate', self)
        calculateBtn.setGeometry(564, 210, 92, 30)
        calculateBtn.pressed.connect(lambda: self.calculateGrades())
        
        self.assignmentsGrade = QLabel('Assignments: ', self)
        self.assignmentsGrade.setGeometry(564, 240, 180, 30)
        self.assignmentsGrade.setStyleSheet("font-size: 13px")
        
        self.assessmentsGrade = QLabel('Assessments: ', self)
        self.assessmentsGrade.setGeometry(564, 270, 180, 30)
        self.assessmentsGrade.setStyleSheet("font-size: 13px")
        
        self.totalAvgGrade = QLabel('Total Average: ', self)
        self.totalAvgGrade.setGeometry(564, 300, 180, 30)
        self.totalAvgGrade.setStyleSheet("font-size: 13px")
        
        self.saveBtn = QPushButton('Save', self)
        self.saveBtn.setGeometry(656, 210, 92, 30)
     
    def editData(self, currentClass):
        with open("data.txt", "r") as file:
            classesData = json.loads(file.read())
        self.className.setText(currentClass)
        self.cycleGrid.itemAtPosition(0, 1).widget().setStyleSheet("color: back; background-color: white;")
        for column in range(1, 7):
            self.cycleGrid.itemAtPosition(0, column).widget().pressed.connect(lambda cOut=column: self.changeTab(cOut, currentClass))
        self.editAssignments(1, currentClass)
        self.editAssessments(1,currentClass)
        self.currentClass = currentClass
        self.calculateGrades()
        self.saveBtn.pressed.connect(lambda: self.saveData(1))

    def changeTab(self, btnIndex, currentClass):
        for column in range(1, 7):
            if column != btnIndex:
                self.cycleGrid.itemAtPosition(0, column).widget().setStyleSheet("color: white; background-color: transparent;")
        self.cycleGrid.itemAtPosition(0, btnIndex).widget().setStyleSheet("color: back; background-color: white;")
        self.editAssignments(btnIndex,currentClass)
        self.editAssessments(btnIndex,currentClass)
        self.calculateGrades()
        self.saveBtn.pressed.connect(lambda: self.saveData(btnIndex))
    
    def editAssignments(self, btnIndex, currentClass):
        self.lastAssignment = 0
        for widget in range(0,9):
            try:
                if self.assignmentsGrid.itemAtPosition(widget,1).widget().metaObject().className() == 'QLineEdit':
                    self.assignmentsGrid.removeWidget(self.assignmentsGrid.itemAtPosition(widget,1).widget())                    
            except:
                pass
            
        self.assignmentsList = classesData[currentClass][f'Cycle {btnIndex}']['Assignments']
        self.lastAssignment = len(self.assignmentsList) + 1
        for index, assignment in enumerate(self.assignmentsList):
            assignmentGrade = QLineEdit(str(assignment), self)
            assignmentGrade.setAlignment(Qt.AlignmentFlag.AlignCenter)
            assignmentGrade.setStyleSheet("border: 1px solid grey;")
            assignmentGrade.setFixedSize(180, 30)
            self.assignmentsGrid.addWidget(assignmentGrade, index, 1)
        self.assignmentsGridFrame.setGeometry(50, 240, 185, len(self.assignmentsList)*30)

    def addAssignment(self):
        if self.lastAssignment + 1 < 10:
            assignmentGrade = QLineEdit(self)
            assignmentGrade.setAlignment(Qt.AlignmentFlag.AlignCenter)
            assignmentGrade.setStyleSheet("border: 1px solid grey;")
            assignmentGrade.setFixedSize(180, 30)
            self.assignmentsGrid.addWidget(assignmentGrade, self.lastAssignment+1, 1)
            self.assignmentsGridFrame.setGeometry(50, 240, 185, (self.lastAssignment)*30)
            self.lastAssignment += 1
    
    def editAssessments(self,btnIndex,currentClass):
        self.lastAssessments = 0
        for widget in range(0,9):
            try:
                if self.assessmentsGrid.itemAtPosition(widget,1).widget().metaObject().className() == 'QLineEdit':
                    self.assessmentsGrid.removeWidget(self.assessmentsGrid.itemAtPosition(widget,1).widget())                    
            except:
                pass
        
        self.assessmentsList = classesData[currentClass][f'Cycle {btnIndex}']['Assessments']
        self.lastAssessment = len(self.assessmentsList)
        for index, assessments in enumerate(self.assessmentsList):
            assessmentsGrade = QLineEdit(str(assessments), self)
            assessmentsGrade.setAlignment(Qt.AlignmentFlag.AlignCenter)
            assessmentsGrade.setStyleSheet("border: 1px solid grey;")
            assessmentsGrade.setFixedSize(180, 30)
            self.assessmentsGrid.addWidget(assessmentsGrade, index, 1)
        self.assessmentsGridFrame.setGeometry(307, 240, 185, len(self.assessmentsList)*30)
    
    def addAssessments(self):
        if self.lastAssessment + 1 < 9:
            assessmentsGrade = QLineEdit( self)
            assessmentsGrade.setAlignment(Qt.AlignmentFlag.AlignCenter)
            assessmentsGrade.setStyleSheet("border: 1px solid grey;")
            assessmentsGrade.setFixedSize(180, 30)
            self.assessmentsGrid.addWidget(assessmentsGrade, self.lastAssessment + 1, 1)
            self.assessmentsGridFrame.setGeometry(307, 240, 185, (self.lastAssessment + 1) * 30)
            self.lastAssessment += 1

    def calculateGrades(self):
        assignmentsWeight = int(classesData[self.currentClass]['Percent']['Assignments'])
        assessmentsWeight = int(classesData[self.currentClass]['Percent']['Assessments'])
        self.assignments = []
        self.assessments = []
        for widget in range(0,10):
            try:
                self.assignments.append(int(self.assignmentsGrid.itemAtPosition(widget,1).widget().text()))
                self.assessments.append(int(self.assessmentsGrid.itemAtPosition(widget,1).widget().text()))
            except:
                pass
        assignmentsAvg = int(sum(self.assignments)/len(self.assignments))
        assessmentsAvg = int(sum(self.assessments)/len(self.assessments))
        self.totalAvg = int((sum(self.assignments) / len(self.assignments) * (assignmentsWeight / 100)) + sum(self.assessments) / len(self.assessments) * (assessmentsWeight / 100))
        self.assignmentsGrade.setText(f'Assignments: {assignmentsAvg}')
        self.assessmentsGrade.setText(f'Assessments: {assessmentsAvg}')
        self.totalAvgGrade.setText(f'Total Average: {self.totalAvg}')
        
    def saveData(self, currentCycle):
        print(currentCycle)
        classesData[self.currentClass][f'Cycle {currentCycle}']['Grade'] = self.totalAvg
        classesData[self.currentClass][f'Cycle {currentCycle}']['Assignments'] = self.assignments
        classesData[self.currentClass][f'Cycle {currentCycle}']['Assessments'] = self.assessments
        with open('data.txt', 'w') as dataFile:
            json.dump(classesData, dataFile)
        
if __name__ == '__main__':
    with open("data.txt", "r") as file:
        classesData = json.loads(file.read())
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icons/window-icon.svg'))
    widget = QStackedWidget()
    GradeCheckerP1 = GradeCheckerP1()
    GradeCheckerP2 = GradeCheckerP2()
    GradeCheckerP3 = GradeCheckerP3()
    widget.addWidget(GradeCheckerP1)
    widget.addWidget(GradeCheckerP2)
    widget.addWidget(GradeCheckerP3)
    widget.setFixedSize(800, 600)
    widget.setWindowTitle('Grade Checker - Nagra')
    widget.show()
    sys.exit(app.exec())
