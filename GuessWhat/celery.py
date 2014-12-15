from __future__ import absolute_import

from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

app = Celery('GuessWhat',
			 broker='redis://',
			 backend='redis://',
			 include=['GuessWhat.task'],
			 )


# Optional configuration, see the application user guide.
app.conf.update(
	CELERY_TASK_RESULT_EXPIRES=3600,
	CELERYBEAT_SCHEDULE={
		'ranking-every-30-seconds': {
		'task': 'GuessWhat.task.ranking',
		'schedule': timedelta(seconds=120),
		'args': ()
	},

		'inbox-ranking-notify': {
		'task': 'GuessWhat.task.send_profile_to_inbox',
		'schedule': crontab(minute=0, hour='*/12'),
		'args': ()
	},

		'cal-expertise': {
		'task': 'GuessWhat.task.cal_expertise',
		'schedule': crontab(minute='*/30'),
		'args': ()
	},

		'detect-ended-game':{
		'task': 'GuessWhat.task.detect_ended_game',
		'schedule': timedelta(seconds=60),
		'args':()
	},
		'game-management':{
		'task': 'GuessWhat.task.game_management',
		'schedule': crontab(minute='*/15'),
		'args':()
	}


						 }
)

if __name__ == '__main__':
	app.start()