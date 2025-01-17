from django.db.utils import IntegrityError
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from battle.businesslogic.tests.Creator import Creator
from cards.models import Card, CardInfo, CardLevel
from . import views
from django.contrib.auth import get_user_model

from .models import UserProfile, Semester, UserCard, Deck, UserDeck
from .serializers import UserDecksSerializer


class UserProfileTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_user = get_user_model().objects.create_user(username='testusername', password='12345')

    def setUp(self) -> None:
        self.test_username = "testuser"
        self.semester = 5
        self.user_profile = UserProfile.objects.create(user=self.test_user,
                                                       displayedUsername=self.test_username,
                                                       semester=Semester.objects.get(pk=5))

    def tearDown(self) -> None:
        self.user_profile.delete()

    def testApiGet(self):
        factory = APIRequestFactory()
        view = views.UserProfileViewSet.as_view({"get": "list"})
        testRequest = factory.get('/api/igusers/basic')
        response = view(testRequest)

        # Assert user in returned users list.
        user_ids = [user_data["user"] for user_data in response.data]
        self.assertTrue(self.test_user.id in user_ids)

        # Assert user has correct data
        for user_data in response.data:
            if user_data["user"] == self.test_user.id:
                self.assertEqual(self.test_username, user_data['displayedUsername'])
                self.assertEqual(self.semester, user_data['semester'])

    def testApiPost(self):
        # Setup test view
        factory = APIRequestFactory()
        view = views.UserProfileViewSet.as_view({"get": "retrieve", "post": "create"})

        # Create data needed to create new UserProfile
        new_user = get_user_model().objects.create_user(username="asdasa", password="129312", email="tse@tst.sd")
        new_username = "test2"
        new_semester = 5

        # Make post request to create new UserProfile
        result = factory.post('/api/igusers/basic', data={'user': new_user.id,
                                                          'displayedUsername': new_username,
                                                          'semester': new_semester}, format='json')
        view(result)

        # Make GET request to check if newly created UserProfile exists.
        testRequest = factory.get('/api/igusers/basic/')
        response = view(testRequest, pk=new_user.id)

        # Assert that UserProfile returned by GET has correct data.
        self.assertEqual(new_user.id, response.data['user'])
        self.assertEqual(new_username, response.data['displayedUsername'])
        self.assertEqual(new_semester, response.data['semester'])

    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()


class UserCardTestCase(TestCase):
    def test_assigning(self):
        card = Card()
        user_profile = UserProfile()
        user_card = UserCard(user_profile=user_profile,
                             card=card)

        self.assertEqual(user_card.card, card)
        self.assertEqual(user_card.user_profile, user_profile)

    def test_unique_constraint(self):
        u1 = UserProfile(user=get_user_model().objects.create_user(username="test"),
                         displayedUsername="test")
        u1.save()

        info = CardInfo.objects.create()
        level = CardLevel.objects.get(pk=1)
        card1 = Card.objects.create(info=info,
                                    level=level)
        # Creating first user_card
        UserCard.objects.create(user_profile=u1, card=card1)
        # Second user_card with the same card and user should raise
        c2 = UserCard(user_profile=u1, card=card1)
        self.assertRaises(IntegrityError, c2.save)


class DeckTestCase(TestCase):
    def test_assigning(self):
        card1 = UserCard()
        card2 = UserCard()
        card3 = UserCard()
        card4 = UserCard()
        card5 = UserCard()

        deck = Deck(card1=card1,
                    card2=card2,
                    card3=card3,
                    card4=card4,
                    card5=card5)

        self.assertIs(deck.card1, card1)
        self.assertIs(deck.card2, card2)
        self.assertIs(deck.card3, card3)
        self.assertIs(deck.card4, card4)
        self.assertIs(deck.card5, card5)

    def test_unique_constraint(self):
        u1 = UserProfile(user=get_user_model().objects.create_user(username="test"),
                         displayedUsername="test")
        u1.save()

        info = CardInfo.objects.create()
        level = CardLevel.objects.get(pk=1)
        card1 = Card.objects.create(info=info,
                                    level=level)
        # Creating first user_card
        card = UserCard.objects.create(user_profile=u1, card=card1)

        deck = Deck.objects.create(card1=card,
                                   card2=card,
                                   card3=card,
                                   card4=card,
                                   card5=card)

        UserDeck.objects.create(deck_number=1,
                                deck=deck,
                                user_profile=u1)
        failing_deck = UserDeck(deck_number=1, deck=deck, user_profile=u1)
        self.assertRaises(IntegrityError, failing_deck.save)


class UserDeckSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.creator = Creator()

    def test_serialization(self):
        user = self.creator.get_user_profile_models()[0]
        serializer = UserDecksSerializer(user)
        data = serializer.data.get('user_decks')

        # We get a first deck from the created user
        actual_deck1 = user.user_decks.all()[0]
        self.assertEqual(data[0]['deck_number'], actual_deck1.deck_number)
        # We check selected two cards
        self.assertEqual(data[0]['card1']['id'], actual_deck1.deck.card1.card.info.id)
        self.assertEqual(data[0]['card1']['level'], actual_deck1.deck.card1.card.level.level)
        self.assertEqual(data[0]['card3']['id'], actual_deck1.deck.card3.card.info.id)
        self.assertEqual(data[0]['card3']['level'], actual_deck1.deck.card3.card.level.level)

    @classmethod
    def tearDownClass(cls):
        cls.creator.perform_deletion()
