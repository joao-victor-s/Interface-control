#files to test any problems that was find in the project
#02/08/22: solving the problems with heritage
import can
import mug
can = can.can("caneca")
mug = mug.mug("mug")
can.setId(132)

print(can.getId())
print(can.decode("isso aqui é "))
print(can.getS()) #this should be working on the project was well
print(mug.getS())