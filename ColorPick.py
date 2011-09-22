import sublime, sublime_plugin
import subprocess
from os import path

def is_hex(s):
  try:
    int('0x' + s, 16)
    return True
  except:
    return False

class ColorPickCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    sel = view.sel()
    start_color = None

    # get the currently selected color - if any
    if len(sel) > 0:
      selected = view.substr(view.word(sel[0])).strip()
      if selected.startswith('#'): selected = selected[1:]
      if is_hex(selected) and (len(selected) == 6 or len(selected) == 3):
        start_color = selected

    # get new color from picker
    args = [path.join(sublime.packages_path(), 'ColorPick', 'bin', 'colorpick')]
    if start_color:
      args.append('-startColor')
      args.append(start_color)
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
          self.view.replace(edit, region, '#' + color)
