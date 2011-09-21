import sublime, sublime_plugin
import subprocess
from os import path

class ColorPickCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    sel = view.sel()
    selected = None

    # get the currently selected color - if any
    if len(sel) > 0:
      selected = view.substr(view.word(sel[0])).strip()
      if selected.startswith('#'): selected = selected[1:]

    # get new color from picker
    args = [path.join(sublime.packages_path(), 'ColorPick', 'bin', 'colorpick')]
    if selected != None and (len(selected) == 6 or len(selected) == 3):
      args.append('-startColor')
      args.append(selected)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    color = proc.communicate()[0]
    
    if color:
      # replace all regions with color
      for region in sel:
        word = view.word(region)
        if view.substr(word.a - 1) == '#':
          word = sublime.Region(word.a - 1, word.b)
          self.view.replace(edit, word, '#' + color)
        else:
          self.view.insert(edit, sel[0].begin(), '#' + color)
