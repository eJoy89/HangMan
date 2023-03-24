import math
import pygame
import random

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션
size = [500, 900]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("HANGMAN")

# 3. 게임 내 필요한 설정
title_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Apple Chancery.ttf', 75)
start_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Times New Roman.ttf', 25)
hint_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Apple Chancery.ttf', 80)
entry_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Apple Chancery.ttf', 60)
no_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Apple Chancery.ttf', 40)
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
exiting = False
drop = False
entre_go = False
entry_text = ''
ready = False


# 정수로 변환 시켜 주는 함수
def tup_r(tup):
    temp_list = []
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)


# A가 영어 단어를 1개 생각 한다
f = open("voca.txt", "r")
raw_data = f.read()
f.close()
data_list = raw_data.split("\n")
data_list = data_list[:-1]
while True:
    r_index = random.randrange(0, len(data_list))
    word = data_list[r_index].replace(u"\xa0", u" ").split(" ")[1]
    if len(word) <= 6: break
word = word.upper()

# 단어의 글자 수만큼 밑줄을 듯는다
word_show = "_" * len(word)
# 폰트에 따라 사용 여부 결정
# word_show = ' '.join(word_show)

try_num = 0
ok_list = []
no_list = []

k = 0

# 시작 화면
while not exiting:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True
        if event.type == pygame.KEYDOWN:
            ready = True
    if ready:
        break

    screen.fill(black)

    title = title_font.render("HANGMAN", True, white)
    title_size = title.get_size()
    title_pos = tup_r((size[0] / 2 - title_size[0] / 2, size[1] / 2 - title_size[1] / 2))

    screen.blit(title, title_pos)

    start = start_font.render("press any key to start the game", True, white)
    start_size = start.get_size()
    start_pos = tup_r((size[0] / 2 - start_size[0] / 2, size[1] / 1.2))

    if pygame.time.get_ticks() % 1000 > 500:
        screen.blit(start, start_pos)

    pygame.display.flip()

# 4. 메인 이벤트
while not exiting:
    # 4-1. FPS 설정
    clock.tick(60)
    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)

            # filter
            if key_name == 'return' or key_name == 'enter':
                if entry_text != '' and (ok_list + no_list).count(entry_text) == 0:
                    entre_go = True
            elif len(key_name) == 1:
                if (65 <= ord(key_name) <= 90) or (97 <= ord(key_name) <= 122):
                    entry_text = key_name.upper()
                else:
                    entry_text = ''
            else:
                entry_text = ''

    # 4-3. 입력, 시간에 따른 변화
    if try_num == 8:
        k += 1
    if entre_go:
        ans = entry_text
        result = word.find(ans)

        if result == -1:
            try_num += 1
            no_list.append(ans)
        else:
            ok_list.append(ans)
            for i in range(len(word)):
                if word[i] == ans:
                    word_show = word_show[:i] + ans + word_show[i + 1:]

        # entre_go 초기화
        entre_go = False
        entry_text = ''

    # 4-4. 그리기
    screen.fill(white)
    A = tup_r((0, size[1] * 2 / 3))
    B = (size[0], A[1])
    C = tup_r((size[0] / 7, A[1]))
    D = (C[0], C[0])
    E = tup_r((size[0] / 2, D[1]))

    pygame.draw.line(screen, black, A, B, 3)
    pygame.draw.line(screen, black, C, D, 3)
    pygame.draw.line(screen, black, D, E, 3)

    F = tup_r((E[0], E[1] + size[0] / 6))

    # if drop == False:
    if not drop:
        pygame.draw.line(screen, black, E, F, 3)

    r_head = round(size[0] / 12)
    # if drop == True:
    if drop:
        G = (F[0], F[1] + r_head + k * 10)
    else:
        G = (F[0], F[1] + r_head)

    # 머리
    if try_num >= 1:
        pygame.draw.circle(screen, black, G, r_head, 3)

    H = (G[0], G[1] + r_head)
    I = (H[0], H[1] + r_head)

    # 목
    if try_num >= 2:
        pygame.draw.line(screen, black, H, I, 3)

    l_arm = r_head * 2
    J = (I[0] - l_arm * math.cos(30 * math.pi / 180),
         I[1] + l_arm * math.sin(30 * math.pi / 180))
    J = tup_r(J)
    K = (I[0] + l_arm * math.cos(30 * math.pi / 180),
         I[1] + l_arm * math.sin(30 * math.pi / 180))
    K = tup_r(K)

    # 팔
    if try_num >= 3:
        pygame.draw.line(screen, black, I, J, 3)
    if try_num >= 4:
        pygame.draw.line(screen, black, I, K, 3)

    L = (I[0], I[1] + l_arm)

    # 몸통
    if try_num >= 5:
        pygame.draw.line(screen, black, I, L, 3)

    l_leg = round(r_head * 2.5)
    M = (L[0] - l_leg * math.cos(60 * math.pi / 180),
         L[1] + l_leg * math.sin(60 * math.pi / 180))
    M = tup_r(M)
    N = (L[0] + l_leg * math.cos(60 * math.pi / 180),
         L[1] + l_leg * math.sin(60 * math.pi / 180))
    N = tup_r(N)

    # 다리
    if try_num >= 6:
        pygame.draw.line(screen, black, L, M, 3)
    if try_num >= 7:
        pygame.draw.line(screen, black, L, N, 3)

    # if drop == False:
    if not drop and try_num == 8:
        O = tup_r((size[0] / 2 - size[0] / 6, E[1] / 2 + F[1] / 2))
        P = (O[0] + k * 2, O[1])

        if P[0] > size[0] / 2 + size[0] / 6:
            P = tup_r((size[0] / 2 + size[0] / 6, O[1]))
            drop = True
            k = 0
        pygame.draw.line(screen, red, O, P, 3)

    # hint
    hint = hint_font.render(word_show, True, black)
    hint_size = hint.get_size()
    hint_pos = tup_r((size[0] / 2 - hint_size[0] / 2, size[1] * 5 / 6 - hint_size[1] / 2))
    screen.blit(hint, hint_pos)

    # 입력창 표시 하기
    entry = entry_font.render(entry_text, True, white)
    entry_size = entry.get_size()

    entry_pos = tup_r((size[0] / 2 - entry_size[0] / 2, size[1] * 17 / 18 - entry_size[1] / 2))

    entry_bg_size = 80
    pygame.draw.rect(screen, black, tup_r(
        (size[0] / 2 - entry_bg_size / 2, size[1] * 17 / 18 - entry_bg_size / 2, entry_bg_size, entry_bg_size)))

    screen.blit(entry, entry_pos)

    # incorrect alphabet add
    no_text = " ".join(no_list)
    no = no_font.render(no_text, True, red)
    no_pos = tup_r((20, size[1] * 2 / 3 + 20))
    screen.blit(no, no_pos)

    # 4-5. update
    pygame.display.flip()

# 5.게임 종료
pygame.quit()
