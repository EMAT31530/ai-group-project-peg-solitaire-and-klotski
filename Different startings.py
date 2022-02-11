#coding=utf-8

# positioning

#                    S S
K = 7       # 2x2 block king
H = 2       # 2x1 block
V = 3       # 1x2 block
P = 4       # 1x1 block
B = 0       # Blank
S = 1       # positions taken by extra block

# common starting positions
chrs = [
    {
        'name':u'1. ',
        'data':
           [[P, K, S, P],
            [V, S, S, V],
            [S, H, S, S],
            [H, S, H, S],
            [B, P, P, B]]
    },
    {
        'name':u'2. ',
        'data':
           [[B, H, S, B],
            [P, H, S, P],
            [V, K, S, V],
            [S, S, S, S],
            [P, H, S, P]]
    },
    {
        'name':u'3. ',
        'data':
           [[K, S, B, B],
            [S, S, H, S],
            [P, P, V, V],
            [H, S, S, S],
            [H, S, H, S]]
    },
    {
        'name':u'4. ',
        'data':
           [[V, K, S, V],
            [S, S, S, S],
            [V, H, S, V],
            [S, P, P, S],
            [P, B, B, P]]
    },
    {
        'name':u'5. ',
        'data':
           [[K, S, P, P],
            [S, S, H, S],
            [H, S, H, S],
            [P, H, S, B],
            [H, S, P, B]]
    },
    {
        'name':u'6. ',
        'data':
           [[V, V, V, V],
            [S, S, S, S],
            [B, K, S, B],
            [P, S, S, P],
            [H, S, P, P]]
    },
    {
        'name':u'7. ',
        'data':
           [[V, V, K, S],
            [S, S, S, S],
            [P, B, P, B],
            [V, H, S, V],
            [S, P, P, S]]
    },
    {
        'name':u'8. ',
        'data':
           [[K, S, P, B],
            [S, S, P, P],
            [V, P, H, S],
            [S, V, H, S],
            [B, S, H, S]]
    },
    {
        'name':u'9. ',
        'data':
           [[B, P, H, S],
            [K, S, B, V],
            [S, S, V, S],
            [P, P, S, V],
            [P, H, S, S]]
    },
    {
        'name':u'10. 阴96',
        'data':
           [[P, H, S, V],
            [P, P, V, S],
            [K, S, S, V],
            [S, S, B, S],
            [B, P, H, S]]
    },
    {
        'name':u'11. 峰回路转',
        'data':
           [[P, P, P, V],
            [K, S, V, S],
            [S, S, S, V],
            [P, H, S, S],
            [B, B, H, S]]
    },
    {
        'name':u'12. 换离为兑',
        'data':
           [[H, S, P, P],
            [H, S, K, S],
            [P, P, S, S],
            [H, S, V, V],
            [B, B, S, S]]
    },
    {
        'name':u'13. 寓巧于拙',
        'data':
           [[K, S, P, P],
            [S, S, H, S],
            [B, H, S, P],
            [V, H, S, V],
            [S, B, P, S]]
    },
    {
        'name':u'14. 小兵探路',
        'data':
           [[K, S, P, V],
            [S, S, B, S],
            [B, V, H, S],
            [P, S, H, S],
            [P, P, H, S]]
    },
    {
        'name':u'15. 近在咫尺',
        'data':
           [[V, V, P, P],
            [S, S, V, P],
            [H, S, S, P],
            [H, S, K, S],
            [B, B, S, S]]
    },
    {
        'name':u'16. 生机盎然',
        'data':
           [[K, S, B, V],
            [S, S, P, S],
            [B, P, V, P],
            [H, S, S, V],
            [H, S, P, S]]
    },
    {
        'name':u'17. 层层设防',
        'data':
           [[V, K, S, V],
            [S, S, S, S],
            [P, H, S, P],
            [P, H, S, P],
            [B, H, S, B]]
    },
    {
        'name':u'18. 入地无门',
        'data':
           [[V, K, S, P],
            [S, S, S, P],
            [P, H, S, P],
            [H, S, H, S],
            [B, H, S, B]]
    },
    {
        'name':u'19. 守口如瓶',
        'data':
           [[V, K, S, V],
            [S, S, S, S],
            [P, V, B, P],
            [P, S, B, P],
            [H, S, H, S]]
    },
    {
        'name':u'20. 四兵同心',
        'data':
           [[P, P, V, B],
            [P, P, S, V],
            [K, S, V, S],
            [S, S, S, B],
            [H, S, H, S]]
    },
    {
        'name':u'21. 暗度陈仓',
        'data':
           [[P, P, P, V],
            [V, K, S, S],
            [S, S, S, P],
            [H, S, H, S],
            [B, H, S, B]]
    },
    {
        'name':u'22. 异地同心',
        'data':
           [[H, S, P, P],
            [P, V, K, S],
            [B, S, S, S],
            [H, S, P, B],
            [H, S, H, S]]
    },
    {
        'name':u'23. 水泄不通',
        'data':
           [[V, K, S, P],
            [S, S, S, P],
            [H, S, H, S],
            [H, S, H, S],
            [P, B, B, P]]
    },
    {
        'name':u'24. 齐头并进',
        'data':
           [[V, K, S, V],
            [S, S, S, S],
            [P, P, P, P],
            [V, H, S, V],
            [S, B, B, S]]
    },
    {
        'name':u'25. 左兵右将',
        'data':
           [[K, S, V, V],
            [S, S, S, S],
            [P, P, H, S],
            [P, P, V, V],
            [B, B, S, S]]
    },
    {
        'name':u'26. 井底之蛙',
        'data':
           [[P, H, S, P],
            [V, K, S, V],
            [S, S, S, S],
            [P, H, S, P],
            [B, H, S, B]]
    },
    {
        'name':u'27. 匹马嘶风',
        'data':
           [[K, S, P, P],
            [S, S, P, P],
            [H, S, B, B],
            [V, V, V, V],
            [S, S, S, S]]
    },
    {
        'name':u'28. 牛气冲天',
        'data':
           [[P, B, B, P],
            [H, S, H, S],
            [V, K, S, V],
            [S, S, S, S],
            [P, H, S, P]]
    },
    {
        'name':u'29. 新手入门',
        'data':
           [[P, K, S, P],
            [P, S, S, P],
            [P, H, S, P],
            [P, P, P, P],
            [B, P, P, B]]
    },
]

