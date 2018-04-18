from fman import DirectoryPaneCommand, show_alert, show_prompt
from fman.fs import is_dir
from fman.url import splitscheme, as_url
from subprocess import DEVNULL, Popen

import os
import shlex

# TODO, Add this path to Settings file
_SUBLIMETEXTPATH = 'C:/Program Files/Sublime Text 3/subl.exe'


class SublimeOpenSelected(DirectoryPaneCommand):
	def __call__(self):
		url = self.pane.get_path()
		scheme, path = splitscheme(url)

		if scheme != 'file://':
			show_alert('{} is not supported'.format(url))
			return

		chosen_files = self.get_chosen_files()
		option=" "
		if len(chosen_files)>1:
			option= " -n "
		if not chosen_files:
			show_alert('No file is selected!')
			return		
		openCommand(option, chosen_files, path)

class SublimeOpenCurrentFolderInNewWindow(DirectoryPaneCommand):
	def __call__(self):
		url = self.pane.get_path()
		scheme, path = splitscheme(url)

		if scheme != 'file://':
			show_alert('{} is not supported'.format(url))
			return

		paths=[]
		paths.append(as_url(path))	
		chosen_files = self.get_chosen_files()
			
		if chosen_files:
			for file in chosen_files:
				if not is_dir(file):
					paths.append(file)
			

		openCommand(" -n -a  ", paths, path)						

def to_path(url):
	
	return splitscheme(url)[1]

def openCommand(option, files, path):
	# TODO: Check if quoting is working for other platforms
	args = [shlex.quote(to_path(x)) for x in files]
	cmd= _SUBLIMETEXTPATH + " " + option + " " + " ".join(args)
	env = create_clean_environment()
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