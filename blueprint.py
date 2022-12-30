apps = []
from leaderboard.app_leader import app
from apis.app_apis import app as apis
from login.app_login import app as alogin
from games.app_game import app as agame
from games.app_game2 import app as agame2
from games.app_game3 import app as agame3

apps.append(app)
apps.append(apis)
apps.append(alogin)
apps.append(agame)
apps.append(agame3)
apps.append(agame2)