import newport_smc100cc as smc100
import time
smc = smc100.SMC100CC()
smc.rs232_set_up()
#smc.initialize()

smc.move_rel_mm(-80)

smc.rs232_close()
