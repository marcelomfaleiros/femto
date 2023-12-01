import newport_smc100cc as smc100
import time
smc = smc100.SMC100CC()
smc.initialize()

'''print(smc.current_position())
smc.move_abs_mm(60)
print(smc.current_position())

smc.rs232_close()'''