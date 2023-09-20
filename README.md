# dynamic_foraging_setup

Circuit Schematics:
![schematics](https://github.com/PeihengLu/dynamic_foraging_setup/assets/59673259/d6acd3dd-36f4-4030-9722-dcaeab385a12)

Setup Image:
<img width="614" alt="setup" src="https://github.com/PeihengLu/dynamic_foraging_setup/assets/59673259/2d061fe4-aedd-4474-bdf7-83b91c1ae005">

Instead of a high-performance and heavily modified computer used in the PhenoSys rig, a Raspberry
Pi 4 was used to support this task, which significantly reduced the budget. The built-in
GPIO ports of Raspberry Pi also saved the trouble and expenses of modifying a PC to
transmit signals to and from various components of the tasks. The hardware components
used in this experiment and their connection details are described below.
• A is the raspberry pi controlling the experiment. It’s connected to two monitors.
Monitor M1 shows the animal and human operator the green cursor turned by
the wheel W, while monitor M2 (not available to the animal) provides some
performance tracking information to give the operator a visual representation of
the animals’ choices, similar to the one shown in Figure 1.3.
• B is the device head-fixing the mice during the task, it was designed independently
to be more suitable for 3D printing. The white mouse holder C was 3D printed
using the model from UCL. The black base D where C is mounted on was
purchased from RS according to the UCL specification of the task.
• The wheel W is connected to a 1024-tick rotary encoder mounted inside C. The
rotary encoder records the movement of wheels as ticks and sends them to the
raspberry pi, where the ticks are decoded into angular movement.
• Breadboard E has a simple circuit converting a 5v signal from the rotary encoder
into 3.3V, the recommended voltage for the GPIO port. A 9v power supply F
supplies the extra current needed to open the valve V and delivers the reward to
the animals since the GPIO ports are not capable of providing enough current to
drive any sort of motor. GPIO ports send signals to the transistors connecting the
power supply and the valve to control the opening and closing of the valve. And
finally, the water is delivered to the animal through sprout S

