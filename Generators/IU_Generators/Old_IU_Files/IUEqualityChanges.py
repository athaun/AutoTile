import UniversalClasses as uc
from UniversalClasses import State, Tile, Assembly, AffinityRule, TransitionRule, System
from Assets.colors import *
import sys
from Generators.IU_Generators.Old_IU_Files.states import GeneratedStates, ds_2, ds_3, ds_4, ds_5, ds_6, ds_7, ds_8, ds_9
from Generators.IU_Generators.binaryStates import *

gsc = GeneratedStates()
gsd = gsc.states_dict



class IUGenerators_EC:
    all_states_dict = {}
    all_initial_states_dict = {}
    all_states_list = []
    all_seed_states_list = []
    all_seed_states_dict = {}
    all_aff_list = []
    all_aff_dict = {}
    all_tr_list = []
    all_tr_dict = {}
    all_sys = {}

    def __init__(self, exampleSysName=""):
        self.exampleSysName = exampleSysName
        self.genSys = None

        self.example_states_data = [north_prefix, start_state, ds_1, ds_2, ds_5, end_state]
        self.aff_list = []

    #To Do
    def setExampleData(self, data_string):
        self.example_states_data = data_string

    def setSampleDataStartCoords(self, x, y, dir):
        self.sampleTiles = []

        for i in range(0, len(self.example_states_data)):
            if dir == "V" or dir == "N" or dir == "S":
                self.sampleTiles.append(Tile(self.example_states_data[i], x, y + i))
            else:
                self.sampleTiles.append(Tile(self.example_states_data[i], x + i, y))

        return self.sampleTiles

    def basicWireSeedAssembly(self, dir_len_dict={"W": ((1, 0), (4, 0))}):
        # , "S": ((-7, -2), (-7, -6))

        if "W" in dir_len_dict.keys():
            wireState = westWire
            k = "W"
        elif "S" in dir_len_dict.keys():
            wireState = southWire
            k = "S"
        elif "E" in dir_len_dict.keys():
            wireState = eastWire
            k = "E"
        elif "N" in dir_len_dict.keys():
            wireState = northWire
            k = "N"

        start_end_coords = dir_len_dict[k]

        start_x = start_end_coords[0][0]
        start_y = start_end_coords[0][1]
        end_x = start_end_coords[1][0]
        end_y = start_end_coords[1][1]

        wa_seed_states = [wireState]
        wa_seed_tiles = []

        if start_x == end_x:
            for i in range(start_y, end_y + 1):
                wa_seed_tiles.append(Tile(wireState, start_x, i))
            example_tiles = self.setSampleDataStartCoords(end_x, end_y + 1, "V")
        elif start_y == end_y:
            for i in range(start_x, end_x + 1):
                wa_seed_tiles.append(Tile(wireState, i, start_y))
            example_tiles = self.setSampleDataStartCoords(end_x + 1, end_y, "H")

        wa_seed_tiles = wa_seed_tiles + example_tiles

        asb = Assembly()
        asb.setTiles(wa_seed_tiles)
        return asb, wa_seed_states, wa_seed_tiles

    def basicWireGenerator(self):
        asb, wa_seed_states, wa_seed_tiles = self.basicWireSeedAssembly()

        #System takes in temp, states, initial states, seed states, vertical_affinitys, horizontal_affinitys, vert transitions, horiz transitions, tile vertical transitions, tile horizontal transitions, seed assembly
        genSys = System(1, wa_seed_states, [], wa_seed_states,  [], [], [], [], [], [], asb)
        wire_stuff = self.wireAffinities()

        wire_tr = wire_stuff[0]
        wire_affs = wire_stuff[1]
        if len(wire_stuff) == 3:
            wire_st = wire_stuff[2]
            for i in wire_st:
                self.addSeedStateToIUSys(i)
                genSys.addSeedState(i)

        print("Wire TR length: ", len(wire_tr))
        print("Wire Affs length: ", len(wire_affs))

        for i in wire_tr:
            self.addToAllTr(i)
            genSys.addTransitionRule(i)



        for a in wire_affs:
            self.addToAllAff(a)
            genSys.addAffinity(a)




        self.all_sys["basicWire"] = genSys

        return genSys

    def wireAffinities(self, gsys=None):
        wire_affs = []
        wire_tr = []
        wire_st = []
        if gsys is None:
            gsys == self.genSys

        if gsys is not None:
            for ds in data_states_list_all_with_prefixes_no_order:
                gsys.addSeedState(ds)
                for i in wire_states:
                    gsys.addSeedState(i)

                    if i.label == "westWire" or i.label == "westProtectedWire":
                        aff = AffinityRule(i.label, i.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(i.label, ds.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(ds.label, i.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        tr = TransitionRule(i.label, ds.label, ds.label, i.label, "h")
                        wire_tr.append(tr)
                        gsys.addTransitionRule(tr)
                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "v", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                    elif i.label == "eastWire" or i.label == "eastProtectedWire":
                        aff = AffinityRule(i.label, i.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(i.label, ds.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(ds.label, i.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        tr = TransitionRule(ds.label, i.label, i.label, ds.label, "h")
                        wire_tr.append(tr)
                        gsys.addTransitionRule(tr)

                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "v", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                    elif i.label == "northWire" or i.label == "northProtectedWire":
                        aff = AffinityRule(i.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(ds.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        tr = TransitionRule(i.label, ds.label, ds.label, i.label, "v")
                        wire_tr.append(tr)
                        gsys.addTransitionRule(tr)

                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "h", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                            aff = AffinityRule(border_state.label, i.label,  "h", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)

                    elif i.label == "southWire" or i.label == "southProtectedWire":
                        aff = AffinityRule(i.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)
                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)
                        aff = AffinityRule(ds.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        tr = TransitionRule(ds.label, i.label, i.label, ds.label, "v")
                        wire_tr.append(tr)
                        gsys.addTransitionRule(tr)

                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "h", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                            aff = AffinityRule(border_state.label, i.label,  "h", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)

                    elif i.label == "northEastWire" or i.label == "northEastProtectedWire":
                        aff = AffinityRule(i.label, northWire.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(i.label, eastWire.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(i.label, ds.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(eastWire.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        tr = TransitionRule(eastWire.label, i.label, i.label, northWire.label, "v")
                        wire_tr.append(tr)
                        gsys.addTransitionRule(tr)

                        if "Protected" in i.label:
                            aff = AffinityRule(border_state.label, i.label,  "h", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)

                    elif i.label == "northWestWire" or i.label == "northWestProtectedWire":
                        aff = AffinityRule(i.label, northWire.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(westWire.label, i.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(ds.label, i.label, "h", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        aff = AffinityRule(westWire.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        gsys.addAffinity(aff)

                        tr = TransitionRule(westWire.label, i.label, i.label, northWire.label, "v")
                        wire_tr.append(tr)
                        gsys.addTransitionRule(tr)

                        """ tr = TransitionRule(i.label, westWire.label, i.label, northWire.label, "v")
                        wire_tr.append(tr)
                        self.genSys.addTransitionRule(tr) """

                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "h", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)
                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)
                            gsys.addAffinity(aff)

        else:
            wire_st.append(border_state)

            for ds in data_states_list_all_with_prefixes_no_order:
                if ds not in wire_st:
                    wire_st.append(ds)

                for i in wire_states:
                    if i not in wire_st:
                        wire_st.append(i)

                    print(i.label)
                    if i.label == "WestWire" or i.label == "WestProtectedWire":
                        print("This Works")
                        aff = AffinityRule(i.label, i.label, "h", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(i.label, ds.label, "h", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(ds.label, i.label, "h", 1)
                        wire_affs.append(aff)

                        tr = TransitionRule(i.label, ds.label, ds.label, i.label, "h")
                        wire_tr.append(tr)

                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "v", 1)
                            wire_affs.append(aff)

                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)

                    elif i.label == "EastWire" or i.label == "EastProtectedWire":
                        aff = AffinityRule(i.label, i.label, "h", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(i.label, ds.label, "h", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(ds.label, i.label, "h", 1)
                        wire_affs.append(aff)

                        tr = TransitionRule(ds.label, i.label, i.label, ds.label, "h")
                        wire_tr.append(tr)


                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "v", 1)
                            wire_affs.append(aff)

                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)

                    elif i.label == "NorthWire" or i.label == "NorthProtectedWire":
                        aff = AffinityRule(i.label, i.label, "v", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(ds.label, i.label, "v", 1)
                        wire_affs.append(aff)

                        tr = TransitionRule(i.label, ds.label, ds.label, i.label, "v")
                        wire_tr.append(tr)


                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "h", 1)
                            wire_affs.append(aff)

                            aff = AffinityRule(border_state.label, i.label,  "h", 1)
                            wire_affs.append(aff)


                    elif i.label == "SouthWire" or i.label == "SouthProtectedWire":
                        aff = AffinityRule(i.label, i.label, "v", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)
                        aff = AffinityRule(ds.label, i.label, "v", 1)
                        wire_affs.append(aff)
                        tr = TransitionRule(ds.label, i.label, i.label, ds.label, "v")
                        wire_tr.append(tr)


                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "h", 1)
                            wire_affs.append(aff)

                            aff = AffinityRule(border_state.label, i.label,  "h", 1)
                            wire_affs.append(aff)


                    """ elif i.label == "NorthEastWire" or i.label == "NorthEastProtectedWire":
                        aff = AffinityRule(i.label, northWire.label, "v", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(i.label, eastWire.label, "h", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(i.label, ds.label, "h", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(eastWire.label, i.label, "v", 1)
                        wire_affs.append(aff)


                        tr = TransitionRule(eastWire.label, i.label, i.label, northWire.label, "v")
                        wire_tr.append(tr)


                        if "Protected" in i.label:
                            aff = AffinityRule(border_state.label, i.label,  "h", 1)
                            wire_affs.append(aff)

                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff)
 """

                    """ elif i.label == "NorthWestWire" or i.label == "NorthWestProtectedWire":
                        aff = AffinityRule(i.label, northWire.label, "v", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(westWire.label, i.label, "h", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(i.label, ds.label, "v", 1)
                        wire_affs.append(aff)

                        aff = AffinityRule(ds.label, i.label, "h", 1)
                        wire_affs.append(aff)


                        aff = AffinityRule(westWire.label, i.label, "v", 1)
                        wire_affs.append(aff)


                        tr = TransitionRule(westWire.label, i.label, i.label, northWire.label, "v")
                        wire_tr.append(tr)




                        if "Protected" in i.label:
                            aff = AffinityRule(i.label, border_state.label, "h", 1)
                            wire_affs.append(aff)

                            aff = AffinityRule(border_state.label, i.label,  "v", 1)
                            wire_affs.append(aff) """

            print("Wires Other")
        return [wire_tr, wire_affs, wire_st]


    def wireAffinitiesTrOnlyUsed(self, used_states):



        used = used_states

        wire_tr = []
        wire_aff = []
        wires_used = [u for u in used if u in wire_states]
        ds_used = [u for u in used if u in data_states_list_all_with_prefixes_no_order]
        dirs = ["north", "south", "east", "west"]

        for d in ds_used:
            for w in wires_used:
                if dirs[0] in w.label.lower(): #North
                    aff = AffinityRule(w.label, w.label, "v", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(w.label, d.label, "v", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(d.label, w.label, "v", 1)
                    wire_aff.append(aff)
                    tr = TransitionRule(w.label, d.label, d.label, w.label, "v") #North
                    wire_tr.append(tr)
                elif dirs[1] in w.label.lower(): #South
                    aff = AffinityRule(w.label, w.label, "v", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(w.label, d.label, "v", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(d.label, w.label, "v", 1)
                    wire_aff.append(aff)
                    tr = TransitionRule( d.label, w.label, w.label, d.label, "v") #South
                    wire_tr.append(tr)
                elif dirs[2] in w.label.lower(): #East
                    aff = AffinityRule(w.label, w.label, "h", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(w.label, d.label, "h", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(d.label, w.label, "h", 1)
                    wire_aff.append(aff)
                    tr = TransitionRule( d.label, w.label, w.label, d.label, "h") #East ->
                    wire_tr.append(tr)
                elif dirs[3] in w.label.lower():
                    aff = AffinityRule(w.label, w.label, "h", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(w.label, d.label, "h", 1)
                    wire_aff.append(aff)
                    aff = AffinityRule(d.label, w.label, "h", 1)
                    wire_aff.append(aff)
                    tr = TransitionRule( w.label,  d.label, d.label, w.label, "h") #West <-
                    wire_tr.append(tr)
                else:
                    print("Error in wireAffinitiesTrOnlyUsed")

        return [wire_aff, wire_tr]
    def addStateToIUSys(self, state):
        if state.label not in self.all_states_dict.keys():
            self.all_states_dict[state.label] = state

    def addSeedStateToIUSys(self, state):
        if state.label not in self.all_seed_states_dict.keys():
            self.all_seed_states_dict[state.label] = state
            self.addStateToIUSys(state)

        else:
            print("Seed State already exists in system")

    def addToAllAff(self, aff):
        if aff not in self.all_aff:
            self.all_aff_list.append(aff)

    def addToAllTr(self, tr):
        if tr not in self.all_tr:
            self.all_tr_list.append(tr)

    def addToAllStates(self, state):
        if state not in self.all_states_list:
            self.all_states_list.append(state)

    def addToAllSeedStates(self, state):
        if state not in self.all_seed_states_list:
            self.all_seed_states_list.append(state)

    def protectedWireBuild(self):
        pass

    def equalityEndCap(self):
        bw_gs = self.basicWireGenerator()

    def macroCellCopyNorthTiles(self):
        tile_list_cg = []

        ds = [start_state_pair, north_prefix, start_state, ds_0, ds_1, ds_0, end_state,
              south_prefix, start_state, start_state_pair, end_state_pair]
        seed_states_used_cg = ds + [northCopyWire, northCopyDoorInactive, northCopyDoorHandleInactive,         endcap_door_west_inactive, border_state, westWire, southWire, verticalMacroCellDoorOpenSignal]

        for i in range(0, 16):
            if i < 15 and i > 0:
                t = Tile(northCopyWire, i, 0)
                tile_list_cg.append(t)

                t = Tile(northCopyDoorInactive, i, -1)
                tile_list_cg.append(t)

                d = Tile(ds[i-1], i, -2)
                tile_list_cg.append(d)

            else:
                h = Tile(northCopyDoorHandleInactive, i, -1)
                tile_list_cg.append(h)

                if i == 0:
                    d = Tile(endcap_door_west_inactive, i, 0)
                    tile_list_cg.append(d)
                elif i == 15:
                    b = Tile(check_for_any_end_cap, i, 0)
                    tile_list_cg.append(b)
                b = Tile(border_state, i, -2)
                tile_list_cg.append(b)

            b = Tile(border_state, i, -3)
            tile_list_cg.append(b)

            b = Tile(border_state, i, 1)
            tile_list_cg.append(b)


        t = Tile(verticalMacroCellDoorOpenSignal, -1, -1)
        tile_list_cg.append(t)

        for i in range(1, 4):
            t = Tile(southWire, -1, i)
            tile_list_cg.append(t)

            t = Tile(westWire, -i, 0)
            tile_list_cg.append(t)

        return tile_list_cg, seed_states_used_cg

    def macroCellCopyNorthAffsTrs(self, states):
        affs = []
        trs = []
        ds_used = [u for u in states if u in data_states_list_all_with_prefixes_no_order]

        for ds_state in ds_used:
            aff = AffinityRule(northCopyWire.label, ds_state.label, "v", 1)
            affs.append(aff)
            aff = AffinityRule(ds_state.label, northCopyWire.label, "v", 1)
            affs.append(aff)

            tr = TransitionRule(northCopyWire.label, ds_state.label, ds_state.label, ds_state.label, "v")
            trs.append(tr)

            aff = AffinityRule(northCopyDoor.label, ds_state.label, "v", 1)
            affs.append(aff)

            aff = AffinityRule(northCopyDoorInactive.label, ds_state.label, "v", 1)
            affs.append(aff)

            tr = TransitionRule(northCopyDoor.label,     ds_state.label, ds_state.label, ds_state.label, "v")
            trs.append(tr)


        aff = AffinityRule(northCopyDoorHandle.label,northCopyDoor.label, "h", 1)
        affs.append(aff)

        aff = AffinityRule(northCopyDoorHandle.label,northCopyDoorInactive.label, "h", 1)
        affs.append(aff)

        aff = AffinityRule(northCopyDoorHandle.label, northCopySeriesCheckEast.label, "h", 1)
        affs.append(aff)

        aff = AffinityRule(northCopySeriesCheckEast.label, northCopyDoorInactive.label, "h", 1)
        affs.append(aff)

        aff = AffinityRule(northCopyDoor.label, northCopySeriesCheckEast.label, "h", 1)
        affs.append(aff)


        tr = TransitionRule(northCopyDoorHandle.label, northCopyDoorInactive.label, northCopyDoorHandle.label, northCopySeriesCheckEast.label, "h")
        trs.append(tr)

        tr = TransitionRule(northCopySeriesCheckEast.label, northCopyDoorInactive.label, northCopyDoor.label, northCopySeriesCheckEast.label, "h")
        trs.append(tr)


        aff = AffinityRule(northCopyDoorHandleInactive.label, northCopyDoorInactive.label, "h", 1)
        affs.append(aff)

        aff = AffinityRule(verticalMacroCellDoorOpenSignal.label, northCopyDoorHandleInactive.label, "h", 1)
        affs.append(aff)

        aff = AffinityRule(verticalMacroCellDoorOpenSignal.label, northCopyDoorHandle.label, "h", 1)
        affs.append(aff)

        tr = TransitionRule(verticalMacroCellDoorOpenSignal.label, northCopyDoorHandleInactive.label, verticalMacroCellDoorOpenSignal.label, northCopyDoorHandle.label, "h")
        trs.append(tr)

        return [affs, trs]

    def macroCellNorthTiles2(self):
        tile_list_cg = []

        ds = [start_state_pair, north_prefix, start_state, ds_0, ds_1, ds_0, end_state,
              south_prefix, start_state, start_state_pair, end_state_pair]
        ds_write_states = [writeDoorInactive, writeStartStatePairInactive, writeNorthPrefixInactive, writeStartStateInactive, writeZeroInactive, writeOneInactive,
                           writeZeroInactive, writeEndStateInactive, writeSouthPrefixInactive, writeStartStateInactive, writeOneInactive,
                           writeZeroInactive, writeZeroInactive, writeEndStateInactive, writeEndStatePairInactive]

        seed_states_used_cg = ds_write_states + [endcap_door_west_inactive, border_state, westWire, southWire, verticalMacroCellDoorOpenSignal]

        for i in range(0, 16):
            if i < 15:
                if i == 0:
                    d = Tile(endcap_door_west_inactive, i-1, 0)
                    tile_list_cg.append(d)

                else:
                    t = Tile(westWire, i, 0)
                    tile_list_cg.append(t)

                t = Tile(ds_write_states[i], i, -1)
                tile_list_cg.append(t)

            else:
                b = Tile(check_for_any_end_cap, i, 0)
                tile_list_cg.append(b)

                b = Tile(border_state, i, -1)
                tile_list_cg.append(b)


            b = Tile(border_state, i, -2)
            tile_list_cg.append(b)

            b = Tile(border_state, i, 1)
            tile_list_cg.append(b)

        for i in range(2, 4):
            t = Tile(southWire, -1, i)
            tile_list_cg.append(t)

            t = Tile(westWire, -i, 0)
            tile_list_cg.append(t)

        return tile_list_cg, seed_states_used_cg

    def macroCellCopyNorthTest2(self):
        tiles = self.macroCellNorthTiles2()[0]
        seed_states = self.macroCellNorthTiles2()[1]
        states = []

    def macroCellCopyNorthTest(self):
        tiles = self.macroCellCopyNorthTiles()[0]
        seed_states = self.macroCellCopyNorthTiles()[1]
        states = [northCopyDoorHandle, endcap_door_west_active, northCopyDoor,
                  endcap_door_west_stop, northCopySeriesCheckEast] + seed_states
        affs = self.macroCellCopyNorthAffsTrs(states)[0]
        trs = self.macroCellCopyNorthAffsTrs(states)[1]

        assm = Assembly()
        assm.setTiles(tiles)
        genSystem = System(1, states, [], seed_states, [], [], [], [], [], [], assm)


        for a in affs:
            genSystem.addAffinity(a)

        for t in trs:
            genSystem.addTransitionRule(t)

        affs_tr_wire = self.wireAffinitiesTrOnlyUsed(genSystem.returnStates())
        affs2 = affs_tr_wire[0]
        tr2 = affs_tr_wire[1]
        for a in affs2:
            genSystem.addAffinity(a)
        for t in tr2:
            genSystem.addTransitionRule(t)
        return genSystem













## Basic Requirements for Boolean Circuit Simulation
### 1. Wires
        """
        This is done
        """
### 2.Turn and Delay

### 3. Signal Crossing
### 4. Gates
### 5. Fan-out


data_states_list_nums_only = [ds_0, ds_1, ds_2,ds_3, ds_4, ds_5, ds_6, ds_7, ds_8, ds_9]