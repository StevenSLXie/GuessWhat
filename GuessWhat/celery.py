from __future__ import absolute_import

from celery import Celery
from datetime import timedelta

app = Celery('GuessWhat',
			 broker='redis://',
			 backend='redis://',
			 include=['GuessWhat.task'],
			 )


# Optional configuration, see the application user guide.
app.conf.update(
	CELERY_TASK_RESULT_EXPIRES=3600,
	CELERYBEAT_SCHEDULE={'ranking-every-30-seconds': {
		'task': 'GuessWhat.task.ranking',
		'schedule': timedelta(seconds=30),
		'args': ()
	},}
)

if __name__ == '__main__':
	app.start()