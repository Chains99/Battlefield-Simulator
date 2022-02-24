class Terrain:

    def __init__(self, floor_type, height=0, m_restriction=1, camouflage=1, available=True, terrain_object=None):
        self.height = height
        self.m_restriction = m_restriction
        # int 1 < camouflage < 2
        self.camouflage = camouflage
        self.available = available
        self.floor_type = floor_type
        self.terrain_object = terrain_object

    def add_object(self, terrain_object):
        self.terrain_object = terrain_object
        self.available = False
