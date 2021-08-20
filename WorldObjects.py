class WorldObject():
	def __init__(self, name):
		self.Name = name

	def SetPos(self, x, y):
		self.PosX = x
		self.PosY = y


class Door(WorldObject):
	def __init__(self, name):
		WorldObject.__init__(self, name)
		self.IsOpen = False

	def Reset(self):
		self.IsOpen = False


class GoalButton(WorldObject):
	def __init__(self, name):
		WorldObject.__init__(self, name)
		self.WasPressed = False

	def Reset(self):
		self.WasPressed = False

	def Press(self):
		self.WasPressed = True


class DoorButton(GoalButton):
	def __init__(self, name, door):
		WorldObject.__init__(self, name)
		self.Door = door

	def Reset(self):
		super().Reset()
		self.Door.IsOpen = False

	def Press(self):
		super().Press()
		self.Door.IsOpen = True