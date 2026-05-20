import json

class Card:
    def __init__(self, name):
        self.card_data = "Items\\Cards.json"
        self.name = name
        self.Description = ""
        self.Rarity = ""
        self.Effect = ""
        self.Effect_Value = 0
        self.Duration = 0
        self.Trigger_Type = ""
        self.Trigger_Value = 0

    def load_card(self):
        with open(self.card_data, "r") as f:
            data = json.load(f)

        card_data = None

        # Search through all categories
        for category, cards in data.items():
            if self.name in cards:
                card_data = cards[self.name]
                break

        if not card_data:
            print(f"Card '{self.name}' not found.")
            return

        self.Description = card_data.get("Description", "")
        self.Rarity = card_data.get("Rarity", "")
        self.Effect = card_data.get("Effect", "")
        self.Effect_Value = card_data.get("Effect_Value", 0)
        self.Duration = card_data.get("Duration", 0)
        self.Trigger_Type = card_data.get("Trigger_Type", "")
        self.Trigger_Value = card_data.get("Trigger_Value", 0)

        # Replace placeholders in description
        self.Description = self.Description.replace(
            "{{Effect_Value}}",
            str(self.Effect_Value)
        )

    def print_card(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.Description}")
        print(f"Rarity: {self.Rarity}")
        print(f"Effect: {self.Effect}")
        print(f"Effect_Value: {self.Effect_Value}")
        print(f"Duration: {self.Duration}")
        print(f"Trigger_Type: {self.Trigger_Type}")
        print(f"Trigger_Value: {self.Trigger_Value}")

    def test_card(self):
        self.load_card()
        self.print_card()
    
    def card_stats(self):
        return {
            "Name": self.name,
            "Description": self.Description,
            "Rarity": self.Rarity,
            "Effect": self.Effect,
            "Effect_Value": self.Effect_Value,
            "Duration": self.Duration,
            "Trigger_Type": self.Trigger_Type,
            "Trigger_Value": self.Trigger_Value
        }

# new_card = Card("Critical Hit Damage")
# new_card.test_card()