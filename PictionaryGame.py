import sys
import csv, random
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QWidget


class Player:
    '''
        for initialising an instance of player
    '''
    def __init__(self, name, score=0):
        self.playerName = name  # to store player's name
        self.score = score  # to store player's score


class GameState:
    '''
        for initialising the state of the game.
    '''
    def __init__(self,
                 isGameRunning,
                 playerOne,
                 playerTwo,
                 currentGuessWord,
                 currentGuesser=None,
                 currentDrawer=None,
                 ):
        self.isGameRunning = isGameRunning  #to determine if the game has started
        self.playerOne = playerOne  # instance of player for player1
        self.playerTwo = playerTwo  # instance of player for player2
        self.currentGuessWord = currentGuessWord # current guess word
        self.currentDrawer = currentDrawer  # player who's in the drawing role in this round
        self.currentGuesser = currentGuesser # player who's in the guessing role in this round


class MainMenu(QWidget):
    '''
        Game main menu UI
    '''

    initRelativePath = "PuiKwan_CHIEW_3132438_Ass2/code/" #to handle the relative path of the assets

    def __init__(self):
        super().__init__()  
        self.init_ui() # initialise ui function

    def init_ui(self):
        '''
            Main menu window of the application
             - users key in their player name and select the mode of game in this window
        '''
        layout = QVBoxLayout(self) # sets the parent layout of the main menu
        self.setStyleSheet('font-size:16px;')  # sets the font size of the window

        # Labels and styling
        label = QLabel("Pictionary Game") # Sets the label of main window
        label.setAlignment(Qt.AlignmentFlag.AlignCenter) # aligns the label center
        label.setStyleSheet('font-size:32px; font-weight:bold') # sets the font style of the label
        layout.addWidget(label) # adds label to main menu layout

        # Icon and styling
        layout.addSpacing(15)  # adds spacing
        icon = QLabel() #  creates an instnace of Qlabel for an icon
        mainIcon = QPixmap(self.initRelativePath + "icons/kitty.png") # sets an icon for the label
        icon.setPixmap(mainIcon.scaled(180, 180)) #resize the icon 
        icon.setAlignment(Qt.AlignmentFlag.AlignHCenter) # aligns the icon center
        layout.addWidget(icon)  # adds label to main menu layout

        # Label for instruction to start game
        layout.addSpacing(15) # adds spacing

        # sets a label instructions in the main window
        instructions = QLabel( "Note: Key in player's name and select game mode to start. \nDefault names are Player 1 & Player 2")
        instructions.setStyleSheet("font-size:12px; padding:2px;") # set style for the instruction label
        instructions.setAlignment(Qt.AlignmentFlag.AlignHCenter) # aligns the instruction to center
        layout.addWidget(instructions) # adds the intruction to the layout

        # Field to input player's name
        self.playersName = QFormLayout()  # sets a child Form layout to main menu (for user input's field )
        self.player1 = QLineEdit()  # Input field for player 1's name
        self.player1.setMinimumWidth(300) # sets a min width of 300 for the input widget
        self.player1.setStyleSheet('padding: 5px')  # sets a padding for the input widget
        self.player2 = QLineEdit() # Input field for player 2's name
        self.player2.setMinimumWidth(300)  # sets a min width of 300 for the input widget
        self.player2.setStyleSheet('padding: 5px') # sets a padding for the input widget
        self.playersName.addRow("Player 1's name: ", self.player1) # adds both input widget form layout
        self.playersName.addRow("Player 2's name: ", self.player2)
        layout.addLayout(self.playersName) # add the Form Layout to the parent layout of the main window

        # Game mode Button Section
        buttonsGrid = QGridLayout() # sets a child grid layout of the main menu (for the game mode button)
        easy_button = QPushButton("Easy Mode", self) # instantiate a button  with label 'easy mode'
        easy_button.setStyleSheet('padding: 15px') # stylise the button with padding
        easy_button.clicked.connect(self.start_game_easy) # connects to the event handler of the button
        #   easy button
        hard_button = QPushButton("Hard Mode", self) # instantiate a button with label 'hard mode'
        hard_button.setStyleSheet('padding: 15px') # stylise the button with padding
        hard_button.clicked.connect(self.start_game_hard) # connects to the event handler of the button
        #   hard button
        buttonsGrid.addWidget(easy_button, 0, 0)    # adds button to the child Grid layout with position specified
        buttonsGrid.addWidget(hard_button, 0, 1)
        layout.addLayout(buttonsGrid)       # add the child GridLayout to the parent Layout 

        # set window title
        self.setWindowTitle("Pictionary Game - Main Menu")
        self.setGeometry(100, 100, 400, 300)

    def start_game_easy(self):
        """
        Function that handles and invoke easy mode of the game
            - calls start_game method and pass in a string "easy" as an argument
        """
        self.start_game("easy")

    def start_game_hard(self):
        """
        Function that handles and invoke hard mode of the game
            - calls start_game method and pass in a string "hard" as an argument
        """
        self.start_game("hard")

    def start_game(self, mode):
        """
        Function that starts the game corresponding to the mode selecte
        Args:
            mode (str): user's selected game mode
        """
        # closes the main window opens up another window which starts the pictionary game. 
        self.game_window = PictionaryGame(mode, self.player1.text(), self.player2.text()) 
        self.game_window.show()
        self.close()


class PictionaryGame(QMainWindow):
    '''
        Painting Application class
    '''
    
    initRelativePath = "PuiKwan_CHIEW_3132438_Ass2/code/" #to handle the relative path of the assets

    # constructor
    def __init__(self, mode, player1Name, player2Name): 
        # instantiate 2 players
        if not player1Name.strip(): # initialise name of the player, if empty or user input is blank
            playerOne = Player("Player 1") # default name is set as "Player 1"
        else:
            playerOne = Player(player1Name) 

        if not player2Name.strip():
            playerTwo = Player("Player 2")  # default name is set as "Player 2"
        else:
            playerTwo = Player(player2Name)

        # instantiate game's state
        self.gameState = GameState(
            False,
            playerOne,
            playerTwo,
            '')

        super().__init__()
        self.mode = mode   #initialise the mode of the game selected by player
        self.gameState.currentGuessWord = "" # initialise the guess word to be empty
        # self.guessWordWindow = None #hide the show word window

        self.init_ui()

    def init_ui(self):
        # set window title according to the mode chosen.
        self.setWindowTitle(f"Pictionary Game - {self.mode.title()} Mode") # sets the title of the window with the game mode
        self.setStyleSheet("font-size:16px;") # sets the font size of the window

        # set the windows dimensions
        top = 200
        left = 200
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(QIcon(self.initRelativePath + "icons/kitty.png"))
        # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop
        # mac version - not yet working
        self.setWindowIcon(QIcon(QPixmap(self.initRelativePath + "icons/kitty.png")))

        # image settings (default)
        self.image = QPixmap(
            self.initRelativePath + "icons/canvas.png")  # documentation: https://doc.qt.io/qt-6/qpixmap.html
        self.image.fill(Qt.GlobalColor.white)  # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        # mainWidget = QWidget()
        # mainWidget.setMaximumWidth(300)

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(" File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size")  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Colour")  # add the "Brush Colour" menu to the menu bar
        otherspMenu = mainMenu.addMenu(" Others") # add others menu to the menu bar

        # Help menu
        helpAction = QAction(QIcon(self.initRelativePath + "icons/help.png"), "Help", self)  # create a help action with a png as an icon
        helpAction.setShortcut("Ctrl+H")  # connect this help action to a keyboard shortcut
        otherspMenu.addAction(helpAction)  # add the help action to the file menu
        helpAction.triggered.connect(self.help)

        # About menu
        aboutAction = QAction(QIcon(self.initRelativePath + "icons/about.png"), "About", self)  # create a about action with a png as an icon
        aboutAction.setShortcut("Ctrl+A")  # connect this about action to a keyboard shortcut
        otherspMenu.addAction(aboutAction)  # add the about action to the file menu
        aboutAction.triggered.connect(self.about)

        # Open menu
        openAction = QAction(QIcon(self.initRelativePath + "icons/open.png"), "Open",
                             self)  # create a open action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        openAction.setShortcut(
            "Ctrl+O")  # connect this open action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(
            openAction)  # add the open action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        openAction.triggered.connect(self.open)

        # save menu item
        saveAction = QAction(QIcon(self.initRelativePath + "icons/save.png"), "Save",
                             self)  # create a save action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        saveAction.setShortcut(
            "Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(
            saveAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        saveAction.triggered.connect(
            self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon(self.initRelativePath + "icons/clear.png"), "Clear",
                              self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(
            self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # end game
        endAction = QAction(QIcon(self.initRelativePath + "icons/exit.png"), "Exit",
                            self)  # create a clear end & exit action with a png as an icon
        endAction.setShortcut("Ctrl+E")  # connect this end & exit action to a keyboard shortcut
        fileMenu.addAction(endAction)  # add this action to the file menu
        endAction.triggered.connect(self.end_game)

        # brush thickness
        threepxAction = QAction(QIcon(self.initRelativePath + "icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon(self.initRelativePath + "icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon(self.initRelativePath + "icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon(self.initRelativePath + "icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon(self.initRelativePath + "icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction)
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon(self.initRelativePath + "icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction)
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon(self.initRelativePath + "icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon(self.initRelativePath + "icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellow)

        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        # widget inside the Dock
        self.playerInfo = QWidget() 
        self.vbdock = QVBoxLayout()
        self.playerInfo.setLayout(self.vbdock) #sets layout for the dock
        self.playerInfo.setMaximumSize(200, self.height()) #sets the width of the docl to 200px
        # add controls to custom widget
        self.turnLabel = QLabel(" Game not started ")  # label to show whose turn to draw
        self.turnLabel.setStyleSheet("font-weight: bold") # set the label to bold
        self.vbdock.addWidget(self.turnLabel) # turn label add to dock
        self.vbdock.addSpacing(30) # adds spacer

        scoresLayout = QGridLayout()    # layout of the scores section

        scoresLabel = QLabel("Scores:") # Scores label
        scoresLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter) # aligns the cores label to center
        scoresLabel.setStyleSheet("text-decoration:underline; font-weight: bold;") # bolds & underline the score label

        self.playerOnescoreLabel = QLabel(str(self.gameState.playerOne.score)) # display the scores of the players
        self.playerTwoscoreLabel = QLabel(str(self.gameState.playerTwo.score))

        scoresLayout.addWidget(scoresLabel, 0, 0, 1, 3) #add the label to the frst row of the layout, spanning 3 column
        scoresLayout.addWidget(QLabel(self.gameState.playerOne.playerName + " : "), 1, 0) #display player 1's name on the second row.
        scoresLayout.addWidget(self.playerOnescoreLabel, 1, 1)  # diplay the score for player 1 inline with the name
        self.player1crown = QLabel()    #set and display a crown for the current highest score player
        scoresLayout.addWidget(self.player1crown, 1, 2) # crown displayed inline with player's name

        scoresLayout.addWidget(QLabel(self.gameState.playerTwo.playerName + " : "), 2, 0) #display player 2's name on the second row of the layout
        scoresLayout.addWidget(self.playerTwoscoreLabel, 2, 1) # diplay the score for player 2 inline with the name
        self.player2crown = QLabel() #set and display a crown for the current highest score player
        scoresLayout.addWidget(self.player2crown, 2, 2) # crown displayed inline with player's name

        self.vbdock.addLayout(scoresLayout) # add the score board to dock

        # countdown timer section
        self.vbdock.addSpacing(30) # add spacing
        self.remaining_time = 60    # set the limit timer to 60 seconds
        self.timer = QTimer()   # create a qtimer object
        self.timer_label = QLabel("Time Left: - ") #label to display remaining time
        self.timer.timeout.connect(self.update_timer) # connects to event handler
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter) #align label to center
        self.vbdock.addWidget(self.timer_label) # add widget to dock


        # set guess history section
        self.vbdock.addSpacing(30) #add spacing
        history_label = QLabel("Previous Tries:") #label for the section
        history_label.setStyleSheet("text-decoration: underline; font-weight:bold") #underlines and bold the label 
        self.vbdock.addWidget(history_label) #add widget to dock

        self.history_text = QTextEdit() #the text field to display previous incorrect gueese
        self.history_text.setReadOnly(True) # this field is non editable
        self.vbdock.addWidget(self.history_text) # add widget to dock

        # User enter guess
        self.guess_input_label = QLabel("Enter your Guess:") #label for the field
        self.guess_input_label.setStyleSheet("text-decoration: underline;font-weight:bold") #underlines and bold the label 
        self.vbdock.addWidget(self.guess_input_label) # add widget to dock
        self.guess_input = QLineEdit() # user input field to guess the word
        # allow user to press enter, thn call the self.check_guess function
        self.guess_input.returnPressed.connect(self.check_guess)
        self.vbdock.addWidget(self.guess_input)


        # set widget for dock
        self.dockInfo.setWidget(self.playerInfo)

        # set skip turn button
        self.vbdock.addSpacing(30) #adds spacing
        self.vbdock.addStretch(1)
        skip_turn_button = QPushButton("Skip Turn")
        skip_turn_button.setShortcut("Ctrl+N") # sets shortcut key for skip button
        skip_turn_button.clicked.connect(self.skip_turn) # connect button to  event handlers
        self.vbdock.addWidget(skip_turn_button) #add button to dock

        # set a toggle button button
        self.toggle_button = QPushButton(self) 
        self.updateToggleButton() # connects to the function determine the start/end button via the gamestate.isGameRunning::Bool
        self.vbdock.addWidget(self.toggle_button) 
        self.toggle_button.clicked.connect(self.toggleGame) # fires the event handler for the button

        # Setting colour of dock to gray
        self.playerInfo.setAutoFillBackground(True) 
        p = self.playerInfo.palette() 
        p.setColor(self.playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        self.playerInfo.setPalette(p)

        # status bar
        self.status_bar = self.statusBar() #sets a status bar

        # Display the a message with 5 seconds timeout
        self.status_bar.showMessage('Ready', 5000)

        # Gets word from the txt file
        self.getList(self.mode)

    # event handlers
    def setScoreToLabel(self):
        '''
            Handles the scoreboard of the game window. 
        '''
        # displays the score of the respective players in the scoreboard
        self.playerOnescoreLabel.setText(str(self.gameState.playerOne.score)) 
        self.playerTwoscoreLabel.setText(str(self.gameState.playerTwo.score))

    def update_timer(self):
        '''
            updates the timer, trickled down every second from 60.
        '''
        if (self.remaining_time > 0):   # when there is still time 
            self.timer_label.setText(f"Time Left: {self.remaining_time}s")  # print out the current remaining time
            self.remaining_time -= 1 # reduce the timer by 1 (second)

        if self.remaining_time <= 0: # when time runs out
            self.timer.stop()   #stoped the timer widget

            timeoutMsg = QMessageBox()  # instantiate a message box to display time out message
            timeoutMsg.setIconPixmap(QPixmap(self.initRelativePath + "/icons/time-out.png"))  # sets the icon for the message box
            timeoutMsg.setText("Ran out of time!")  # display the message
            timeoutMsg.setWindowTitle("Time's Out")  # sets the tile of the pop up box
            timeoutMsg.setStandardButtons(QMessageBox.StandardButton.Ok)  # message standard ok button
            timeoutMsg.exec() # executes the timeout message box
            self.skip_turn()    # proceed to the next round

    def skip_turn(self):
        '''
            Handles the skipping the current turn of the player
                - this function will only execute the lines if the game has started
                  else it would do nothing.
        '''
        if self.gameState.isGameRunning: # if the game has started
            self.timer.stop    # stop the timer widget
            self.remaining_time = 60    # reset the remaining time to 60 
            self.status_bar.showMessage('Skipped a turn!', 5000) # display a status bar message indicating turn skipping - timeout 5 seconds
            self.clearInputandGuessHistory()
            self.startGame() # continue with the game

    def updateToggleButton(self):
        '''
            Handles the toggle button.
            Displays either an end/ start game button. 
             - Start Game is displayed if the game has not started. 
             - End Game is displayed if the game has started
        '''
        # Set button text and connect it to the appropriate function based on game state

        try:
            self.toggle_button.clicked.disconnect()  # Disconnect previous connection
        except Exception:
            pass

        if self.gameState.isGameRunning: # if the game has started
            self.toggle_button.setText('End Game') # sets the button label to 'end game'
            self.toggle_button.clicked.connect(self.stopGame) # connect the button to end game event handler
        else:                                           # if the game has not started
            self.toggle_button.setText('Start Game') # set the button label to 'start game'
            self.toggle_button.clicked.connect(self.startGame) # connect button to start game event handler 

    def toggleGame(self):
        '''
            Function to toggle between start and stop game events
        '''
        if self.gameState.isGameRunning: # if the has started
            self.stopGame() # the toggle button will call stop game function to handle the event
        else:                   # if the game was not started
            self.startGame() # the toggle button will call start game function to handle the event

    def setPlayer(self):
        '''
            Handled the assignment of player to who shall be a guesser / drawer.
            Returns None after assignment.
        '''
        # when the game has just started where the two roles are None
        if self.gameState.currentDrawer is None and self.gameState.currentGuesser == None:
            self.gameState.currentDrawer = self.gameState.playerOne # drawer is set to be player 1
            self.gameState.currentGuesser = self.gameState.playerTwo # guesser is set to be player 2
            return None

        # when the game has already started, switch the roles of the players
        if self.gameState.currentDrawer.playerName == self.gameState.playerOne.playerName: 
            self.gameState.currentDrawer = self.gameState.playerTwo
            self.gameState.currentGuesser = self.gameState.playerOne
            return None
        else:
            self.gameState.currentDrawer = self.gameState.playerOne
            self.gameState.currentGuesser = self.gameState.playerTwo
            return None    

    def startGame(self):
        '''
            Function to handle the start game event
        '''
        if self.gameState.isGameRunning is False:
            self.status_bar.showMessage('Game Started!', 5000) # Display game started at the status bar
        self.gameState.isGameRunning = True # sets the game state to be true
        self.gameState.currentGuessWord = self.getWord() # gets a random word from the list
        self.clear()     # clears the drawing panel
        self.setPlayer() # sets the player role either to guesser / drawer
        self.updateToggleButton()   # updated toggle button to either "end game"
        self.guess_input.setFocus()
        self.timer.start(1000) # starts the Qtimer to timeout every second hence it will call the update_timer function to update the label
        self.currentDrawer = str(self.gameState.currentDrawer.playerName) # converts the player's name to string
        self.currentGuesser = str(self.gameState.currentGuesser.playerName) 
        self.turnLabel.setText(str(self.currentDrawer+"'s turn to draw!")) # display the label to show the current drawer
        self.guess_input_label.setText(str(self.currentGuesser+"'s guess :")) # display the label to show the current guesser
        self.guessWordWindow = ShowGuessWordWindow(self.gameState.currentGuessWord, self) # initiate the display of the guess word window
        self.guessWordWindow.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True) 
        self.setDisabled(True) # momentarily disable the game window
        self.guessWordWindow.show() # display the guess word to the drawer

    def stopGame(self):
        '''
            Function to handle the stop game event
        '''
        self.gameState.isGameRunning = False # sets the flag to false
        self.updateToggleButton() # update the toggle button
        self.status_bar.showMessage('Game Ended', 5000) # display a status bar message to notify game has ended - timeout 5 seconds
        self.end_game() # calls the end game method to handle end game event

    answersList = []    # a list to store the previous guesses 

    def check_guess(self):
        '''
            Handles the word guess from user input
             - correct guess grants guesser 1 score & drawer with 2
        '''
        if self.gameState.isGameRunning:
            guess = self.guess_input.text().strip().lower() # gets the user input trimmed & lowercased
        
            if guess == self.gameState.currentGuessWord.lower(): # if the word matches; proceed to display  message
                correctMsg = QMessageBox()  
                correctMsg.setIconPixmap(QPixmap(self.initRelativePath + "/icons/happy-cat.png"))  # sets the icon for the message box
                correctMsg.setText("Your guess is correct!")  # display the congratulatory text
                correctMsg.setWindowTitle("Correct")  # sets the tile of the pop up box
                correctMsg.setStandardButtons(QMessageBox.StandardButton.Ok)  # message standard ok button
                correctMsg.exec()
                self.clearInputandGuessHistory()    # calls function to clear input & incorrect guess history widget
                self.gameState.currentGuesser.score += 1   # add score  to guesser
                self.gameState.currentDrawer.score += 2    # add score  to guesser 
                self.setScoreToLabel()  # sets score to the scoreboard label
                self.check_score_display_crown()    # display a crown icon for the player with leading score
                self.startGame()    # continue the game
            else:
                wrongMessage = QMessageBox()
                wrongMessage.setIconPixmap(QPixmap(self.initRelativePath + "/icons/collar-of-shame.png"))  # sets the icon for the message box
                wrongMessage.setText("Your guess is incorrect :(")  # display the message
                wrongMessage.setWindowTitle("Wrong Guess")  # sets the tile of the pop up box
                wrongMessage.setStandardButtons(QMessageBox.StandardButton.Ok)  # message standard ok button
                wrongMessage.exec()

                self.answersList.append(self.guess_input.text().strip())   # appends the current incorrect guess to the set
                self.displayAns = ""            # clears the previous string value
                for i in self.answersList:      # iterates the previous incorrect guesses and place into a string
                    self.displayAns = self.displayAns + i + "\n"   
                self.history_text.clear()       # clears the output widget
                self.history_text.setText(self.displayAns)  # display the string of incorrrect guesses with the updated info
                self.guess_input.clear()        # clears the input widget

    def check_score_display_crown(self):
        '''
            Determine if a crown icon will be showed.
             - Crown icon displayed for the leading score player in the scoreboard
        '''
        if self.gameState.playerOne.score ==  self.gameState.playerTwo.score: 
            return # if the score is a tie, do nothing

        if self.gameState.playerOne.score > self.gameState.playerTwo.score: # display crown for player 1 if the score is higher thn player 2
            self.player1crown.setPixmap(QPixmap(self.initRelativePath + "icons/crown.png").scaled(18, 18))
            self.player2crown = QLabel("")  
            return
        
        if self.gameState.playerTwo.score > self.gameState.playerOne.score: # display crown for player 1 if the score is higher thn player 2
            self.player1crown = QLabel("") 
            self.player2crown.setPixmap(QPixmap(self.initRelativePath + "icons/crown.png").scaled(18, 18))
            return

    def end_game(self):
        '''
            to handle end game button
        '''
        self.timer.stop()   #stops the timer
        self.status_bar.showMessage('Game Ended!', 5000) #display a status bar message
        self.show_winner_dialog() # shows an end game dialog box
        self.close()    #close the window

    def determine_winner(self):
        '''
            Determine player that have higher scores win.

            Return String / None
        '''
        if self.gameState.playerOne.score == self.gameState.playerTwo.score:    #if the score is a tie, return None
            return None

        if self.gameState.playerOne.score > self.gameState.playerTwo.score: # get the name of the highest score player
            winner = str(self.gameState.playerOne.playerName)
        else:
            winner = str(self.gameState.playerTwo.playerName)
            
        return winner # return the name of the highest score player

    def show_winner_dialog(self):
        '''
            display a pop up message to congratulate winner!
        '''
        winner = self.determine_winner()
        msg = QMessageBox()
        if winner is not None:
            msg.setIconPixmap(QPixmap(self.initRelativePath + "/icons/trophy.png"))  # sets the icon for the message box
            msg.setText("Congratulations, " + winner+ "! You are the winner!")  # display the congratulatory text
        else:
            msg.setIconPixmap(QPixmap(self.initRelativePath + "/icons/tie.png"))  # sets the icon for the message box
            msg.setText("It's a tie! You both did great!")  # display the congratulatory text
        msg.setWindowTitle("Game Over")  # sets the tile of the pop up box
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)  # message standard ok button
        msg.exec()

    def clearInputandGuessHistory(self):
        '''
            Clearing the guess word input widget and the widget to display previous incorrect guess
        '''
        self.history_text.clear()   # clear the previous guesses
        self.guess_input.clear()    # clear the input field
        self.answersList.clear()    # clear the temporary array to store the previous guesses

    # event handlers for mouse painting
    def mousePressEvent(self,
                        event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            # print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(self,
                       event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint,
                             event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self,
                          event):  # when the mouse is released, documentation: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button, documentation: https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(
            self)  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(QPoint(),
                                 self.image)  # draw the image , documentation: https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(
            Qt.GlobalColor.white)  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.GlobalColor.black

    def red(self):
        self.brushColor = Qt.GlobalColor.red

    def green(self):
        self.brushColor = Qt.GlobalColor.green

    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow

    # Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        return randomWord

    # read word list from file
    def getList(self, mode):
        with open(self.initRelativePath + mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.wordList = row
                line_count += 1

    # help window of the application
    def help(self):
        '''
        Handles Help menu item
         - opens a pop up box and display info about the app
        '''
        ""
        help_content = """
        Welcome to Pictionary Game!

        How to Play: 
            - Pictionary is a drawing and guessing game. 
            - Players take turns drawing a word or phrase while the other tries to guess what it is.
            - A pop up message will show the the guess word ONCE to the designated drawer. Click reveal button in the window to display/hide word
            - Refer the label of the top of dock for who is the drawer. 
            - Guesser will need to key in their word of guess at the input field in the middle of the dock
            - Previous incorrect guesses can be referred in the dock.
   
        Game Controls:
            - Drawing Tools: Use the mouse to draw.
            - Brush: Click or tap to select different colors. (Refer shortcut keys in menu tab)
            - Clear: Clear to erase your drawing and start over (Ctrl+C)

        Rules:
            - Each player takes turns drawing/guessing a randomized word for 60 seconds limit. 
            - No letters, numbers, or verbal hints allowed.

        Scoring:
            - Each correct guess earns drawer 2 points and guesser with 1 points. Highest score player wins!
            - Scoreboard is in the dock

        Have fun playing!
        """
        helpMsg = QMessageBox()

        helpMsg.setIconPixmap(QPixmap(self.initRelativePath + "/icons/kitty.png"))  # sets the icon for the message box
        helpMsg.setText(help_content)  # display the content
        helpMsg.setStandardButtons(QMessageBox.StandardButton.Ok)  # message standard ok button
        helpMsg.exec()

    # about window of the application
    def about(self):
        '''
        Handles About menu item
         - opens a pop up box and display info about the app
        '''
        about_content = """
        About Pictionary:
        Pictionary is a classic drawing and guessing game where players use their artistic skills to convey words or phrases to the other player to make a guess.
      
        Developed by Florryn Chiew 2023
       
        Credits:
        - UIcons by Flaticon @ https://www.flaticon.com/uicons
        """
        aboutMsg = QMessageBox()

        aboutMsg.setIconPixmap(QPixmap(self.initRelativePath + "/icons/kitty.png"))  # sets the icon for the message box
        aboutMsg.setText(about_content)  # display the content
        aboutMsg.setStandardButtons(QMessageBox.StandardButton.Ok)  # message standard ok button
        aboutMsg.exec()

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class

class ShowGuessWordWindow(QWidget):
    '''
        A widget to handle the pop up window to  show the guess word 
    '''
    def __init__(self, guessWord, parentWindow):
        self.guessWord = guessWord  # get the guess word from the calling window
        self.parentWindow = parentWindow    
        currentDrawPlayerName = self.parentWindow.gameState.currentDrawer.playerName # gets the current drawer's player name
        
        super().__init__() # initialise this class  
        self.hiddenText = "*************"     # hidden text
        self.isTextHidden = True              # boolean flag for hidden guess word
        self.setStyleSheet('font-size:16px;') # sets the font size of the window

        layout = QVBoxLayout()  # layout for the components inside in window
        self.titleOneLabel = QLabel(f'Hi, {currentDrawPlayerName}! \n\nHere is your word!') # display label to indicate player designated for
        self.guessWordLabel = QLabel(self.hiddenText) # display hidden text
        self.revealButton = QPushButton('Reveal/Hide Word') #button to reveal the word
        self.revealButton.clicked.connect(self.revealWord)  # fires the event handler to reveal the hidden word
        layout.addWidget(self.titleOneLabel)    # add widgets to layout
        layout.addWidget(self.guessWordLabel)
        layout.addWidget(self.revealButton)

        self.setLayout(layout)  # set the window's layout
        self.setFixedSize(200, 200)

    def revealWord(self):
        """
            Function to handle the event triggered by the reveal word button. 
             - Hide or reveal the guess word to current draw player
        """
        if self.isTextHidden: # if the word is currently hidden, the button will reveal the text
            self.guessWordLabel.setText(self.guessWord) 
            self.guessWordLabel.setStyleSheet('font-weight: bold;')
            self.isTextHidden = False
        else:                # if the word is currently visible, the button will hide the text
            self.guessWordLabel.setText(self.hiddenText)
            self.isTextHidden = True

    def closeEvent(self, event): #closes the pop up window
        self.revealWord() 
        self.close()
        self.parentWindow.setDisabled(False)


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())
