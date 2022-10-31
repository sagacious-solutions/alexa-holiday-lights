
### Current Skills

<table>
    <tr>
        <th>Invocation Phrases</th>
        <th>Intent in Alexa Dash</th>
        <th>Loop Function</th>
        <th>Function Called / kwargs</th>
    </tr>
    <tr>
        <td>turn off lights</td>
        <td>turnOffIntent</td>    
        <td>No</td>    
        <td>light_string.setSolid, {"color": LedColor.black}</td>
    </tr>
    <tr>
        <td>Start Rainbow Chase</td>
        <td>setRainbowChaseIntent</td>
        <td>Yes</td>    
        <td>light_string.rainbowCycle</td>
    </tr>
    <tr>
        <td>start slow color changing</td>
        <td>slowRandomTransitionIntent</td>    
        <td>Yes</td>    
        <td>
            light_string.transition_to_random_color, {"wait_after_transition_ms": 1}
        </td>
    </tr>
    <tr>
        <td>solid random colors</td>
        <td>solidRandomIntent</td>    
        <td>No</td>    
        <td>light_string.random_colors</td>
    </tr>
</table>

## Hardware
<p>Current hardware is a Raspberry Pi 4 running off an NVMe SSD on USB3.0 for rapid prototyping. However once development is complete it will likely be moved to Raspberry Pi Zero W or other inexpensive SBC.</p>
<img src="./docs/pi4_hardware.jpg" width="50%" />

### RGB Lights
<img src="./docs/one_light.jpg" width="50%" />

### Pinout
<img src="./docs/pi_pinout.png" width="50%" />
<p>Image source <a href="https://pinout.xyz/">https://pinout.xyz/</a></p>