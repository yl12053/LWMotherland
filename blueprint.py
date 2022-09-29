apps = []
from leaderboard.app_leader import app
from apis.app_apis import app as apis
from login.app_login import app as alogin

apps.append(app)
apps.append(apis)
apps.append(alogin)