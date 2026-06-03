import json


class Card:
    def __init__(self, name):
        self.card_data = "Items\\Cards.json"
        self.name = name

        self.Description_Template = ""
        self.Description = ""

        self.Rarity = ""
        self.Effect = ""
        self.Effect_Value = 0
        self.Duration = 0
        self.Trigger_Type = ""
        self.Trigger_Value = 0
        self.card_level = 1

    def update_description(self):
        """
        Build the displayed description from the template.
        """
        self.Description = self.Description_Template

        self.Description = self.Description.replace(
            "{{Effect_Value}}",
            str(self.Effect_Value)
        )

        self.Description = self.Description.replace(
            "{{1-Effect_Value}}",
            f"{self.Effect_Value}%"
        )

    def load_card(self):
        with open(self.card_data, "r") as f:
            data = json.load(f)

        card_data = None

        for category, cards in data.items():
            if self.name in cards:
                card_data = cards[self.name]
                break

        if card_data is None:
            print(f"Card '{self.name}' not found.")
            return False

        self.Description_Template = card_data.get("Description", "")
        self.Rarity = card_data.get("Rarity", "")
        self.Effect = card_data.get("Effect", "")
        self.Effect_Value = card_data.get("Effect_Value", 0)
        self.Duration = card_data.get("Duration", 0)
        self.Trigger_Type = card_data.get("Trigger_Type", "")
        self.Trigger_Value = card_data.get("Trigger_Value", 0)

        self.update_description()
        return True

    def upgrade_card(self, levels=1):
        """
        Upgrade the card by the specified number of levels.
        """
        is_percentage_card = "{{1-Effect_Value}}" in self.Description_Template

        for _ in range(levels-1):
            if is_percentage_card:
                self.Effect_Value *= 2
            else:
                self.Effect_Value *= 1.5
            self.card_level += 1

        self.update_description()

    def print_card(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.Description}")
        print(f"Rarity: {self.Rarity}")
        print(f"Effect: {self.Effect}")
        print(f"Effect_Value: {self.Effect_Value}")
        print(f"Duration: {self.Duration}")
        print(f"Trigger_Type: {self.Trigger_Type}")
        print(f"Trigger_Value: {self.Trigger_Value}")

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


# Example usage
new_card = Card("Health Potion")

if new_card.load_card():
    print("Original:")
    new_card.print_card()

    print("\nUpgrading by 2 levels...\n")

    new_card.upgrade_card(2)
    new_card.print_card()