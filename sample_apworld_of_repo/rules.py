import math
from typing import TYPE_CHECKING, Dict, List
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from BaseClasses import CollectionState

from .options import REPOGameOptions
from .names import location_names as lname
from .names import item_names as iname
from .names import region_names as rname
from .locations import level_types, location_table, pelly_list
from . import logic
#import logic

if TYPE_CHECKING:
    from . import REPOWorld

#forkless_easy_skills: List[str] = {

#}

#forkless_hard_skills: List[str] = {
  
#}



def set_region_rules(world: "REPOWorld") -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options
    
    # ---- Levels are locked behind Level Items ----
    multiworld.get_entrance(f"{rname.menu} -> {rname.headman}", player).access_rule = \
lambda state: state.has(iname.headman_lvl, player)
    
    multiworld.get_entrance(f"{rname.menu} -> {rname.mcjannek}", player).access_rule = \
lambda state: state.has(iname.mcjannek_lvl, player)
    
    multiworld.get_entrance(f"{rname.menu} -> {rname.swiftbroom}", player).access_rule = \
lambda state: state.has(iname.swiftbroom_lvl, player)
    
    multiworld.get_entrance(f"{rname.menu} -> {rname.museum}", player).access_rule = \
lambda state: state.has(iname.museum_lvl, player)  

def set_location_rules(world: "REPOWorld") -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    pellys = (pelly for pelly in location_table if location_table[pelly].location_group.__contains__("Pelly"))
    valuables = (val for val in location_table if location_table[val].location_group.__contains__("Valuable"))
    monster_souls = (soul for soul in location_table if location_table[soul].location_group.__contains__("Soul"))
    #Set Completion Condition to Victory Event
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

    #Set Logic for Victory Location
    add_rule(multiworld.get_location("Victory",player),
        lambda state: state.has_all({iname.headman_lvl,iname.mcjannek_lvl,iname.swiftbroom_lvl,iname.museum_lvl},player))
    
    # ---- Pelly Logic ----
    #Player Should be able to reach all Pellys
    for pelly in pellys:
        if (options.pelly_spawning == True or any(map(pelly.__contains__,options.pellys_required))):

            #Victory for spawned pellys
            add_rule(multiworld.get_location("Victory",player), lambda state, pell=pelly: state.can_reach_location(pell, player))
            
            #Rules for Pelly by Location
            if (pelly.__contains__("Swiftbroom Academy")):
                print("SBA Pelly Added")
                set_rule(multiworld.get_location(pelly,player),
                    lambda state: state.can_reach(multiworld.get_region(rname.swiftbroom,player),player=player))
            if (pelly.__contains__("Headman Manor")):
                print("HM Pelly added")
                set_rule(multiworld.get_location(pelly,player),
                    lambda state: state.can_reach(multiworld.get_region(rname.headman,player),player=player))
            if (pelly.__contains__("McJannek Station")):
                print("McJ Pelly added")
                set_rule(multiworld.get_location(pelly,player),
                    lambda state: state.can_reach(multiworld.get_region(rname.mcjannek,player),player=player))
            if (pelly.__contains__("Museum of Human Art")):
                print("Museum Pelly added")
                set_rule(multiworld.get_location(pelly,player),
                    lambda state: state.can_reach(multiworld.get_region(rname.museum,player),player=player)) 
            #Rules for Pelly by Type
            if pelly.__contains__("Gold"):
                add_rule(multiworld.get_location(pelly,player),
                    lambda state: state.has(iname.strength_up,player,3))    
    
    # ---- Valuable Logic ----
    for valuable in valuables:        
        #Victory if valuable hunt is enabled
        if options.valuable_hunt:
            add_rule(multiworld.get_location("Victory",player), lambda state, val=valuable: state.can_reach_location(val,player))

        #Valuable rules based on weight
        weight = location_table[valuable].location_group
        if weight.__contains__("VeryHeavy"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,4))
        elif weight.__contains__("Heavy++"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,3))
        elif weight.__contains__("Heavy+"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,3))
        elif weight.__contains__("Heavy"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,2))
        elif weight.__contains__("Medium+++"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,2))
        elif weight.__contains__("Medium++"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,1))
        elif weight.__contains__("Medium+"):
            add_rule(multiworld.get_location(valuable,player), lambda state: state.has(iname.strength_up,player,1))
        
    # ---- Monter Soul Logic ----
    easy_combat_items = {iname.grenade,iname.human_grenade,iname.duct_taped_grenade,iname.explosive_mine,iname.shotgun,iname.gun,iname.pulse_pistol,iname.photon_blaster,iname.cart_cannon,iname.cart_laser}
    medium_combat_items = {iname.baseball_bat,iname.frying_pan,iname.sledge_hammer,iname.sword}

    

    for soul in monster_souls:        
        #Victory if monster hunt is enabled
        if options.monster_hunt:
            add_rule(multiworld.get_location("Victory",player), lambda state, s=soul: state.can_reach_location(s,player))   

        if options.combat_logic.value == options.combat_logic.option_easy:
            add_rule(multiworld.get_location(soul,player), lambda state: state.has_any(easy_combat_items,player))

        elif options.combat_logic.value == options.combat_logic.option_medium:
            add_rule(multiworld.get_location(soul,player), lambda state: (state.has_any(medium_combat_items.union(easy_combat_items),player)) or state.has(iname.strength_up,player,13))

    # ---- Shop Logic ----
    for loc_name in location_table:
        print(f"Shop Upgrade total: {int(options.shop_upgrade_total.value)}\n Location id: {location_table[loc_name].location_id_offset}")
        if location_table[loc_name].location_id_offset != None and location_table[loc_name].location_id_offset > int(options.shop_upgrade_total.value):
            continue

        if loc_name.__contains__(lname.upgrade_pur):
            stockItemsRequired = math.ceil( (location_table[loc_name].location_id_offset - options.shop_stock) / options.shop_stock)
            print(f"Adding rule for {loc_name} requiring {stockItemsRequired} stock")
            if stockItemsRequired > 0:
                set_rule(multiworld.get_location(loc_name,player),
                    lambda state, requiredStockUps=stockItemsRequired: state.has(iname.shop_stock,player,requiredStockUps))

    #set_rule(multiworld.get_location())


#logic.set_options(world.options)




  
