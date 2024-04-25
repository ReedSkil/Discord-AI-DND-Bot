Set up:

	First you will need a:
		Discord Bot Token (on line 15)
		gemini api key (for all processes of the dungeon master such as decisions and storywriting) on line 13
		Openai api key (for picture services, head admin can disable this feature at will) on line 19
		Two discord ids (These can be the same discord id) starting on line 18
	
	*You may also need to configure your file path for saving and loading the text log of the dnd story on lines 125, 146 and 170*

Description:

    	This bot functions as a dungeon master for the game of DND by using gemini (and openai if you have money in an account for
    pictures). 

	Every decision is decided by the gemini ai, anything from character creation (including character stats) to story decisions.
    All characters and story elements are saved to a specified file location (on the desktop by default). 

	The only feature introduced as of now is health and a damage dealt function for failing any type of roll, having the characters 
    in a campaign slowly die off (however I believe this adds to the campaign in my humble opinion). Any other actions or features are implemented 
    by gemini such as conversations with npcs (it is worth noting that gemini decides the skill barrier for the action you are about to take, 
    then the bot rolls for it applying the appropriate modifier in your character screen). 

	Lastly the bot takes into account all characters created and are included in the prompt to gemini whenever anyone takes an action, 
    resulting in a dnd party like atmosphere (ie if I "!go slap [insert other character]" gemini will have a history of that characters info 
    to draw upon and might even involve more characters in the party in the interaction). Fair warning, as of now it has a hard time killing 
    off characters but I am in the process of fixing that.


Commands to Use (id recommend pasting these somewhere in your discord):

	Everyone:
		!create (make a character) You can always recreate your character if they die, but personally I think I am going to try to make a new character every death
		!status (see your characters stats)
		!story (Summarizes the campaign so far this is a new feature so its a bit untested)
		!party (Show Everyone in the Party and their Classes)
		!go [insert prompt here.] (do an action, go to a place, etc.) example: !go play valorant with a trackpad
		!say [insert prompt here.] (Say something. Can be followed by an action of formatted like !say "Hey Person!" while punching him in the face)
		!delete character heartlessly (deletes your character. Its long to type since there is no confirm or deny)

	Admin only:
		!test (simple test that prints the members id in the console of the program)
		!picture (Enables or Disables pictures, a message will be sent into chat stating the status pictures)
		