import machine
from utime import ticks_ms, ticks_diff

class Keypad:
    def __init__(self, rows, cols, keymap, debounceTime=50):
        self.rows = []
        self.cols = []
        self.rowsCount = len(rows)
        self.colsCount = len(cols)
        self.keymap = keymap
        self.keyStates = [[False] * self.colsCount for _ in range(self.rowsCount)]
        self.debounceTime = debounceTime

        for row in rows:
            self.rows.append(machine.Pin(row, machine.Pin.OUT))
        
        for col in cols:
            self.cols.append(machine.Pin(col, machine.Pin.IN, machine.Pin.PULL_DOWN))

        if len(self.keymap) != self.rowsCount:
            raise ValueError("Invalid keymap: number of rows does not match")
        
        for row in self.keymap:
            if len(row) != self.colsCount:
                raise ValueError("Invalid keymap: number of columns does not match")
            
    
    def scanKeys(self):
        for row in range(self.rowsCount):
            self.rows[row].high()

            for col in range(self.colsCount):
                if not self.keyStates[row][col]:
                    if self.cols[col].value() == 1 and not self._debounce(col, row):
                        self.keyStates[row][col] = True
                        return self.keymap[row][col]
                elif self.cols[col].value() == 0:
                    self.keyStates[row][col] = False
            
            self.rows[row].low()
    
    def _debounce(self, col, row):
        startTime = ticks_ms()
        while ticks_diff(ticks_ms(), startTime) < self.debounceTime:
            if self.cols[col].value() == 0:
                return False
        return True