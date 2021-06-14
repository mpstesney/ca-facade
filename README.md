# ca-facade

Carnegie Mellon University, School of Architecture <br>
Generative Systems for Design, Fall '19 <br>
Assignment 3: from rule-based to agent-based modeling

Project team: <br>
Michael Stesney <br>
Aprameya Pandit <br>

<img src="https://user-images.githubusercontent.com/27044210/121946397-1d52c080-cd12-11eb-985e-106e7f2aac82.jpg" alt="Operable shade states" width="500" />

### Project description
Our model uses the behavior of a forest fire CA to open and close sunshade elements on the Hunt Library facades. Each sunshade on the façade maps to a cell in the same relative location within the CA matrix. Each cell has three discrete states, 0, 1 or 2, representing barren, treed or on fire, respectively. On the façade a cell state of 0 creates a 50% open sunshade, a cell state of 1 creates a 100% open sunshade and a cell state of 2 closes the sunshade completely. The shading device position obviously cannot change instantaneously. To translate between a discrete computational state and a physical movement that requires time, the CA cell matrix is not updated on every computational loop. Consequently, if a cell state change initiates a new sunshade position, the shade has time to move into position before the cell matrix is evaluated again.

The CA initiates with a random distribution of treed and barren cells. However, the initial state is of limited importance since the building façade will perform continuously uninterrupted day and night once initiated. Cell states change by random probability without regard of neighboring cell states with one exception. A burning cell in a cell's Von Neumann neighborhood raises the probability of that cell also catching fire. Cell state transitions occur in one direction only, 0 to 1 to 2 to 0 again. For example, it is not possible to change state from 2 to 1 without transitioning through the 0 state.

The façade interacts with the environment by responding to solar radiation striking individual cell locations. To translate radiation quantity, a "combustibility" attribute was added to the cell definition. The combustibility of a cell is directly proportional to the solar radiation impacting it. Higher combustibility increases the likelihood that a treed cell will ignite from a lightning strike or an adjacent burning cell. It also reduces the chance that a burning cell will extinguish. CA behavior involving more burning and barren cells will close more sunshades and increase overall façade shading. Conversely, at night, combustibility will be low, limiting the spread of lighting strike fires and resulting in a façade with limited shading.

### Use of the model
For the sake of this exercise, it is assumed that a future user will not want to create a new interactive façade for the Hunt Library and will have model geometry to import. As mentioned above in this report, for the emergent patterns of a forest fire CA to be evident, a large quantity of cells is required. A user should start by subdividing their geometry into the maximum number of cells that work with the architectural order of the façade.

Next a user should determine the desired average position of the sunshades on an average day. The probability and combustibility variables are adjusted to achieve this. The current state display in the model is helpful for evaluating adjustments. The state values available to be displayed within the cells are also helpful. The timing of state change and speed of transition between positions is adjusted with the delay variable. A user can adjust the transition from barely perceptible to easily noticeable. However, the cycle of transitions will impact the progression of the emergent patterns and by extension the ability of those patterns to respond to changing solar radiation levels.

Finally, a user must decide how much the varied solar radiation striking the facade throughout the day will guide the behavior of the CA. This is controlled with the cell combustibility thresholds. Of the possible user inputs, the probability values that control the state transition will be the most difficult to adjust well. Because all user adjustments are interrelated, trial and error will be unavoidable.
