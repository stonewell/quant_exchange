import backends.pickle_backend

def default_backend():
	return backends.pickle_backend.PickleBackend()
