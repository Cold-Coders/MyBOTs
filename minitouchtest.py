from pyminitouch import safe_connection, safe_device, MNTDevice, CommandBuilder

_DEVICE_ID = "emulator-5554"

# ---
'''
device = MNTDevice(_DEVICE_ID)



# It's also very important to note that the maximum X and Y coordinates may, but usually do not, match the display size.
# so you need to calculate position by yourself, and you can get maximum X and Y by this way:
print("max x: ", device.connection.max_x)
print("max y: ", device.connection.max_y)

# single-tap
device.tap([(400, 600)])
# multi-tap
device.tap([(400, 400), (600, 600)])
# set the pressure, default == 100
device.tap([(400, 600)], pressure=50)

# long-time-tap
device.tap([(400, 600)], duration=2000)

# and no up at the end. you can continue your actions after that. default to false
device.tap([(400, 600)], duration=2000, no_up=True)

# swipe
device.swipe([(100, 100), (500, 500)])
# of course, with duration and pressure
device.swipe([(100, 100), (400, 400), (200, 400)], duration=500, pressure=50)

# and no down at the beginning or no up at the end.
# you can apply a special action before swipe, to build a complex action.
device.tap([(400, 600)], duration=2000, no_up=True)
device.swipe(
    [(400, 600), (400, 400), (200, 400)],
    duration=500,
    pressure=50,
    no_down=True,
    no_up=True,
)
device.swipe(
    [(200, 400), (400, 400), (400, 600)], duration=500, pressure=50, no_down=True
)

# extra functions ( their names start with 'ext_' )
device.ext_smooth_swipe(
    [(100, 100), (400, 400), (200, 400)], duration=500, pressure=50, part=20
)

# stop minitouch
# when it was stopped, minitouch can do nothing for device, including release.
device.stop()

# ---

# In another way, you needn't consider about device's life-cycle.
# context manager will handle it
with safe_device(_DEVICE_ID) as device:
    # single-tap
    device.tap([(400, 600)])
    # multi-tap
    device.tap([(400, 400), (600, 600)])
    # set the pressure, default == 100
    device.tap([(400, 600)], pressure=50)

# ---


# What's more, you can also access low level API for further usage.
with safe_connection(_DEVICE_ID) as connection:
    builder = CommandBuilder()
    builder.down(0, 400, 400, 50)
    builder.commit()
    builder.move(0, 500, 500, 50)
    builder.commit()
    builder.move(0, 800, 400, 50)
    builder.commit()
    builder.up(0)
    builder.commit()

    builder.publish(connection)
    # if you are using MNTDevice object, replace with this:
    # builder.publish(device.connection)

# ---




# Of course, you may want to operate it just like using minitouch itself.
# send raw text to it
_OPERATION = """
d 0 10 10 50\n
c\n
u 0\n
c\n
"""

with safe_connection(_DEVICE_ID) as conn:
    conn.send(_OPERATION)

'''

_OPERATION2 = """
d 0 9000 1000 90\n
d 1 9000 19000 90\n
c\n
m 0 9000 2000 90\n
m 1 9000 18000 90\n
c\n
m 0 9000 3000 90\n
m 1 9000 17000 90\n
c\n
m 0 9000 4000 90\n
m 1 9000 16000 90\n
c\n
m 0 9000 5000 90\n
m 1 9000 15000 90\n
c\n
m 0 9000 6000 90\n
m 1 9000 14000 90\n
c\n
m 0 9000 7000 90\n
m 1 9000 13000 90\n
c\n
u 0\n
u 1\n
c\n
"""



_OPERATION3 = """
d 0 1000 100 90\n
d 1 10000 100 90\n
c\n
u 0\n
u 1\n
c\n
"""


_OPERATION4 = """
d 0 1000 1000 60\n
c\n
u 0\n
c\n
"""
_OPERATION5 = """
d 0 10000 100 60\n
c\n
u 0\n
c\n
"""




#y,x 
_ZoomOut2 = """
r\n
d 0 300 600 50\n
d 1 560 600 50\n
c\n
w 50\n
m 0 325 600 50\n
m 1 535 600 50\n
c\n
w 50\n
m 0 350 600 50\n
m 1 510 600 50\n
c\n
w 50\n
m 0 375 600 50\n
m 1 485 600 50\n
c\n
w 50\n
m 0 400 600 50\n
m 1 460 600 50\n
c\n
w 50\n
m 0 425 600 50\n
m 1 435 600 50\n
c\n
w 50\n
m 0 430 600 50\n
m 1 430 600 50\n
c\n
w 50\n
u 0\n
u 1\n
c\n
"""




_ZoomOut = """
r\n
d 0 9000 1000 50\n
d 1 9000 16000 50\n
c\n
w 50\n
m 0 9000 2000 50\n
m 1 9000 15000 50\n
c\n
w 50\n
m 0 9000 3000 50\n
m 1 9000 14000 50\n
c\n
w 50\n
m 0 9000 4000 50\n
m 1 9000 13000 50\n
c\n
w 50\n
m 0 9000 5000 50\n
m 1 9000 12000 50\n
c\n
w 50\n
m 0 9000 6000 50\n
m 1 9000 11000 50\n
c\n
w 50\n
m 0 9000 7000 50\n
m 1 9000 10000 50\n
c\n
w 50\n
u 0\n
u 1\n
c\n
"""

with safe_connection(_DEVICE_ID) as conn:
    #conn.send(_OPERATION4)
    conn.send(_ZoomOut)
    #conn.send(_OPERATION3)
    #conn.send(_OPERATION4)
    #conn.send(_OPERATION5)
