class PlayerService:
    players = []

    @classmethod
    def get_all_players(cls):
        return cls.players

    @classmethod
    def add_player(cls, data):
        player = {
            "id": len(cls.players) + 1,
            "name": data["name"],
            "age": data["age"],
            "team": data["team"]
        }
        cls.players.append(player)
        return player
