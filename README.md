# 7drl


progress through the http://rogueliketutorials.com/tutorials/tcod/v2/

currently finished part 9

keep updated in github for practice in rcparke/7drl then adjust the engine to suit my goals


## activating venv through powershell:

- cd\

- 7drl\scripts\activate.ps1

- cd 7drl

- python main.py

- start editing with visual studio code


## potential future changes:

change line of sight implementation

- maybe repurpose the LoS code for visual targeting?
- having done the targeting in chapter 9, I think I will want my implementation to be more universal
  - simple single square targeting, that can then support area attacks that effect entities in an area
  - maybe a single RangedAttackHandler (PlayerTargetHandler maybe?) that supports a visual of potential targeting range, and targeting area on cursor, if called for

adjust map generation

- the tutorials implementation has corridors between rooms generated in the random order the rooms are generated, resulting in corridors overlapping previous rooms and corridors
- will want a mix of predefined maps (like nethack quest levels), and predefined rooms in addition to the classic rectangle room

implement spell system (much easier said than done)

- card/deck/draw based inspired by noita
- probably dont have wrapping
- turn based, how will I make the spellcasting system work within a turn
  - brainstorming ideas:
  - mana system, partially regenerate mana pool each turn, restricts casting more than total mana in a turn, as well as turn delay between casts to recharge mana
  - spell cast delay system, where each spell has a given cast delay, and you can only cast up to a certain total cast delay per turn
  - spellbook spell slot capacity
  - the cast delay per turn restriction, and mana total/regen restrictions, could be local to each spellbook item along with the spellbook's spell slot capacity

implement items

- evocable items that arent consumables
- evocable items that use charges before consumption
- evocable spellbook items that tie into the spell system
- spell items (like noita)?
