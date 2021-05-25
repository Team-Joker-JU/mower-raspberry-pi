# Mower Raspberry pi

## Connect to robot
Run program
`/mower-raspberry-pi/src/main.py ARG1 ARG2`
<table border=1>
    <tr>
            <th>Name</th>
            <th>Description</th>
    </tr>
    <tr>
            <td>ARG 1</td>
            <td>Port that raspberry pi is connected to, for us its often `/dev/ttyUSB0`</td>
    </tr>
    <tr>
            <td>ARG 2</td>
            <td>Baudrate, for example `115200` is often used in our case</td>
    </tr>
</table>

## When Raspberry pi receives power
`/mower-raspberry-pi/src/main.py /dev/ttyUSB0 115200`<br>
is executed and the raspberry is ready to connect with bluetooth