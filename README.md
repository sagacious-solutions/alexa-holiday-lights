
### Current Skills

<table>
<tr>
<td>turn off lights</td>
<td>turnOffIntent</td>    
<td>light_loop.set_static_lights(xmasTree.setSolid, {"color": LedColor.black})</td>
</tr>
<tr>
<td>Start Rainbow Chase</td>
<td>setRainbowChaseIntent</td>
<td>light_loop.set_looping_pattern(xmasTree.rainbowCycle)</td>
</tr>
<tr>
<td>start slow color changing</td>
<td>slowRandomTransitionIntent</td>    
<td>light_loop.set_looping_pattern(
        xmasTree.transition_to_random_color, {"wait_after_transition_ms": 1}
    )</td>
</tr>
<tr>
<td>solid random colors</td>
<td>solidRandomIntent</td>    
<td>light_loop.set_static_lights(xmasTree.random_colors)</td>
</tr>
</table>
