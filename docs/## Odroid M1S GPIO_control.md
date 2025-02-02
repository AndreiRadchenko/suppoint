## Odroid M1S GPIO_control 

Supervized HA instalation on host: `/usr/share/hassio/homeassistant`

[Odroid GPIO pinouts](https://wiki.odroid.com/odroid-m1s/hardware/expansion_connectors) | [Command line tools](https://docs.radxa.com/en/rock5/rock5c/app-development/gpiod)

[libgpiod docs](https://libgpiod.readthedocs.io/en/latest/python_line.html#gpiod.line.Bias) | [gpiod lyb python examples](https://github.com/brgl/libgpiod/blob/master/bindings/python/examples/watch_line_value.py)

[Home Assistant Developer](https://developers.home-assistant.io/docs/development_environment) | [Custom component creating tutorial](https://community.home-assistant.io/t/tutorial-for-creating-a-custom-component/204793)

<img src='./img/Screenshot from 2025-02-02 16-41-52.png' width='600px'>

#### Naming conventions

There are usually 5 groups (also called banks) of GPIOs on the Rockchip platform: GPIO0 ~ GPIO4 (varies from chip to chip), each group has 32 GPIOs. Each group of GPIOs is divided into 4 groups, A/B/C/D, with 8 GPIOs in each group (0~7, also called bank_idx). rockchip.h)). So the GPIOs can be named from GPIO0_A0 to GPIO4_D7. Taking GPIO3_C5 as an example, we can deduce that its bank is 3 and its bank_idx is 21, i.e. GPIO3_C5 is the 21st GPIO in group 3.

#### Correspondence to libgpiod

The GPIO bank of Rockchip platform corresponds to gpiochip in libgpiod, and bank_idx corresponds to gpio line. Take GPIO3_C5 as an example, it is in libgpiod, gpiochip is 3 and line is 21.

### 1. Install Home Assistant GPIO Support

Since Odroid M1S uses GPIO similar to Raspberry Pi, you need a suitable Python library to interface with GPIO pins. For this task, the RPi.GPIO library doesn’t work, but lgpio or libgpiod will.

Install Required Packages

SSH into your Odroid M1S:

```bash
sudo apt update
sudo apt install python3-libgpiod libgpiod-dev
```

Install the Python GPIO Library

```bash
pip3 install gpiod
```

### 2. Create a Custom Component in Home Assistant

`custom_components/gpio_control`

Add to the configuration.yaml:

```yml 
sensor:
  - platform: gpio_control  
```