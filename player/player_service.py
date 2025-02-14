class PlayerService:
    players = []

    @classmethod
    def get_all_players(cls):
        """Retrieve all players"""
        return cls.players

    @classmethod
    def add_player(cls, data):
        """Add a new player"""
        new_player = {
            "id": len(cls.players) + 1,
            "name": data["name"],
            "score": data["score"]
        }
        cls.players.append(new_player)
        return new_player
