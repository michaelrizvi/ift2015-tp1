# Prénom, Nom, Matricule
# Prénom, Nom, Matricule

import math
import random
import copy

class LinkedList:
    # TODO standardize empty list check! either size==0 or head is None 
    class _Node:
        def __init__(self, v, n=None):
            self.value = v
            self.next = n

    def __init__(self):
        self._head = None
        self._size = 0

    def __str__(self):
        if self._size == 0:
            return '[]'
        result = '['
        current = self._head
        while current:
            result += str(current.value) + ', '
            current = current.next

        return result[:-2] + ']'

    def __len__(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    # Adds a node of value v to the beginning of the list
    def add(self, v):
        if self._head is None:
            self._head = self._Node(v)
        else:
            new_node = self._Node(v)
            temp = self._head
            self._head = new_node
            new_node.next = temp
        self._size += 1

    # Adds a node of value v to the end of the list
    def append(self,v):
        if self._size == 0:
            self._head = self._Node(v)
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = self._Node(v)
        self._size += 1

    # Removes and returns the first node of the list
    def pop(self):
        if self._size == 0:
            return None
        result = self._head.value
        self._head = self._head.next
        self._size -= 1
        return result

    # Returns the value of the first node of the list
    def peek(self):
        if self._size == 0:
            return None
        return self._head.value

    # Removes the first node of the list with value v and return v
    def remove(self, v):
        if self._head is None:
            return None 
        if self._head.value == v:
            return self.pop()
        current = self._head
        prev = self._head
        while current:
            if current.value == v:
                prev.next = current.next 
                current.next = None
                self._size -= 1
                return v
            prev = current
            current = current.next
    
        return None

class CircularLinkedList(LinkedList):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        if self._head is None:
            return '[]'
        result = '['
        current = self._head
        for i in range(self._size):
            result += str(current.value) + ', '
            current = current.next
        return result[:-2] + ']'

    def __iter__(self):
        return self
    # Moves head pointer to next node in list
    def next(self):
        if self._head is not None:
            self._head = self._head.next

    # Adds a node of value v to the end of the list
    def append(self, v):
        if self._size == 0:
            self._head = self._Node(v)
            self._head.next = self._head
        else:
            current = self._head
            for i in range(self._size - 1):
                current = current.next
            current.next = self._Node(v, self._head)
        self._size += 1

    # Reverses the next pointers of all nodes to previous node
    def reverse(self):
        if self._size == 0:
            return None
        prev = None
        current = self._head
        next_node = current.next  
        current.next = prev
        prev = current
        current = next_node
        for i in range(self._size - 1):
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self._head.next = prev

    # Removes head node and returns its value
    def pop(self):
        if self._size == 0:
            return None
        result = self._head.value
        current = self._head
        for i in range(self._size - 1):
            current = current.next
        current.next = current.next.next 
        self._head.next = None
        self._head = current.next
        self._size -= 1
        return result

class Card:
    def __init__(self, r, s):
        self._rank = r
        self._suit = s

    suits = {'s': '\U00002660', 'h': '\U00002661', 'd': '\U00002662', 'c': '\U00002663'}

    def __str__(self):
        return self._rank + self.suits[self._suit]

    def __eq__(self, other):
        if self._suit == other._suit:
            if self._rank == other._rank:
                return True
            elif self._rank in ['1', 'A'] and other._rank in ['1', 'A']:
                return True
        else:
            return False


        return self._rank == other._rank and self._suit == other._suit

class Hand:
    def __init__(self):
        self.cards = {'s': LinkedList(), 'h': LinkedList(), 'd': LinkedList(), 'c': LinkedList()}

    def __str__(self):
        result = ''
        for suit in self.cards.values():
            result += str(suit)
        return result

    def __getitem__(self, item):
        return self.cards[item]

    def __len__(self):
        result = 0
        for suit in list(self.cards):
            result += len(self.cards[suit])

        return result

    def add(self, card):
        self.cards[card._suit].add(card)

    def get_most_common_suit(self):
        return max(list(self.cards), key = lambda x: len(self[x]))

    # Returns a card included in the hand according to
    # the criteria contained in *args and None if the card
        # isn't in the hand. The tests show how *args must be used.
    def play(self, *args):
        if args is None:
            return None
        ranks = ['1', 'a', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'J', 'q', 'Q', 'k', 'K'] 
        suits = ['s', 'h', 'd', 'c']
        # unpack the *args
        suit = None
        rank = None
        for x in args:
            if x in suits:
                suit = x
            if x in ranks:
                rank = x
        if suit and not rank:
            return self.cards[suit].pop()
        elif suit and rank:
            return self.cards[suit].remove(Card(rank, suit))
        elif rank and not suit:
            for s in suits:
                card = self.cards[s].remove(Card(rank, s))
                if card:
                    return card
            return None

class Deck(LinkedList):
    def __init__(self, custom=False):
        super().__init__()
        if not custom:
            # for all suits
            for i in range(4):
                # for all ranks
                for j in range(13):
                    s = list(Card.suits)[i]
                    r = ''
                    if j == 0:
                        r = 'A'
                    elif j > 0 and j < 10:
                        r = str(j+1)
                    elif j == 10:
                        r = 'J'
                    elif j== 11:
                        r = 'Q'
                    elif j == 12:
                        r = 'K'
                    self.add(Card(r,s))

    def draw(self):
        return self.pop()

    def shuffle(self, cut_precision = 0.05):
        # TODO: do we have to make 2 new Deck() instances??

        # Cutting the two decks in two
        center = len(self) / 2
        k = round(random.gauss(center, cut_precision*len(self)))
        # other_deck must point the kth node in self
        # (starting at 0 of course)
        current = self._head
        for i in range(k-1):
            current = current.next
        other = current.next
        other_deck = Deck(custom=True)
        other_deck._head = other
        other_deck._size = self._size - k
        print("other deck ", other_deck)
         
        current.next = None
        self._size = k
        print("deck ", self)
        #if random.uniform(0,1) < 0.5:
        #    pass
        current = self._head
        other = other_deck._head
        for i in range(k):
            current_next = current.next
            other_next = other.next
            current.next = other
            other.next = current_next 
            current = current_next
            other = other_next

class Player():
    def __init__(self, name, strategy='naive'):
        self.name = name
        self.score = 8
        self.hand = Hand()
        self.strategy = strategy

    def __str__(self):
        return self.name

    # This function must modify the player's hand,
    # the discard pile, and the game's declared_suit 
    # attribute. No other variables must be changed.
    # The player's strategy can ONLY be based
    # on his own cards, the discard pile, and
    # the number of cards his opponents hold.
    def play(self, game):
        if(self.strategy == 'naive'):
            top_card = game.discard_pile.peek()

            #TO DO

            return game

        else:
            # TO DO(?): Custom strategy (Bonus)
            pass

class Game:
    def __init__(self):
        self.players = CircularLinkedList()

        for i in range(1,5):
            self.players.append(Player('Player '+ str(i)))

        self.deck = Deck()
        self.discard_pile = LinkedList()

        self.draw_count = 0
        self.declared_suit = ''

    def __str__(self):
        result = '--------------------------------------------------\n'
        result += 'Deck: ' + str(self.deck) + '\n'
        result += 'Declared Suit: ' + str(self.declared_suit) + ', '
        result += 'Draw Count: ' + str(self.draw_count) + ', '
        result += 'Top Card: ' + str(self.discard_pile.peek()) + '\n'

        for player in self.players:
            result += str(player) + ': '
            result += 'Score: ' + str(player.score) + ', '
            result += str(player.hand) + '\n'
        return result


    # Puts all cards from discard pile except the 
    # top card back into the deck in reverse order
    # and shuffles it 7 times
    def reset_deck(self):
        #TO DO
        pass

    # Safe way of drawing a card from the deck
    # that resets it if it is empty after card is drawn
    def draw_from_deck(self, num):
        #TO DO
        pass
            

    def start(self, debug=False):
        # Ordre dans lequel les joeurs gagnent la partie
        result = LinkedList()

        self.reset_deck()

        # Each player draws 8 cards
        for player in self.players:
            for i in range(8):
                player.hand.add(self.deck.draw())

        self.discard_pile.add(self.deck.draw())

        transcript = open('result.txt','w',encoding='utf-8')
        if debug:
            transcript = open('result_debug.txt','w',encoding='utf-8')

        while(not self.players.isEmpty()):
            if debug:
                transcript.write(str(self))

            # player plays turn
            player = self.players.peek()

            old_top_card = self.discard_pile.peek()

            self = player.play(self)

            new_top_card = self.discard_pile.peek()

            # Player didn't play a card => must draw from pile
            if new_top_card == old_top_card:
               #TO DO
               pass
            # Player played a card
            else:
                #TO DO
                pass
            # Handling player change
            # Player has finished the game
            if len(player.hand) == 0 and player.score == 1:
                #TO DO
                pass
            else:
                # Player is out of cards to play
                if len(player.hand) == 0:
                    #TO DO
                    pass
                # Player has a single card left to play
                elif len(player.hand) == 1:
                    #TO DO
                    pass
                self.players.next()
        return result


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
    print("All tests passed!")

    # Circular linkedlist
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
    
    print("All tests passed!")

    '''
    random.seed(420)
    game = Game()
    print(game.start(debug=True))

    # TESTS
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

    # Card
    c1 = Card('A','s')
    c2 = Card('A','s')
    # Il est pertinent de traiter le rang 1
    # comme étant l'ace
    c3 = Card('1','s')
    assert(c1 == c2)
    assert(c1 == c3)
    assert(c3 == c2)

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
    assert(str(h) == '[A♠][8♡][Q♢][]')
    assert(h.play('d','Q') == Card('Q','d'))
    assert(h.play('1') == Card('A','s'))
    assert(h.play('J') == None)

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
