
class CIDict(dict):
	"""Case Insensitive dict where all keys are converted to lowercase
	This does not maintain the inputted case when calling items() or keys()
	in favor of speed, since headers are case insensitive
	"""

	def get(self, key, default=None):
		return super().get(key.lowercase(), default)

	def __getitem__(self, key):
		return super().__getitem__(key.lowercase())

	def __setitem__(self, key, value):
		return super().__setitem__(key.lowercase(), value)

	def __contains__(self, key):
		return super().__contains__(key.lowercase())
