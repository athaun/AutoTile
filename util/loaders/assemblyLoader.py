import xml.etree.ElementTree as ET

from UniversalClasses import State, Tile, Assembly
from UniversalClasses import AffinityRule
from UniversalClasses import TransitionRule

# System's Affinity Rules
VerticalAffinityRules = []
HorizontalAffinityRules = []
# System's Transition Rules
VerticalTransitionRules = []
HorizontalTransitionRules = []
SeedStateSet = []  # Used in SingleTile mode; States that were marked as potential seeds
# States marked as initial states; states that float around the system looking to attach to something.
InitialStateSet = []
CompleteStateSet = []  # All states in the system
seed_assembly = Assembly()

def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()

    # Record System Temp
    global Temp
    Temp = treeroot.get("Temp")

    # Record All States
    for state_tag in treeroot.findall('AllStates/State'):
        label = state_tag.get("Label")
        color = state_tag.get("Color")
        display_label = state_tag.get("DisplayLabel")
        display_label_color = state_tag.get("DisplayLabelColor")
        display_label_font = state_tag.get("DisplayLabelFont")
        rotate_display_label_degrees = state_tag.get("RotateDisplayLabelDegrees")

        if display_label is None:
            display_label = label
        if display_label_font is None:
            display_label_font = "Nerd Font"
        if display_label_color is None:
            display_label_color = "black"
        if rotate_display_label_degrees is None:
            rotate_display_label_degrees = 0

        tempState = State(label, color, display_label, display_label_color, display_label_font, rotate_display_label_degrees)

        CompleteStateSet.append(tempState)

    # Record Initial States
    for state_tag in treeroot.findall("InitialStates/State"):
        label = state_tag.get("Label")
        color = state_tag.get("Color")
        display_label = state_tag.get("DisplayLabel")
        display_label_color = state_tag.get("DisplayLabelColor")
        display_label_font = state_tag.get("DisplayLabelFont")

        rotate_display_label_degrees = state_tag.get("RotateDisplayLabelDegrees")

        if display_label is None:
            display_label = label
        if display_label_font is None:
            display_label_font = "Nerd Font"
        if display_label_color is None:
            display_label_color = "black"
        if rotate_display_label_degrees is None:
            rotate_display_label_degrees = 0

        tempState = State(label, color, display_label, display_label_color, display_label_font, rotate_display_label_degrees)

        InitialStateSet.append(tempState)

    # Record Seed States and make seed assembly
    for state_tag in treeroot.findall("SeedStates/State"):
        label = state_tag.get("Label")
        color = state_tag.get("Color")
        display_label = state_tag.get("DisplayLabel")
        display_label_color = state_tag.get("DisplayLabelColor")
        display_label_font = state_tag.get("DisplayLabelFont")

        x = state_tag.get("x")
        y = state_tag.get("y")

        if display_label is None:
            display_label = label
        if display_label_font is None:
            display_label_font = "Nerd Font"
        if display_label_color is None:
            display_label_color = "black"
        if rotate_display_label_degrees is None:
            rotate_display_label_degrees = 0

        tempState = State(label, color, display_label, display_label_color, display_label_font, rotate_display_label_degrees)
        SeedStateSet.append(tempState)

        if isinstance(x,str) & isinstance(y,str):
            seed_assembly.setTiles([Tile(tempState,int(x),int(y))])


    # Record Vertical Transitions
    for rule_tag in treeroot.findall("VerticalTransitions/Rule"):
        label1 = rule_tag.get("Label1")
        label2 = rule_tag.get("Label2")
        label1Final = rule_tag.get("Label1Final")
        label2Final = rule_tag.get("Label2Final")

        tempRule = TransitionRule(
            label1, label2, label1Final, label2Final, "v")
        VerticalTransitionRules.append(tempRule)

    # Record Horizontal Transitions
    for rule_tag in treeroot.findall("HorizontalTransitions/Rule"):
        label1 = rule_tag.get("Label1")
        label2 = rule_tag.get("Label2")
        label1Final = rule_tag.get("Label1Final")
        label2Final = rule_tag.get("Label2Final")

        tempRule = TransitionRule(
            label1, label2, label1Final, label2Final, "h")
        HorizontalTransitionRules.append(tempRule)

    # Record Vertical Affinities
    for rule_tag in treeroot.findall("VerticalAffinities/Rule"):
        label1 = rule_tag.get("Label1")
        label2 = rule_tag.get("Label2")
        strength = rule_tag.get("Strength")

        tempRule = AffinityRule(label1, label2, "v", strength)
        VerticalAffinityRules.append(tempRule)

    # Record Horizontal Affinities
    for rule_tag in treeroot.findall("HorizontalAffinities/Rule"):
        label1 = rule_tag.get("Label1")
        label2 = rule_tag.get("Label2")
        strength = rule_tag.get("Strength")

        tempRule = AffinityRule(label1, label2, "h", strength)
        HorizontalAffinityRules.append(tempRule)