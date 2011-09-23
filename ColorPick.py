import sublime, sublime_plugin
import subprocess
from os import path

def is_valid_hex_color(s):
  if len(s) not in (3, 6):
    return False
  try:
    return 0 <= int(s, 16) <= 0xffffff
  except ValueError:
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
      if is_valid_hex_color(selected):
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
