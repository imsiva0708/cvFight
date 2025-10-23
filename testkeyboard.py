from pynput.keyboard import Key, Controller

keyboard = Controller()
keyboard.press(Key.alt)
keyboard.press(Key.tab)
keyboard.release(Key.alt)
keyboard.release(Key.tab)
for i in range(1000):
    keyboard.press('z')
    keyboard.release('z')