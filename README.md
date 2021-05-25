# Mower Raspberry pi

## Dependencies
<table border=1>
    <tr>
        <th>Name</th>
        <th>Terminal command</th>
        <th>Download link</th>
    </tr>
    <tr>
        <td>blepy</td>
        <td>pip install blepy</td>
        <td>https://pypi.org/project/blepy/</td>       
    </tr>
    <tr>
        <td>python-bluezero</td>
        <td>pip install bluezero</td>
        <td>https://github.com/ukBaz/python-bluezero</td>
    </tr>
    <tr>
        <td>argparse</td>
        <td>pip install argparse</td>
        <td>https://docs.python.org/3/library/argparse.html</td>
    </tr>
</table>

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