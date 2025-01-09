# cardcounting
Simulator of Hi-Lo card counting strategies.

## Supported game types
This is a WIP. Currently will support H17 games with no option for insurance, no DAS, and no re-splitting.

In the future, will support S17, insurance, DAS, and re-splitting.

## Deviations
Currently only supports basic strategy. Intend to add common deviations in the future, as well as mechanisms for users to define their own deviations.

## Usage
Change game rules and bet spreads in `config.py`.
Then, just run `sim.py`.

## Testing
Coming soon -- will run the simulator for tried-and-tested strategies to confirm that EV is the same as expected.