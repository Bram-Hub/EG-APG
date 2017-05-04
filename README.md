# ExistentialGraphProofGenerator
Automatedly generates existential graph proofs from a set of premises and a goal provided in propositional logic format.  Implements the [idea](http://www.cogsci.rpi.edu/~heuveb/Research/EG/details.html "EG Technical Details")  proposed by Bran van Heuveln in his Computability and Logic course at RPI. At the moment, the algorithm only handles valid arguments (does not prove invalidity directly) and has a method of outputting to terminal and an output file.  Future work will include handling Pegasus output which is another software developed by an RPI student that visualizes an existential graph proof.

## How to run the tool
In terminal and in the project folder, run:

`cd src`

`python generate.py <premise.txt> <goal.txt> -o <output-file.pega>`

premises.txt and goal.txt should contain well-formed logic statement (add parentheses around "NOT" and compound statements).

The majority of the terminal output is separated by "phases" in the algorithm from conversion to setup to consistency checking.  Intermediary trees will be displayed in a sideways format.  From top down, the tree goes from left to right.

## Grammar

    atoms are '[a-zA-Z]''
    not is '~''
    and is '&''
    or is '|''
    implication is '-''
    biconditional is '='
    contradiction is '!'
    left parenthesis is '('
    right parenthesis is ')'
    and the goal is prepended by '$'

## Example
  modus_ponens.txt:
  
      p-q
      p

  goal_example.txt:
      ```q```

## Pegasus format
Currently each line in Pegasus starts off with an action and two states: the start and end states.  Right now only pseudo-Pegasus output works.  That format is outputed to an output file that is either provided through command line or defaults to ```output.pega```.

    atoms : A...Z...0...9
    cuts: ()
    end of atom : |
    [-] : stuff in between brackets to be removed
    [+] : stuff in between brackets to be added
    [/] : keep everything in between these brackets
    [.] : notifies where the iteration is coming from

