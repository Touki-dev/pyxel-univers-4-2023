import pyxel, time
from Entitées.Joueur import *
from Constantes import TUILES

class Game:
    def __init__(self):
        pyxel.init(128, 128, "Nuit du code 2024 Univers 4", fps=30)
        pyxel.load("univers.pyxres")

        self.joueur = Joueur((64, 64), self)
        self.pos_camera = [0,0]
        self.tilemap = pyxel.tilemaps[0]
        self.taille_map = (128*4,128*4)
        self.pieces = self.trouver_pieces()
        self.image_pieces = 0
        self.nb_piece = 0
        self.check_point_pass = 0

        pyxel.run(self.update, self.draw)

    def trouver_pieces(self):
        pieces = []
        for i in range(self.taille_map[0]//8):
            for j in range(self.taille_map[1]//8):
                if self.tilemap.pget(i,j) == (4,20):
                    pieces.append((i,j))
        return pieces
    
    def update_pieces(self):
        if pyxel.frame_count % 6 == 0:
            for p in self.pieces:
                x,y = p
                self.tilemap.pset(x, y, (4 + self.image_pieces % 4, 20))
            self.image_pieces += 1

    def move_camera(self, jx, jy):
        if jx < pyxel.width/3 + self.pos_camera[0]:
            self.pos_camera[0] -= pyxel.width/3 + self.pos_camera[0] - jx
        elif pyxel.width/3 * 2 + self.pos_camera[0] < jx:
            self.pos_camera[0] += jx - (pyxel.width/3 * 2 + self.pos_camera[0])

        if jy < pyxel.height/3 + self.pos_camera[1]:
            self.pos_camera[1] -= pyxel.height/3 + self.pos_camera[1] - jy
        elif pyxel.height/3 * 2 + self.pos_camera[1] < jy:
            self.pos_camera[1] += jy - (pyxel.height/3 * 2 + self.pos_camera[1])
            
        pyxel.camera(self.pos_camera[0], self.pos_camera[1])


    def update(self):
        if not self.joueur.mort:
            self.joueur.update()
            self.move_camera(self.joueur.x, self.joueur.y)
            self.update_pieces()

    def compteur_piece(self):
        pyxel.blt(self.pos_camera[0] + 4, self.pos_camera[1] + 4, 0, 4*8, 20*8, 8, 8, 5)
        pyxel.text(self.pos_camera[0] + 16, self.pos_camera[1] + 5, str(self.nb_piece), 7)

    def draw(self):
        if not self.joueur.mort:
            pyxel.cls(5)
            pyxel.bltm(0, 0, 0, 0, 0, self.taille_map[0], self.taille_map[1], 5)
            self.joueur.draw()
        else:
            self.pos_camera = (0,0)
            pyxel.camera()
            pyxel.cls(0)
            pyxel.text(45,60,"Game Over",7)
        self.compteur_piece()

Game()