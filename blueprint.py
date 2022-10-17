apps = []
from leaderboard.app_leader import app
from apis.app_apis import app as apis
from login.app_login import app as alogin
from games.app_game import app as agame

apps.append(app)
apps.append(apis)
apps.append(alogin)
apps.append(agame)