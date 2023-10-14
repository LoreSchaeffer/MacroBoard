import ujson as json

class Config:
    def __init__(self, filename, defaults={}):
        self.filename = filename
        self.data = defaults
        self.defaults = defaults


    def exists(self):
        try:
            with(open(self.filename, "r")) as file:
                return True
        except OSError:
            return False


    def load(self):
        try:
            with(open(self.filename, "r")) as file:
                self.data = self._mergeDefaults(self.defaults, json.load(file))
            self.save()
        except ValueError:
            self.data = self.defaults
            self.save()
        except:
            print("Error reading " + self.filename)

    
    def save(self):
        try:
            with(open(self.filename, "w")) as file:
                json.dump(self.data, file)
        except:
            print("Error writing " + self.filename)

    
    def get(self, key):
        keys = key.split('.')
        value = self.data
        for k in keys:
            value = value.get(k, None)
            if value is None:
                break
        return value
    

    def set(self, key, value):
        keys = key.split('.')
        data = self.data
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        data[keys[-1]] = value
        self.save()

    
    def getData(self):
        return self.data
    
    
    def _mergeDefaults(self, defaults, loaded):
        for key, value in defaults.items():
            if key not in loaded:
                loaded[key] = value
            elif isinstance(value, dict) and isinstance(loaded[key], dict):
                loaded[key] = self._mergeDefaults(value, loaded[key])
        return loaded