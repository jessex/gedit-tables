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
		"""Constructs and returns a horizontal row for the table."""
		total = self.col * self.width
		chars = []
		if outside: #top or bottom horizontal piece
			total += self.col + 1
			for i in range(total):
				if i % (self.width+1) == 0:
					chars.append(self.inter_out)
				else:
					chars.append(self.horiz)
		else: #inner horizontal piece
			if self.has_outer: #there is an outer wall to watch for
				total += self.col + 1
				for i in range(total):
					if i % (self.width+1) == 0:
						if i == 0 or i == total - 1:
							chars.append(self.inter_out)
						else:
							chars.append(self.inter_in)
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
		#chars.append("\n")
		return ''.join(chars) #stringified character list
					

	def vertical(self):
		"""Constructs and returns a vertical row for the table."""
		total = self.col * self.width
		chars = []
		if self.has_outer:
			total += self.col + 1
			for i in range(total):
				if i % (self.width + 1) == 0:
					chars.append(self.vert)
				else:
					chars.append(' ')
		else:
			total += self.col - 1
			for i in range(total):
				if (i + 1) % (self.width + 1) == 0:
					if i != total:
						chars.append(self.vert)
				else:
					chars.append(' ')
		#chars.append("\n")
		return ''.join(chars) #stringified character list
		
	def vertical_data(self, columns):
		if self.col > len(columns):
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
		for i in range(self.row):
			if i != 0:
				pieces.append(self.horizontal(False))
			else:
				if self.has_outer:
					pieces.append(self.horizontal(True))
			for j in range(self.height):
				pieces.append(self.vertical())
		if self.has_outer:
			pieces.append(self.horizontal(True))
		return '\n'.join(pieces)
		
	def table_data(self, text, delimiter):
		"""Constructs a table around a block of text with this TableMaker's 
		parameters. Column and row count depends on the provided text."""
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
		"""Takes in a string of text and centers it in a whitespace-padding 
		string of length=width. Example: 'abcdef', 8 -> ' abcdef '"""
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
		
		
		