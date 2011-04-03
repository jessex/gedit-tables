class TableMaker:

	def __init__(self, col, row, height, width, chars, has_outer):
		self.col = col
		self.row = row
		self.height = height
		self.width = width
		self.horiz, self.vert, self.inter_out, self.inter_in = chars #unpack
		self.has_outer = has_outer
	
	def horizontal(self, outside):
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
		
	def table(self):
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
		