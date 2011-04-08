import gedit
import pygtk
pygtk.require('2.0')
import gtk
from gettext import gettext

ui_str = """
<ui>
  <menubar name="MenuBar">
	<menu name="ToolsMenu" action="Tools">
	  <placeholder name="ToolsOps_2">
		<menuitem name="Gedit Tables" action="Gedit Tables"/>
	  </placeholder>
	</menu>
  </menubar>
</ui>
"""


class TableMaker:

	def __init__(self, col, row, height, width, chars, has_outer):
		"""Instantiates TableMaker instance with the number of columns, the 
		number of rows, the height (in lines) of each row, the width (in spaces) 
		of each column, a tuple of characters (horizontal, vertical, 
		intersection outside and intersection inside), and whether or not there 
		is a border around the outside of the table."""
		self.col = col
		self.row = row
		self.height = height
		self.width = width
		self.horiz, self.vert, self.inter_out, self.inter_in = chars #unpack
		self.has_outer = has_outer
	
	def horizontal(self, outside):
		"""Constructs and returns a horizontal piece for the table."""
		total = self.col * self.width
		chars = []
		if outside: #top or bottom horizontal piece
			total += self.col + 1
			for i in range(total):
				if i % (self.width+1) == 0:
					chars.append(self.inter_out) #all intersections are outer
				else:
					chars.append(self.horiz)
		else: #inner horizontal piece
			if self.has_outer: #there is an outer wall to watch for
				total += self.col + 1
				for i in range(total):
					if i % (self.width+1) == 0:
						if i == 0 or i == total - 1:
							chars.append(self.inter_out) #edge pieces
						else:
							chars.append(self.inter_in) #inner intersections
					else:
						chars.append(self.horiz)
			else: #no outer wall to watch for
				total += self.col - 1
				for i in range(total):
					if (i + 1) % (self.width + 1) == 0:
						if i != total:
							chars.append(self.inter_in)
					else:
						chars.append(self.horiz)
		return ''.join(chars) #stringified character list
					

	def vertical(self):
		"""Constructs and returns a vertical piece for the table."""
		total = self.col * self.width
		chars = []
		if self.has_outer: #vert, white space, vert, whitespace, ... , vert
			total += self.col + 1
			for i in range(total):
				if i % (self.width + 1) == 0:
					chars.append(self.vert)
				else:
					chars.append(' ')
		else: #white space, vert, white space, vert, ... , white space
			total += self.col - 1
			for i in range(total):
				if (i + 1) % (self.width + 1) == 0:
					if i != total: #last char will make check so filter out
						chars.append(self.vert)
				else:
					chars.append(' ')
		return ''.join(chars) #stringified character list
		
	def vertical_data(self, columns):
		"""Constructs and returns a vertical piece containing data from the 
		columns list."""
		if self.col > len(columns): #fill in extra table columns with whitespace
			white = " " * self.width
			for i in range(self.col - len(columns)):
				columns.append(white)
		str = ''
		if self.has_outer:
			for col in columns:
				str += self.vert
				str += self.centered(col, self.width)
			str += self.vert
		else:
			for col in columns:
				str += self.centered(col, self.width)
				str += self.vert
			str = str[0:-1] #remove extra vertical separator at end
		return str
		
	def table(self):
		"""Constructs and returns a table with this TableMaker's parameters."""
		pieces = []
		for i in range(self.row): #build each row as horizontal then vertical(s)
			if i != 0:
				pieces.append(self.horizontal(False))
			else:
				if self.has_outer:
					pieces.append(self.horizontal(True))
			for j in range(self.height):
				pieces.append(self.vertical())
		if self.has_outer: #bottom horizontal piece if outer border
			pieces.append(self.horizontal(True))
		return '\n'.join(pieces)
		
	def table_data(self, text, delimiter):
		"""Constructs a table around a block of text with this TableMaker's 
		parameters. Column/row count and column width depends on the provided 
		text. Text across multiple lines is split on new lines to determine 
		rows, and individual rows are split on delimiter to make columns."""
		#divide our text into rows and columns and set our row, col, width vars
		lines = text.rsplit("\n")
		self.row = len(lines)
		self.col = 0
		rows = [] #contains rows, each row contains columns
		for line in lines:
			rows.append(line.rsplit(delimiter)) #separate rows by column
			if len(rows[-1]) > self.col: #get maximum column count for a row
				self.col = len(rows[-1])
		self.width = 0
		for row in rows:
			for col in row:
				if len(col) > self.width: #get maximum column width
					self.width = len(col)
		self.width += 2 #add cushioning
		
		#construct table around text
		pieces = []
		for i in range(self.row): #begin normal construction
			if i != 0:
				pieces.append(self.horizontal(False))
			else:
				if self.has_outer:
					pieces.append(self.horizontal(True))
			pieces.append(self.vertical_data(rows[i])) #add col data as vertical
			if self.height > 1:
				for i in range(self.height-1): #more empty vertical space
					pieces.append(self.vertical())
		if self.has_outer:
			pieces.append(self.horizontal(True))
		return '\n'.join(pieces)
		
	def centered(self, text, width):
		"""Takes in a string of text and centers it in a whitespace-padded 
		string of length=width. Example: 'abcdef', 8 -> ' abcdef '. Example: 
		'abcdef', 11 -> '  abcdef   '. Example: 'ab', 2 -> 'ab'."""
		if len(text) == width:
			return text
		if len(text) > width:
			return text[0:width]
		str = ''
		if len(text) % 2 == width % 2: #both even or both odd
			padding = (width - len(text)) / 2
			str += " " * padding
			str += text
			str += " " * padding
		else: #cannot be perfectly centered, push 1 to left
			padding = (width - 1 - len(text)) / 2
			str += " " * padding
			str += text
			str += " " * (padding + 1)
		return str
		
		
class GTWindow:

	def __init__(self, plugin, window):
		self.window = window
		self.plugin = plugin
		self.insert_menu()
		
	def deactivate(self):
		self.remove_menu()
		self.window = None
		self.plugin = None
		self.action_group = None
		
	def insert_menu(self):
		manager = self.window.get_ui_manager()
		#create action group
		self.action_group = gtk.ActionGroup("Gedit Tables Actions")
		#add actions to group
		self.action_group.add_actions([("Gedit Tables", None, \
		gettext("Create Table"), None, gettext("Create a Table"), \
		self.launch_dialog)])
		#add action group to manager
		manager.insert_action_group(self.action_group, -1)
		self.ui_id = manager.add_ui_from_string(ui_str)
		
	def remove_menu(self):
		manager = self.window.get_ui_manager()
		manager.remove_ui(self.ui_id)
		manager.remove_action_group(self.action_group)
		manager.ensure_update()
		
	def update_ui(self):
		self.action_group.set_sensitive(self.window.get_active_document()!=None)
		
	def launch_dialog(self, action):
		doc = self.window.get_active_document()
		if not doc:
			return
		self.plugin.on_menu_click(self.window, doc)
	
	
class GeditTables(gedit.Plugin):

	def __init__(self):
		gedit.Plugin.__init__(self)
		self.instances = {}
		self.dialog = None
	
	def activate(self, window):
		self.instances[window] = GTWindow(self, window)
	
	def deactivate(self, window):
		self.instances[window].deactivate()
		del self.instances[window]
		
	def update_ui(self, window):
		self.instances[window].update_ui()
		
	def insert_table(self, table_maker):
		document = gedit.app_get_default().get_active_window().get_active_document()
		document.insert_at_cursor(table_maker.table()) #insert table at cursor position
		
	def insert_data_table(self, delimiter, table_maker):
		document = gedit.app_get_default().get_active_window().get_active_document()
		bounds = document.get_selection_bounds() #get boundaries of highlighted
		if not bounds:
			return False
		start, end = bounds
		
		text = document.get_text(start, end) #get highlighted text
		table = table_maker.table_data(text, delimiter) #create table around it
		document.delete(start, end) #delete highlighted portion and...
		document.insert_at_cursor(table) #...overwrite with table
		
	def is_valid_tm(self, vals):
		pass
	
	def on_menu_click(self, window, document):
		self.dialog = TableDialog(self)
		self.dialog.set_transient_for(window)
		self.dialog.present()
		
	def on_dialog_response(self, dialog, response):
		if response == gtk.RESPONSE_ACCEPT:
			doc = gedit.app_get_default().get_active_window().get_active_document()
		else:
			self.dialog = None
			self.dialog.destroy()
			
	
			
class TableDialog():
	def toggle_snap(self, widget, spin):
		spin.set_snap_to_ticks(widget.get_active())

	def toggle_numeric(self, widget, spin):
		spin.set_numeric(widget.get_active())

	def change_digits(self, widget, spin, spin1):
		spin1.set_digits(spin.get_value_as_int())

	def get_value(self, widget, data, spin, spin2, label):
		if data == 1:
			buf = "%d" % spin.get_value_as_int()
		else:
			buf = "%0.*f" % (spin2.get_value_as_int(),
							 spin.get_value())
		label.set_text(buf)
		
	def toggle_with_data(self, widget, delim, row, col, width):
		b = not widget.get_active()
		delim.set_sensitive(not b)
		row.set_sensitive(b)
		col.set_sensitive(b)
		width.set_sensitive(b)
		
	def close(self, widget):
		self.plugin.dialog = None
		self.window.destroy()
		
	def make_table(self, widget, row, col, width, height, ch_h, ch_v, ch_io, \
	ch_ii, delim, check, borders):
		#pull data from dialog fields
		rows = row.get_value_as_int()
		columns = col.get_value_as_int()
		spaces = int(width.get_text())
		lines = int(height.get_text())
		horiz = ch_h.get_text()
		vert = ch_v.get_text()
		inner = ch_ii.get_text()
		outer = ch_io.get_text()
		#create TableMaker instance
		tm = TableMaker(columns, rows, lines, spaces, (horiz, vert, outer, \
		inner), borders.get_active())
		
		if check.get_active():
			delimiter = delim.get_text()
			self.plugin.insert_data_table(delimiter, tm)
		else:
			self.plugin.insert_table(tm)
		
		
		

	def __init__(self, plugin):
		self.plugin = plugin
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#window.connect("destroy", lambda w: gtk.main_quit())
		self.window.set_title("Insert Table")
		self.window.set_resizable(False)

		main_vbox = gtk.VBox(False, 5)
		main_vbox.set_border_width(10)
		self.window.add(main_vbox)


		frame = gtk.Frame("Table Dimensions")
		main_vbox.pack_start(frame, True, True, 0)
  
		vbox = gtk.VBox(False, 0)
		vbox.set_border_width(5)
		frame.add(vbox)

		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, True, True, 5)
  
		vbox2 = gtk.VBox(False, 0)
		hbox.pack_start(vbox2, True, True, 5)

		label = gtk.Label("Rows:")
		label.set_alignment(0, 0.5)
		vbox2.pack_start(label, False, True, 5)
  
		adj = gtk.Adjustment(1.0, 1.0, 1000.0, 1.0, 5.0, 0.0)
		spinner_rows = gtk.SpinButton(adj, 0, 0)
		spinner_rows.set_wrap(True)
		vbox2.pack_start(spinner_rows, False, True, 0)
  
		vbox2 = gtk.VBox(False, 0)
		hbox.pack_start(vbox2, True, True, 5)
  
		label = gtk.Label("Columns:")
		label.set_alignment(0, 0.5)
		vbox2.pack_start(label, False, True, 5)

		adj = gtk.Adjustment(1.0, 1.0, 1000.0, 1.0, 5.0, 0.0)
		spinner_cols = gtk.SpinButton(adj, 0, 0)
		spinner_cols.set_wrap(True)
		vbox2.pack_start(spinner_cols, False, True, 0)
  
		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, True, True, 5)
		
		vbox2 = gtk.VBox(False, 0)
		hbox.pack_start(vbox2, True, True, 5)
  
		label = gtk.Label("Row Height:")
		label.set_alignment(0, 0.5)
		vbox2.pack_start(label, False, True, 5)
		
		hbox2 = gtk.HBox(False, 0)
		
		entry_rows = gtk.Entry()
		entry_rows.set_max_length(3)
		entry_rows.set_text("1")
		entry_rows.set_width_chars(10)
		hbox2.pack_start(entry_rows, False, True, 0)
		
		label = gtk.Label(" lines")
		label.set_alignment(0, 0.5)
		hbox2.pack_start(label, False, True, 0)
		
		vbox2.pack_start(hbox2, False, True, 0)
		
		vbox2 = gtk.VBox(False, 0)
		hbox.pack_start(vbox2, True, True, 5)
		
		label = gtk.Label("Column Width:")
		label.set_alignment(0, 0.5)
		vbox2.pack_start(label, False, True, 5)
		
		hbox2 = gtk.HBox(False, 0)
		vbox2.pack_start(hbox2, False, True, 0)
		
		entry_cols = gtk.Entry()
		entry_cols.set_max_length(3)
		entry_cols.set_text("5")
		entry_cols.set_width_chars(10)
		hbox2.pack_start(entry_cols, False, True, 0)
		
		label = gtk.Label(" spaces")
		label.set_alignment(0, 0.5)
		hbox2.pack_start(label, False, True, 0)
		
		borders = gtk.CheckButton("Build outer walls of table")
		borders.set_active(True)
		vbox.pack_start(borders, False, True, 5)
		
		
		frame = gtk.Frame("Characters")
		main_vbox.pack_start(frame, True, True, 0)
		
		vbox = gtk.VBox(False, 0)
		vbox.set_border_width(5)
		frame.add(vbox)
		
		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, False, True, 5)
		
		label = gtk.Label("Horizontal:")
		label.set_alignment(0, 0.5)
		hbox.pack_start(label, False, True, 0)
		
		entry_horiz = gtk.Entry()
		entry_horiz.set_max_length(1)
		entry_horiz.set_text("-")
		entry_horiz.set_width_chars(3)
		hbox.pack_start(entry_horiz, False, True, 12)
		
		label = gtk.Label("Vertical:")
		label.set_alignment(0, 0.5)
		hbox.pack_start(label, False, True, 0)
		
		entry_vert = gtk.Entry()
		entry_vert.set_max_length(1)
		entry_vert.set_text("|")
		entry_vert.set_width_chars(3)
		hbox.pack_start(entry_vert, False, True, 27)
		
		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, False, True, 5)
		
		label = gtk.Label("Outer Cross:")
		label.set_alignment(0, 0.5)
		hbox.pack_start(label, False, True, 0)
		
		entry_outer = gtk.Entry()
		entry_outer.set_max_length(1)
		entry_outer.set_text("o")
		entry_outer.set_width_chars(3)
		hbox.pack_start(entry_outer, False, True, 5)
		
		label = gtk.Label("Inner Cross:")
		label.set_alignment(0, 0.5)
		hbox.pack_start(label, False, True, 5)
		
		entry_inner = gtk.Entry()
		entry_inner.set_max_length(1)
		entry_inner.set_text("+")
		entry_inner.set_width_chars(3)
		hbox.pack_start(entry_inner, False, True, 0)
		
		
		frame = gtk.Frame("Fill Table")
		main_vbox.pack_start(frame, True, True, 0)
		
		vbox = gtk.VBox(False, 0)
		vbox.set_border_width(5)
		frame.add(vbox)
		
		entry_delim = gtk.Entry()
		check = gtk.CheckButton("Build around highlighted data")
		check.connect("clicked", self.toggle_with_data, entry_delim, \
		spinner_rows, spinner_cols, entry_cols)
		vbox.pack_start(check, False, True, 5)
		
		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, False, True, 0)
		
		label = gtk.Label("Delimiter:")
		label.set_alignment(0, 0.5)
		hbox.pack_start(label, False, True, 0)
		
		entry_delim.set_max_length(1)
		entry_delim.set_text(",")
		entry_delim.set_width_chars(10)
		entry_delim.set_sensitive(False)
		hbox.pack_start(entry_delim, False, True, 10)
  
		hbox = gtk.HBox(False, 0)
		main_vbox.pack_start(hbox, False, True, 0)
  
		button_ok = gtk.Button("Insert")
		button_ok.connect("clicked", self.make_table, spinner_rows, spinner_cols, \
		entry_cols, entry_rows, entry_horiz, entry_vert, entry_outer, \
		entry_inner, entry_delim, check, borders)
		hbox.pack_start(button_ok, True, True, 5)
  
		button_cancel = gtk.Button("Cancel")
		button_cancel.connect("clicked", self.close)
		hbox.pack_start(button_cancel, True, True, 5)
		self.window.show_all()



			