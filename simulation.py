"""
Name: Simulation - run this script to run the project simulation

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli


"""
import numpy as np
from agent import agent
from uav import uav
import sys
from CreateEnvironment import CreateEnvironment
from GridWorld import GridWorld
#environment class/functions?
#def 



if __name__ == "__main__":
	#-------for unit tests----------
	start = np.array([int(1),int(1)])
	goal = np.array([[int(9),int(9)]]) 
	#-----------------------------------------------------
	#obstacle = [[1,1] [5,5]]
	env_file = open("Environment.txt","w")
	gridWorld = CreateEnvironment()
	gridWorld.create(env_file, size_row='10', size_col='10', agent_row='0', agent_col='0', goal_row='9', goal_col='9', static_number='2', static_list=[0,3,2,4])
	env_file = open("Environment.txt", "r")
	text_in_file = env_file.readline()
	print (text_in_file)
	grid = GridWorld(text_in_file)
	gw = grid.gridDefine()
	#-------------------------------------------------------
	# initalize vehicle position
	vehState = start
	
	# initialize agent class and uav class
	Agent=agent(vehState)
	# define a model dictionary, which maps user inputs of learning model names to learning model function
	modelType = {"random":Agent.predict_Random,"standard":Agent.predict_Standard,"NN":Agent.predict_NN}
	UAV = uav(vehState)
	
	# initialize decision model (options = "random", "standard", or "NN")
	model = "random" # will be a user input

	
	try:
		# while the agent is not located at the goal position:
		while vehState[0,0] != goal[0,0] or vehState[0,1] != goal[0,1] or vehState != wall:
			#------------------------------------------
			print("sim is running")
			# make observations
			rew = UAV.observe([gw[vehState[0]-1][vehState[1]],gw[vehState[0,0]][vehState[0,1]+1],gw[vehState[0,0]+1][vehState[0,1]],gw[vehState[0,0]][vehState[0,1]-1]])
			print("rewards =", rew)
			# decide what action to take
			action_commanded = modelType[model](vehState,rew)
			print ("commanded action = ",action_commanded)
			# command action (employ dynamics)
			vehState = UAV.move(vehState, action_commanded) # is location an argument to this?
			print ("New Vehicle State = ", vehState)
			#------------------------------------------

		# if vehicle is in an obstacle grid space, quit and output "Mission Failed"
			#if vehState.all() == obstacle.any():
			#	print ("Mission Failed")
			#	break 
			#else:
			#	pass
		# store hstory of states		
	except KeyboardInterrupt:
		print("Interrupted")
		
		#store history of state and commanded action as text files
		sys.exit(0)
					 

