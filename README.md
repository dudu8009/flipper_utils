# Flipper Utils

## Usage: 
drop the [flipper\_ir\_update.py](./scripts/flipper_ir_update.py) in to the scripts directory in your firmware repo, connect the flipper via usb, and run the following command from the root of the firmware

`python ./scripts/flipper_ir_update.py path/to/IRDB/repo/`

if there is no repo located, it will clone the [IRDB](https://github.com/Lucaslhm/Flipper-IRDB) to the directory and transfer the relevent files to the flipper. 

if the repo exists it will update it and transfer the relevent files to the flipper.