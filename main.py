from Language.Parser.ast import FuncDef
from Language.Semantic.Type_checking.Context import Context
from Language.Semantic.Type_checking.Type import Type
from Visual.Console import execute

def build_initial_context():
    context = Context('root')
    Type(context, 'Number')
    Type(context, 'Bool')
    Type(context, 'String')
    Type(context, 'Void')
    Type(context, 'function')
    soldier = Type(context, 'Soldier')
    weapon = Type(context, 'Weapon')
    terrain = Type(context, 'Terrain')
    weather = Type(context, 'Weather')
    Type(context, 'List')
    Type(context, 'List Soldier')
    Type(context, 'List Number')
    Type(context, 'List Bools')
    Type(context, 'List String')
    Type(context, 'List Void')
    Type(context, 'List Weapon')
    Type(context, 'List Terrain')
    Type(context, 'List Weather')
    map = Type(context, 'Map')

    # SOLDIER
    soldier.add_attribute('health', 'Number')
    soldier.add_attribute('current_health', 'Number')
    soldier.add_attribute('vision_range', 'Number')
    soldier.add_attribute('precision', 'Number')
    soldier.add_attribute('move_speed', 'Number')
    soldier.add_attribute('crit_chance', 'Number')
    soldier.add_attribute('orientation', 'String')
    soldier.add_attribute('stance', 'String')
    soldier.add_attribute('max_load', 'Number')
    soldier.add_attribute('concealment', 'Number')
    soldier.add_attribute('melee_damage', 'Number')
    soldier.add_attribute('equipped_weapon', 'Weapon')

    soldier.define_function('get_map', 'Map', [], [])
    soldier.define_function('set_weapons', 'Void', ['weapons', 'magazines'], ['List Weapon', 'List Number'])
    soldier.define_function('set_affinity', 'Void', ['weapon_name', 'value'], ['String', 'Number'])
    soldier.define_function('set_position', 'Void', ['map', 'row', 'col'], ['Map', 'Number', 'Number'])
    soldier.define_function('set_equiped_weapon', 'Void', ['weapon'], ['String'])
    soldier.define_function('add_extra_action', 'Void', ['action'], ['function'])
    soldier.define_function('remove_extra_action', 'Void', ['index'], ['Number'])
    soldier.define_function('get_team', 'Number', [], [])
    soldier.define_function('is_ally', 'Bool', ['soldier'], ['Soldier'])


    # WEAPON
    weapon.add_attribute('name', 'String')
    weapon.add_attribute('weight', 'Number')
    weapon.add_attribute('w_effective_range', 'Number')
    weapon.add_attribute('w_max_range', 'Number')
    weapon.add_attribute('effective_range_precision', 'Number')
    weapon.add_attribute('max_range_precision', 'Number')
    weapon.add_attribute('damage', 'Number')
    weapon.add_attribute('fire_rate', 'Number')
    weapon.add_attribute('ammunition_capacity', 'Number')
    weapon.add_attribute('current_ammo', 'Number')

    weapon.define_function('set_name', 'Void', ['a'], ['String'])
    weapon.define_function('set_weight', 'Void', ['a'], ['Number'])
    weapon.define_function('set_w_effective_range', 'Void', ['a'], ['Number'])
    weapon.define_function('set_w_max_range', 'Void', ['a'], ['Number'])
    weapon.define_function('set_effective_range_precision', 'Void', ['a'], ['Number'])
    weapon.define_function('set_damage', 'Void', ['a'], ['Number'])
    weapon.define_function('set_fire_rate', 'Void', ['a'], ['Number'])
    weapon.define_function('set_current_ammo', 'Void', ['a'], ['Number'])

    # WEATHER
    weather.add_attribute('state', 'String')
    weather.add_attribute('wind_speed', 'Number')
    weather.add_attribute('visibility_impairment', 'Number')
    weather.add_attribute('temperature', 'Number')
    weather.add_attribute('humidity', 'Number')

    # MAP

    # TERRAIN
    terrain.add_attribute('floor_type', 'String')
    terrain.add_attribute('height', 'Number')
    terrain.add_attribute('m_restriction', 'Number')
    terrain.add_attribute('camouflage', 'Number')
    terrain.add_attribute('available', 'Bool')
    terrain.add_attribute('terrain_object', 'Bool')

    # HEURISTIC

    # BUILDERS
    context.add_func(FuncDef('Soldier', 'Soldier',
                             ['health', 'vision_range', 'precision', 'move_speed', 'crit_chance', 'orientation',
                              'stance', 'max_load', 'concealment', 'melee_damage', 'team'],
                             ['Number', 'Number', 'Number', 'Number', 'Number', 'String', 'String', 'Number', 'Number',
                              'Number', 'Number'], None))
    context.add_func(FuncDef('Terrain', 'Terrain',
                             ['floor_type', 'height', 'm_restriction', 'camouflage', 'available', 'terrain_object'],
                             ['String', 'Number', 'Number', 'Number', 'Bool', 'Bool'], None))
    context.add_func(FuncDef('Weather', 'Weather',
                             ['state', 'wind_speed', 'visibility_impairment', 'temperature', 'humidity'],
                             ['String', 'Number', 'Number', 'Number', 'Number'], None))
    context.add_func(FuncDef('Map', 'Map',
                             ['row', 'col'],
                             ['Number', 'Number'], None))
    context.add_func(FuncDef('Weapon', 'Weapon',
                             ['name', 'weight', 'w_effective_range', 'w_max_range', 'effective_range_precision',
                              'max_range_precision',
                              'damage', 'fire_rate', 'ammunition_capacity', 'current_ammo'],
                             ['String', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number',
                              'Number'], None))

    # AUXILIARY FUNCTIONS
    context.add_func(FuncDef('len', 'Number', ['list'], ['List'], None))
    context.add_func(FuncDef('str', 'String', ['number'], ['Number'], None))
    context.add_func(FuncDef('int', 'Number', ['number'], ['Number'], None))
    context.add_func(FuncDef('print', 'Void', ['text'], ['String'], None))
    context.add_func(FuncDef('run', 'Void', ['map', 'weather', 'soldiers', 'ia_max_depth'],
                             ['Map', 'Weather', 'List Soldier', 'Number'], None))
    #   DETECTION FUNCTIONS
    context.add_func(
        FuncDef('detect_enemies_within_eff_range', 'List Soldier', ['soldier', 'map'], ['Soldier', 'Map'], None))
    context.add_func(
        FuncDef('detect_enemies_within_max_range', 'List Soldier', ['soldier', 'map'], ['Soldier', 'Map'], None))
    context.add_func(FuncDef('detect_allies', 'List Soldier', ['soldier', 'map'], ['Soldier', 'Map'], None))

    context.add_func(
        FuncDef('shoot', 'Void', ['soldierA', 'soldierB'], ['Soldier', 'Soldier'], None))
    context.add_func(
        FuncDef('move', 'Void', ['soldier', 'position'], ['Soldier', 'List Number'], None))


    return context

if __name__ == '__main__':
    execute(build_initial_context())
