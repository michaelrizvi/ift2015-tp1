import math
import random
import copy

from crazy8 import LinkedList, CircularLinkedList, Card, Hand, Deck

if __name__ == '__main__':
    # LinkedList
    l = LinkedList()
    l.append('b')
    l.append('c')
    l.add('a')
    assert(str(l) == '[a, b, c]')
    assert(l.pop() == 'a')
    assert(len(l) == 2)
    assert(str(l.remove('c')) == 'c')
    assert(l.remove('d') == None)
    assert(str(l) == '[b]')
    assert(l.peek() == 'b')
    assert(l.pop() == 'b')
    assert(len(l) == 0)
    assert(l.isEmpty())
    print("LinkedList: All tests passed!")

    # CircularLinkedList
    l = CircularLinkedList()
    l.append('a')
    l.append('b')
    l.append('c')
    assert(str(l) == '[a, b, c]')
    l.next()
    assert(str(l) == '[b, c, a]')
    l.next()
    assert(str(l) == '[c, a, b]')
    l.next()
    assert(str(l) == '[a, b, c]')
    l.reverse()
    assert(str(l) == '[a, c, b]')
    assert(l.pop() == 'a')
    assert(str(l) == '[c, b]')
    print("CircularLinkedList: All tests passed!")

    # Card
    c1 = Card('A','s')
    c2 = Card('A','s')
    # Il est pertinent de traiter le rang 1
    # comme étant l'ace
    c3 = Card('1','s')
    assert(c1 == c2)
    assert(c1 == c3)
    assert(c3 == c2)
    print("Card: All tests passed!")

    # Hand
    h = Hand()
    h.add(Card('A','s'))
    h.add(Card('8','s'))
    h.add(Card('8','h'))
    h.add(Card('Q','d'))
    h.add(Card('3','d'))
    h.add(Card('3','c'))

    assert(str(h) == '[8♠, A♠][8♡][3♢, Q♢][3♣]')
    assert(str(h['d']) == '[3♢, Q♢]')
    assert(h.play('3','d') == Card('3','d'))
    assert(str(h) == '[8♠, A♠][8♡][Q♢][3♣]')
    assert(str(h.play('8')) == '8♠')
    assert(str(h.play('c')) == '3♣')
    print(h)
    assert(str(h) == '[A♠][8♡][Q♢][]')
    assert(h.play('d','Q') == Card('Q','d'))
    assert(h.play('1') == Card('A','s'))
    assert(h.play('J') == None)
    print("Hand: All tests passed!")

    # Deck
    d = Deck(custom=True)
    d.append(Card('A','s'))
    d.append(Card('2','s'))
    d.append(Card('3','s'))
    d.append(Card('A','h'))
    d.append(Card('2','h'))
    d.append(Card('3','h'))
    print(d)
    d.shuffle()
    print(d)
    '''
    random.seed(15)

    temp = copy.deepcopy(d)
    assert(str(temp) == '[A♠, 2♠, 3♠, A♡, 2♡, 3♡]')
    temp.shuffle()
    assert(str(temp) == '[A♠, A♡, 2♠, 2♡, 3♠, 3♡]')
    temp = copy.deepcopy(d)
    temp.shuffle()
    assert(str(temp) == '[A♡, A♠, 2♡, 2♠, 3♡, 3♠]')
    assert(d.draw() == Card('A','s'))
    print("Deck: All tests passed!")
    '''
    '''
    random.seed(420)
    game = Game()
    print(game.start(debug=True))

    # Deck
    d = Deck(custom=True)
    d.append(Card('A','s'))
    d.append(Card('2','s'))
    d.append(Card('3','s'))
    d.append(Card('A','h'))
    d.append(Card('2','h'))
    d.append(Card('3','h'))

    random.seed(15)

    temp = copy.deepcopy(d)
    assert(str(temp) == '[A♠, 2♠, 3♠, A♡, 2♡, 3♡]')
    temp.shuffle()
    assert(str(temp) == '[A♠, A♡, 2♠, 2♡, 3♠, 3♡]')
    temp = copy.deepcopy(d)
    temp.shuffle()
    assert(str(temp) == '[A♡, A♠, 2♡, 2♠, 3♡, 3♠]')
    assert(d.draw() == Card('A','s'))
    '''
