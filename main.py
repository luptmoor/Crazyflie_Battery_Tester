import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.position_hl_commander import PositionHlCommander

def chn(id: str) -> str:
    ID = int(id);
    if ID <= 0: print('Invalid Radio Address! Must be between 01 and 40!');
    elif ID <=  8: return  '20';
    elif ID <= 16: return  '40';
    elif ID <= 24: return  '60';
    elif ID <= 32: return  '80';
    elif ID <= 40: return '100';
    else: print('Invalid Radio Address! Must be between 01 and 40!');

    return 0;


# URI to the Crazyflie to connect to
ID = input('Enter CF ID (01 - 40):');
uri = 'radio://0/' + chn(ID) + '/2M/247E0000' + ID;
print(uri);

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def simple_log(scf, logconf):

    with SyncLogger(scf, logconf) as logger:

        for log_entry in logger:

            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' % (timestamp, logconf_name, data))

            break
...

def log_vbat(logger):
    for log_entry in logger:
        print('V_bat: ', round(log_entry[1]['pm.vbat'], 2), 'V');
        break;
    return 0;

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_bat= LogConfig(name='Battery', period_in_ms=10)
    lg_bat.add_variable('pm.vbat', 'float')


    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        with SyncLogger(scf, lg_bat) as logger:
            
            log_vbat(logger);
            time.sleep(1.0);

            commander = PositionHlCommander(scf);
            commander.take_off(1.0, 1.0);
            commander.go_to(0, 0, 1, 1.0);

            time.sleep(2);
            log_vbat(logger);
            time.sleep(1.0);
            commander.land();