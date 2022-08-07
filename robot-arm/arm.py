import time
import usb_arm # See https://github.com/orionrobots/python_usb_robot_arm
import glob

arm = usb_arm.Arm()

# Array to list components by abbreviation, name, status, actions
# 0 status is the mid-point for most components, off for LED and closed for grips
components =	[["l","LED",0,"Turn on (1) or turn off (0)"],
				["b","Base",0,"Rotate CW (+ve) or CCW (-ve)"],# base takes 14 seconds to rotate
				["s","Shoulder",0,"Move up (+ve) or down (-ve)"],# INCONSITENT ~ 14 seconds
				["e","Elbow",0,"Move up (+ve) or down (-ve)"],# 16 sec.s end to end depending on position
				["w","Wrist",0,"Move up (+ve) or down (-ve)"],# 4 sec.s end to end - fairly consistent
				["g","Grips",0,"Open (+ve) or close (-ve)"]]# grips take 1 second to open. 0 = closed

arm_calibrated = False

def arm_home():
	global arm_calibrated
	if arm_calibrated:
		print("Function to return home")
	else:
		print("Arm Not Calibrated To Home Position")

def arm_control(component,movetime):
	#Expects a l,b,s,e,w,g with a movetime
	global components
	if component == "l":
		if movetime == 0:
			arm.move(usb_arm.LedOff)
		elif movetime == 1:
			arm.move(usb_arm.LedOn)
	elif component == "b":
		if movetime > 0:
			arm.move(usb_arm.BaseClockWise, movetime)
		elif movetime < 0:
			arm.move(usb_arm.BaseCtrClockWise, (-1 * movetime))
	elif component =="s":
		if movetime > 0:
			arm.move(usb_arm.ShoulderUp, movetime)
		elif movetime < 0:
			arm.move(usb_arm.ShoulderDown, (-1 * movetime))
	elif component =="e":
		if movetime > 0:
			arm.move(usb_arm.ElbowUp, movetime)
		elif movetime < 0:
			arm.move(usb_arm.ElbowDown, (-1 * movetime))
	elif component =="w":
		if movetime > 0:
			arm.move(usb_arm.WristUp, movetime)
		elif movetime < 0:
			arm.move(usb_arm.WristDown, (-1 * movetime))
	elif component =="g":
		if movetime > 0:
			arm.move(usb_arm.GripsOpen, movetime)
		elif movetime < 0:
			arm.move(usb_arm.GripsClose, (-1 * movetime))
	elif component == "h":
		arm_home()
	else:
		print("Command Aborted")

def arm_calibrate():
	global arm_calibrated
	print("\n------------------\nConfiguration Mode\n------------------")
	print("Manually adjust each component so the arm is upright with closed grips.")
	global components
	configinput = ""
	for i in range (1,len(components)): # skip LED
		if components[i][0] == "b":
			print("Aligning Base")
			movetime = input("Enter +ve for CW or -ve for CCW or Blank to skip: ")
		elif components[i][0] == "g":
			print("Closing Grips")
			movetime = input("Enter +ve to open or -ve to close or Blank to skip: ")
		else:
			print("Aligning",str(components[i][1]))
			movetime = input("Enter +ve for up or -ve for down or Blank to skip: ")
		while movetime != "":
			movetime = float(movetime)
			arm_control(components[i][0],movetime)
			movetime = input("Enter move time again or leave blank to skip: ")
	arm_calibrated = True
	print("--------------\nArm Calibrated\n--------------")

def arm_commands():
	instructionlist = []
	print("-----------------------\nDirect Instruction Input\n-----------------------\n")
	print("Enter instruction in the format of component abbreviation\nfollowed by time e.g. 'b3.2' or 'end' to finish\nType 'help' for a helpful prompt.")
	instruction = input("Enter instruction: ")
	while instruction != "":
		if instruction == "help":
			print("""
Enter instructions by typing the component's
abbreviation followed by the move time.
Components are LED (l), Base (b), Shoulder (s),
Elbow (e), Wrist (w), Grips (g)
Positive or negative move times determine
actions e.g. up/down, open/close, anti/clockwise
E.g. s3 moves the shoulder up 3 seconds,
     g-0.5 closes the grips for 0.5 seconds,
     b2 rotates the base clockwise for 2 seconds
""")
		elif len(instruction) > 1:
			instructionlist.append(instruction)
			arm_control(instruction[0],float(instruction[1:]))
		instruction = input("Enter Instruction: ")
	
	print("These are the instructions you sent:")
	print(instructionlist)
	if input("Would you like to save instructions to file? (y or Enter)?: ") == "y":
		print("The directory contains the following files:")
		print(glob.glob("arm-commands/*.txt"),"/n")
		print("Please specify a filename (incl. extension).\nExisting files will be overwritten.")
		filename = input("Filename: ")
		txt_file = open("arm-commands/"+filename,"w")
		for i in range(len(instructionlist)):
			#print("Writing:",str(instructionlist[i]))
			if i ==  (len(instructionlist) - 1):
				txt_file.write(instructionlist[i])
			else:
				txt_file.write(instructionlist[i]+",")
		txt_file.close()
		time.sleep(1)
		print(str(len(instructionlist)),"instructions written to file.")
		time.sleep(1)
	instructionlist = []
	print("\nDirect command input session finished.")

def arm_interactive():
	global components
	for i in range(len(components)):
		print(str(i+1)+". "+str(components[i][1]))
	choice_comp = input("Choose component (Blank To End): ")
	if choice_comp == "":
		return "",""
	print("Perform the following actions by entering a positive or negative number.")
	print(str(components[int(choice_comp)- 1][3]))
	choice_comp = components[int(choice_comp)-1][0]
	choice_movetime = input("Enter a positive or negative number or BLANK to skip: ")
	if choice_movetime == "":
		return "f",""
	choice_movetime = float(choice_movetime)
	return choice_comp,choice_movetime
	
def arm_openfile():
	print("\n-----------------------\nRun Commands from file.\n-----------------------")
	print("This program expects to see .txt files containing\ninstructions in the sub-directory arm-commands/")
	print("List of files:\n")
	print(glob.glob("arm-commands/*.txt"))
	print("(TBC) - Would you like to attempt to return\nthe arm to the home position first?")
	print("Please specify the name of the file and include the extension\nDo not include the directory path.")
	filename = input("Filename: ")
	txt_file = open("arm-commands/"+filename,"r")
	instructionlist = txt_file.read().split(",")
	txt_file.close()
	time.sleep(1)
	print("The file",str(filename),"contains",str(len(instructionlist)),"instructions.")
	if input("Execute instructions? (y) or ENTER to abandon: ") == "y":
		for i in range(len(instructionlist)):
			instruction = instructionlist[i]
			arm_control(instruction[0],float(instruction[1:]))
	print("Instructions Complete")

def main():
	print("\n****************************\nWelcome to Robot Arm Control\n****************************")
	menu_choice = 0
	while menu_choice != "5":
		time.sleep(1)
		print("""\n---------
MAIN MENU
---------
You have the following options:
1. Calibrate arm to home position (pseudo-positioning)
2. Open and execute commands from a file
3. Use interactive menu to control arm
4. Type in control commands (e.g. "S-3")
5. Exit
(Choosing 3 and 4 will give option to save commands.)
""")
		menu_choice = input("Choose Option 1 to 5: ")
		print("")
		if menu_choice == "1":
			arm_calibrate()
		elif menu_choice == "2":
			arm_openfile()
		elif menu_choice == "3":
			component,movetime = arm_interactive()
			while component !="":
				arm_control(component,movetime)
				component,movetime = menu_choice()
		elif menu_choice == "4":
			arm_commands()
		elif menu_choice == "5":
			print("Goodbye\n")
			time.sleep(1)
		else:
			print("Menu Option Not Recognised")
	
main()
