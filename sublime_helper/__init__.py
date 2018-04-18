from fman import DirectoryPaneCommand, show_alert, show_prompt
from fman.url import splitscheme
from subprocess import DEVNULL, Popen

import os
import shlex

# TODO, Add this path to Settings file
_SUBLIMETEXTPATH = 'C:/Program Files/Sublime Text 3/subl.exe'


class SublimeOpenProjectInNewWindow(DirectoryPaneCommand):
	def __call__(self):
		# show_alert('Hello World!')
		url = self.pane.get_path()
		scheme, path = splitscheme(url)

		if scheme != 'file://':
			show_alert('{} is not supported'.format(url))
			return

		chosen_files = self.get_chosen_files()
		if not chosen_files:
			show_alert('No file is selected!')
			return		
		openCommand(" ", chosen_files, path)

class SublimeOpenFolderInNewWindow(DirectoryPaneCommand):
	def __call__(self):
		url = self.pane.get_path()
		scheme, path = splitscheme(url)

		if scheme != 'file://':
			show_alert('{} is not supported'.format(url))
			return

		chosen_files = self.get_chosen_files()
		if not chosen_files:
			show_alert('No file is selected!')
			return		
		openCommand("   ", path, path)						

def to_path(url):
    return splitscheme(url)[1]

def openCommand(option, files, path):
	args = [shlex.quote(to_path(x)) for x in files]
	cmd= _SUBLIMETEXTPATH + " " + option + " " + " ".join(args)
	env = create_clean_environment()
	f= open('c:\\tmp\\flat.txt', 'a')
	f.write('\n' + cmd)
	f.close()	
	Popen(cmd, shell=False, cwd=path,
		stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, env=env)

def create_clean_environment():
	# Pyinstaller, used by fman to ship on Linux sets LD_LIBRARY_PATH, which
	# prevents starting Qt5 applications. Remove the variable if it is set.
	env = dict(os.environ)
	try:
		del env['LD_LIBRARY_PATH']
	except KeyError:
		pass
	return env