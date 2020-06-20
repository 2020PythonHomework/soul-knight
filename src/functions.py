
import pygame

def hit_check(group1, group2):
    atk_list1 = []
    atk_list2 = []
    attacker = pygame.sprite.groupcollide(group1, group2, False, False)
    if attacker:
        for key in attacker.keys():
            for key2 in attacker[key]:
                if pygame.sprite.collide_circle_ratio(0.8)(key, key2):
                    atk_list1.append(key)
                    atk_list2.append(key2)
    return atk_list1, atk_list2
                    # key.currentHP -= bullet.damage
                    # bullet_g.remove(bullet)

def damage_check(character_group, bullet_group):
    character_list, bullet_list = hit_check(character_group, bullet_group)
    for i in range(len(character_list)):
        character_list[i].currentHP -= bullet_list[i].damage
        bullet_list[i].kill()

def block_check(character_group, wall_group, if_delete = False):
    character_list, wall_list = hit_check(character_group, wall_group)
    for i in range(len(character_list)):
        if character_list[i].X + 0.3 * character_list[i].frame_width < wall_list[i].X:
            if character_list[i].velocity[0] > 0:
                character_list[i].velocity[0] = 0
        if character_list[i].Y + 0.3 * character_list[i].frame_height < wall_list[i].Y and\
            character_list[i].velocity[1] > 0:
            character_list[i].velocity[1] = 0
        if wall_list[i].X + 0.3 * wall_list[i].frame_width < character_list[i].X and\
            character_list[i].velocity[0] < 0:
            character_list[i].velocity[0] = 0
        if wall_list[i].Y + 0.3 * wall_list[i].frame_height < character_list[i].Y and\
            character_list[i].velocity[1] < 0:
            character_list[i].velocity[1] = 0
        if if_delete:
            character_list[i].kill()