import pyxel
from Constantes import TUILES

class Joueur():
    def __init__(self, spawnpoint, game):
        self.game = game
        self.spawnpoint = spawnpoint
        self.x, self.y = spawnpoint
        self.hauteur = 8
        self.largeur = 8
        self.image = 0
        self.saute = False
        self.flip = False
        self.gravité = 0.4
        self.force_saut = 5
        self.rotate = 0
        self.vitesse_y = 0
        self.vitesse_x = 1
        self.dir = 1
        self.mort = False
        self.tilemap = pyxel.tilemaps[0]
        self.sur_pad = [0,(0,0)]

    def collision_y(self, x, y):
        points_impact_bas = [self.tilemap.pget(i, (y + self.hauteur)//8) for i in range(int(x//8), int((x + self.largeur)//8+1))]
        points_impact_haut = [self.tilemap.pget(i, y//8) for i in range(int(x//8), int((x + self.largeur)//8+1))]

        if any(map(lambda x: x == (10,0), points_impact_bas + points_impact_haut)):
            self.mort = True
        return any(map(lambda x: x[1] >= 25, points_impact_bas + points_impact_haut))
    
    def collision_tile(self):
        for i in range(int(self.x//8), int((self.x + self.largeur)//8 + 1)):
            for j in range(int(self.y//8), int((self.y + self.hauteur)//8 + 1)):
                tuile = self.tilemap.pget(i,j)
                if tuile in TUILES['pieces']:
                    self.game.nb_piece += 1
                    self.game.pieces.remove((i,j))
                    pyxel.tilemaps[0].pset(i,j,TUILES['vide'])
                if tuile == TUILES['pad']:
                    if not self.sur_pad[0]:
                        self.jump(self.force_saut*2)
                        self.sur_pad = [2, (i,j)]
                if tuile == TUILES['drapeau']:
                    # self.game.check_point(1, (i,j))
                    pass

    def jump(self, force_saut):
        if not self.saute:
            self.saute = True
            self.vitesse_y = -force_saut
            self.y += self.vitesse_y

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.vitesse_x
            self.dir = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.vitesse_x
            self.dir = 1
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT):
            if pyxel.frame_count % 2 == 0:
                self.image = (self.image+1) % 10
        if pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.KEY_RIGHT):
            self.image = 0

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_SPACE):
            self.jump(self.force_saut)

        if pyxel.btn(pyxel.KEY_DOWN):
            if self.saute:
                self.saute = False
                self.vitesse_y = -2
                self.flip = True
                self.rotate = 0

        if self.saute:
            self.vitesse_y += self.gravité
            self.vitesse_y = -7 if self.vitesse_y < -7 else self.vitesse_y
            self.vitesse_y = 7 if self.vitesse_y > 7 else self.vitesse_y
            self.y += self.vitesse_y

            if self.collision_y(self.x, self.y):
                self.y = self.y - self.y % 8
                self.vitesse_y = 0
                self.saute = False
        else:
            # gravité
            self.vitesse_y += self.gravité
            self.vitesse_y = -7 if self.vitesse_y < -7 else self.vitesse_y
            self.vitesse_y = 7 if self.vitesse_y > 7 else self.vitesse_y
            self.y += self.vitesse_y

            if self.collision_y(self.x, self.y):
                self.y = self.y - self.y % 8
                self.vitesse_y = 0

        if self.flip:
            self.rotate += 360/15
            if self.rotate == 360:
                self.flip = False

        if self.sur_pad[0]:
            if pyxel.frame_count % 2 == 0:
                x, y = self.sur_pad[1]
                self.sur_pad[0] -= 1
                self.tilemap.pset(x, y, (4 + (2-self.sur_pad[0]), 22))

        self.collision_tile()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.image * self.largeur, 16, self.largeur * self.dir, self.hauteur, 5, rotate=self.rotate)