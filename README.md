# Observer for 3D printer TRex for Home Assistant

Component for Home Assistant that lets you observe the status of your 3D Printer. 
Currently it works for the following Printers:
- Bresser T-Rex
As the software seems to be similar the following printers could also work if they can be connected via Wifi:
- Bresser Rex
- Bresser Raptor
- Most Bresser printer
- Flashforge Creator
- Flashforge Finder
- Most other Flashforge printer

## HACS Installation
1. Go to the HACS integration of your Home Assistant.
2. Click on Integration.
3. Click on the 3 dots in the upper right und choose Custom Repositories.
4. Copy the Link of this repository in the field repository, category Integration and click add.
5. You now have the card 3D Observer in your integrations. 
6. Dont forget to restart after you installed it.

## Configuration

Note that this integration yield a platform for sensors so you need to configure this as a sensor.

| Name          | Required | Description                                                           |
| ------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| ip_address       | no     | The IP Address of your printer as a string. Default is 192.168.178.98.  |
| port      | no     | The port that your printer uses. Default is 8899 |
| scan_interval | no       | not implemented yet but to change the scan intervall of the status |


## Sample Configuration
```yaml
sensor:
  - platform: observer
    ip_address: 192.168.178.1
    port: 1234
```

### Sensors
After the configuration was successfull a number of sensors is created with a prefix of '3d_print_'. Most importantly:
- Name: Name of the printer
- percentage: Percecntage of printed bits.
- t0_actual and t0_target: current temperature and target temperature of left nozzle.
- t1_actual and t1_target: current temperature and target temperature of right nozzle.
- b_actual and b_target: current temperature and target temperature of bed.


