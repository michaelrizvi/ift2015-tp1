# Michael, Rizvi-Martel, 20223775
# Jie, Bao, 20047494 

import math
import random
import copy


class LinkedList:
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
        result = "["
        current = self._head
        while current:
            result += str(current.value) + ", "
            current = current.next

        return result[:-2] + "]"

    def __len__(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    # Adds a node of value v to the beginning of the list
    def add(self, v):
        if self._size == 0:
            self._head = self._Node(v)
        else:
            new_node = self._Node(v)
            temp = self._head
            self._head = new_node
            new_node.next = temp
        self._size += 1

    # Adds a node of value v to the end of the list
    def append(self, v):
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
        if self._size == 0:
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
        if self._size == 0:
            return '[]'
        result = "["
        current = self._head
        for i in range(self._size):
            result += str(current.value) + ", "
            current = current.next
        return result[:-2] + "]"

    def __iter__(self):
        current = self._head
        for i in range(self._size):
            yield current.value
            current = current.next

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

    suits = {"s": "\U00002660", "h": "\U00002661", "d": "\U00002662", "c": "\U00002663"}

    def __str__(self):
        return self._rank + self.suits[self._suit]

    def __eq__(self, other):
        if self._suit == other._suit:
            if self._rank == other._rank:
                return True
            elif self._rank in ["1", "A"] and other._rank in ["1", "A"]:
                return True
        else:
            return False

        return self._rank == other._rank and self._suit == other._suit


class Hand:
    def __init__(self):
        self.cards = {
            "s": LinkedList(),
            "h": LinkedList(),
            "d": LinkedList(),
            "c": LinkedList(),
        }

    def __str__(self):
        result = ""
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
        return max(list(self.cards), key=lambda x: len(self[x]))

    # Returns a card included in the hand according to
    # the criteria contained in *args and None if the card
    # isn't in the hand. The tests show how *args must be used.
    def play(self, *args):
        if args is None:
            return None
        ranks = [
            "1",
            "a",
            "A",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "j",
            "J",
            "q",
            "Q",
            "k",
            "K",
        ]
        suits = ["s", "h", "d", "c"]
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
                    r = ""
                    if j == 0:
                        r = "A"
                    elif j > 0 and j < 10:
                        r = str(j + 1)
                    elif j == 10:
                        r = "J"
                    elif j == 11:
                        r = "Q"
                    elif j == 12:
                        r = "K"
                    self.add(Card(r, s))

    def draw(self):
        return self.pop()

    def shuffle(self, cut_precision=0.05):
        # Cutting the two decks in two
        center = len(self) / 2
        k = round(random.gauss(center, cut_precision * len(self)))
        deck_size = len(self)

        # Go to the k-1nth index
        current = self._head
        for i in range(k - 1):
            current = current.next

        # Create other deck
        other = current.next
        other_deck = Deck(custom=True)
        other_deck._head = other
        other_deck._size = self._size - k

        # Shrink deck
        current.next = None
        self._size = k

        # Shuffle
        current = self._head
        other = other_deck._head
        if random.uniform(0, 1) < 0.5:
            current = other_deck._head
            other = self._head
            self._head = other_deck._head

        for i in range(min(k, deck_size - k)):
            current_next = current.next
            other_next = other.next
            current.next = other
            if current_next:
                other.next = current_next
            current = current_next
            other = other_next

        self._size = deck_size


class Player:
    def __init__(self, name, strategy="naive"):
        self.name = name
        self.score = 8
        self.hand = Hand()
        self.strategy = strategy
        self.counted_cards = LinkedList() 

    def __str__(self):
        return self.name

    # This function must modify the player's hand,
    # the discard pile, and the game's declared_suit
    # attribute. No other variables must be changed.
    # The player's strategy can ONLY be based
    # on his own cards, the discard pile, and
    # the number of cards his opponents hold.
    def play(self, game):
        if self.strategy == "naive":
            top_card = game.discard_pile.peek()
            top_rank = top_card._rank
            is_wildcard = False
            if game.declared_suit != "":
                top_suit = game.declared_suit
                is_wildcard = True
            else:
                top_suit = top_card._suit
            card = None
            score = str(self.score) if self.score > 1 else "A"

            # if we have to pick up cards, try playing a 2 or a Q of Spades
            if game.draw_count > 0 and (
                top_rank == "2" or (top_rank == "Q" and top_card._suit == "s")
            ):
                if is_wildcard:
                    card = self.hand.play("Q", "s")
                    if card:
                        game.discard_pile.add(card)
                else:
                    card = self.hand.play("2")
                    if card:
                        game.discard_pile.add(card)
                        if score == "2":
                            game.declared_suit = self.hand.get_most_common_suit()
                    else:
                        card = self.hand.play("Q", "s")
                        if card:
                            game.discard_pile.add(card)
            # if we don't have to pickup cards 
            else:
                # if no card of same suit or only card of same suit is wildcard play
                # card of same rank
                nb_top_suit = len(self.hand[top_suit])
                cards_of_suit = self.hand[top_suit]
                if cards_of_suit.isEmpty() or (
                    nb_top_suit == 1 and cards_of_suit.peek()._rank == score
                ):
                    # if top_rank is wildcard then play rank = score
                    if is_wildcard or top_rank == score:
                        card = self.hand.play(score)
                        if card:
                            game.discard_pile.add(card)
                            game.declared_suit = self.hand.get_most_common_suit()
                    else:
                        card = self.hand.play(top_rank)
                        if card:
                            game.discard_pile.add(card)
                        # if no card of same rank play a wildcard
                        else:
                            card = self.hand.play(score)
                            if card:
                                game.discard_pile.add(card)
                                game.declared_suit = self.hand.get_most_common_suit()

                # if there are cards of same suit other than wildcard
                else:
    
                    if cards_of_suit.peek():
                        # if card is wildcard pick next
                        if cards_of_suit.peek()._rank == score:
                            current = cards_of_suit._head
                            current = current.next
                            next_rank = current.value._rank
                            card = self.hand.play(top_suit, next_rank)
                        else:
                            card = self.hand.play(top_suit)
                        game.discard_pile.add(card)

            # if played card not wildcard reinit declared_suit
            if card and card._rank != score:
                game.declared_suit = ""
            return game

        elif self.strategy == 'cardcounting':
            top_card = game.discard_pile.peek()
            # Initialize dict of frequences by rank
            freq_dict = dict()
            current = game.discard_pile._head
            while current.next:
                if current.value._rank not in freq_dict.keys():
                    freq_dict[current.value._rank] = 1
                else:
                    freq_dict[current.value._rank] += 1
                current = current.next
            top_rank = top_card._rank
            # if declared suit is not null and
            is_wildcard = False
            if game.declared_suit != "":
                top_suit = game.declared_suit
                is_wildcard = True
            else:
                top_suit = top_card._suit
            card = None
            score = str(self.score) if self.score > 1 else "A"

            # if we have to pick up cards, try playing a 2 or a Q of Spades
            if game.draw_count > 0 and (
                top_rank == "2" or (top_rank == "Q" and top_card._suit == "s")
            ):
                if is_wildcard:
                    card = self.hand.play("Q", "s")
                    if card:
                        game.discard_pile.add(card)
                else:
                    card = self.hand.play("2")
                    if card:
                        game.discard_pile.add(card)
                        if score == "2":
                            game.declared_suit = self.hand.get_most_common_suit()
                    else:
                        card = self.hand.play("Q", "s")
                        if card:
                            game.discard_pile.add(card)
            # else if we don't have to pickup cards 
            else:
                # if no card of same suit or only card of same suit is wildcard play
                # card of same rank
                nb_top_suit = len(self.hand[top_suit])
                cards_of_suit = self.hand[top_suit]
                if cards_of_suit.isEmpty() or (
                    nb_top_suit == 1 and cards_of_suit.peek()._rank == score
                ):
                    # if top_rank is wildcard then play rank = score
                    if is_wildcard or top_rank == score:
                        card = self.hand.play(score)
                        if card:
                            game.discard_pile.add(card)
                            game.declared_suit = self.hand.get_most_common_suit()
                    else:
                        card = self.hand.play(top_rank)
                        if card:
                            game.discard_pile.add(card)
                        # if no card of same rank play a wildcard
                        else:
                            card = self.hand.play(score)
                            if card:
                                game.discard_pile.add(card)
                                game.declared_suit = self.hand.get_most_common_suit()

                # if there are cards of same suit other than wildcard
                else:
                    if cards_of_suit.peek():
                        freq_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
                        for key, value in freq_dict.items():
                            card = self.hand.play(key)
                            if card:
                                game.discard_pile.add(card)
                                if card._rank == score:
                                    game.declared_suit = self.hand.get_most_common_suit()
                                break
                        if card is None:
                            if cards_of_suit.peek()._rank == score:
                                current = cards_of_suit._head
                                current = current.next
                                next_rank = current.value._rank
                                card = self.hand.play(top_suit, next_rank)
                            else:
                                card = self.hand.play(top_suit)
                            game.discard_pile.add(card)

            if card and card._rank != score:
                game.declared_suit = ""
            return game


class Game:
    def __init__(self):
        self.players = CircularLinkedList()

        for i in range(1, 5):
            self.players.append(Player("Player " + str(i)))

        self.deck = Deck()
        self.discard_pile = LinkedList()

        self.draw_count = 0
        self.declared_suit = ""

    def __str__(self):
        result = "--------------------------------------------------\n"
        result += "Deck: " + str(self.deck) + "\n"
        result += "Declared Suit: " + str(self.declared_suit) + ", "
        result += "Draw Count: " + str(self.draw_count) + ", "
        result += "Top Card: " + str(self.discard_pile.peek()) + "\n"
        for player in self.players:
            result += str(player) + ": "
            result += "Score: " + str(player.score) + ", "
            result += str(player.hand) + "\n"
        return result

    # Puts all cards from discard pile except the
    # top card back into the deck in reverse order
    # and shuffles it 7 times
    def reset_deck(self):
        top_card = self.discard_pile.pop()
        discard_size = len(self.discard_pile)
        for i in range(discard_size):
            self.deck.append(self.discard_pile.pop())
        for i in range(7):
            self.deck.shuffle()
        if top_card:
            self.discard_pile.add(top_card)

    # Safe way of drawing a card from the deck
    # that resets it if it is empty after card is drawn
    def draw_from_deck(self, num):
        draw_list = LinkedList()
        if self.deck.isEmpty():
            self.reset_deck()
        for n in range(num):
            draw_list.append(self.deck.draw())
            if self.deck.isEmpty():
                self.reset_deck()
        return draw_list

    def start(self, debug=False):
        # Ordre dans lequel les joeurs gagnent la partie
        result = LinkedList()

        self.reset_deck()
        # Each player draws 8 cards
        for player in self.players:
            for i in range(8):
                player.hand.add(self.deck.draw())

        self.discard_pile.add(self.deck.draw())

        transcript = open("result.txt", "w", encoding="utf-8")
        if debug:
            transcript = open("result_debug.txt", "w", encoding="utf-8")

        position = 0
        while not self.players.isEmpty():
            if debug:
                print(str(self))
                transcript.write(str(self))

            # player plays turn
            player = self.players.peek()

            old_top_card = self.discard_pile.peek()

            self = player.play(self)

            new_top_card = self.discard_pile.peek()

            # Player didn't play a card => must draw from pile
            if new_top_card == old_top_card:
                # If top card is 2 and draw_count is not 0
                if (
                    new_top_card._rank == "2" or new_top_card._rank == "Q"
                ) and self.draw_count > 0:
                    print(f"{player.name} draws {self.draw_count} cards")
                    transcript.write(f"{player.name} draws {self.draw_count} cards \n")
                    card_list = self.draw_from_deck(self.draw_count)
                    for i in range(self.draw_count):
                        player.hand.add(card_list.pop())
                    self.draw_count = 0
                else:
                    print(f"{player.name} draws 1 card")
                    transcript.write(f"{player.name} draws 1 card \n")
                    card_list = self.draw_from_deck(1)
                    player.hand.add(card_list.pop())
            # Player played a card
            else:
                print(f"{player.name} played {new_top_card}")
                transcript.write(f"{player.name} played {new_top_card} \n")
                # if played a 2 or a Queen, update draw_count
                if new_top_card._rank == "2":
                    self.draw_count += 2
                elif new_top_card._rank == "Q" and new_top_card._suit == "s":
                    self.draw_count += 5
                # if ace, change the order
                elif new_top_card._rank == "A":
                    self.players.reverse()
                # if J skip player
                elif new_top_card._rank == "J":
                    self.players.next()

            # Handling player change
            # Player has finished the game
            if len(player.hand) == 0 and player.score == 1:  # TO DO
                # increment player position
                position += 1
                print(f"{player.name} finishes in position {position}")
                transcript.write(f"{player.name} finishes in position {position} \n")
                self.players.remove(player)
            else:
                # Player is out of cards to play
                if len(player.hand) == 0:
                    player.score -= 1
                    print(
                        f"{player.name} is out of cards to play! {player.name} draws {player.score} cards"
                    )
                    transcript.write(
                        f"{player.name} is out of cards to play! {player.name} draws {player.score} cards \n"
                    )
                    cards = self.draw_from_deck(player.score)
                    for i in range(player.score):
                        player.hand.add(cards.pop())

                # Player has a single card left to play
                elif len(player.hand) == 1:
                    print(f"*Knock, knock* - {player.name} has a single card left!")
                    transcript.write(
                        f"*Knock, knock* - {player.name} has a single card left! \n"
                    )

                self.players.next()

            if len(self.players) == 1:
                player = self.players.pop()
                print(f"{player.name} finishes last")
                transcript.write(f"{player.name} finishes last \n")
        return result


if __name__ == "__main__":
    random.seed(420)
    game = Game()
    print(game.start(debug=True))

    # TESTS
    # LinkedList
    l = LinkedList()
    l.append("b")
    l.append("c")
    l.add("a")

    assert str(l) == "[a, b, c]"
    assert l.pop() == "a"
    assert len(l) == 2
    assert str(l.remove("c")) == "c"
    assert l.remove("d") == None
    assert str(l) == "[b]"
    assert l.peek() == "b"
    assert l.pop() == "b"
    assert len(l) == 0
    assert l.isEmpty()

    # CircularLinkedList
    l = CircularLinkedList()
    l.append("a")
    l.append("b")
    l.append("c")

    assert str(l) == "[a, b, c]"
    l.next()
    assert str(l) == "[b, c, a]"
    l.next()
    assert str(l) == "[c, a, b]"
    l.next()
    assert str(l) == "[a, b, c]"
    l.reverse()
    assert str(l) == "[a, c, b]"
    assert l.pop() == "a"
    assert str(l) == "[c, b]"

    # Card
    c1 = Card("A", "s")
    c2 = Card("A", "s")
    # Il est pertinent de traiter le rang 1
    # comme ??tant l'ace
    c3 = Card("1", "s")
    assert c1 == c2
    assert c1 == c3
    assert c3 == c2

    # Hand
    h = Hand()
    h.add(Card("A", "s"))
    h.add(Card("8", "s"))
    h.add(Card("8", "h"))
    h.add(Card("Q", "d"))
    h.add(Card("3", "d"))
    h.add(Card("3", "c"))

    assert str(h) == "[8???, A???][8???][3???, Q???][3???]"
    assert str(h["d"]) == "[3???, Q???]"
    assert h.play("3", "d") == Card("3", "d")
    assert str(h) == "[8???, A???][8???][Q???][3???]"
    assert str(h.play("8")) == "8???"
    assert str(h.play("c")) == "3???"
    assert str(h) == "[A???][8???][Q???][]"
    assert h.play("d", "Q") == Card("Q", "d")
    assert h.play("1") == Card("A", "s")
    assert h.play("J") == None

    # Deck
    d = Deck(custom=True)
    d.append(Card("A", "s"))
    d.append(Card("2", "s"))
    d.append(Card("3", "s"))
    d.append(Card("A", "h"))
    d.append(Card("2", "h"))
    d.append(Card("3", "h"))

    random.seed(15)

    temp = copy.deepcopy(d)
    assert str(temp) == "[A???, 2???, 3???, A???, 2???, 3???]"
    temp.shuffle()
    assert str(temp) == "[A???, A???, 2???, 2???, 3???, 3???]"
    temp = copy.deepcopy(d)
    temp.shuffle()
    assert str(temp) == "[A???, A???, 2???, 2???, 3???, 3???]"
    assert d.draw() == Card("A", "s")
