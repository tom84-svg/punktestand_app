import time

# Startwert des Counters
counter = 5

while counter > 0:
    print(counter)
    time.sleep(1)  # wartet 1 Sekunde
    counter -= 1

# Aktion nach der letzten Runde
print("Countdown beendet! Jetzt kannst du weitermachen.")
input("Drücke Enter, um fortzufahren...")
