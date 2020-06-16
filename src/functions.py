
import pygame

def hit_check(character_g, bullet_g):
    attacker = pygame.sprite.groupcollide(character_g, bullet_g, False, False)
    if attacker:
        for key in attacker.keys():
            for bullet in attacker[key]:
                if pygame.sprite.collide_circle_ratio(0.7)(key, bullet):
                    key.currentHP -= bullet.damage
                    bullet_g.remove(bullet)
