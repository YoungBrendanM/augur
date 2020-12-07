import logging, os, sys, time, requests, json
from datetime import datetime
from multiprocessing import Process, Queue
import pandas as pd
import sqlalchemy as s
from workers.worker_base import Worker

class ProfanityWorker(Worker):
    def __init__(self, config={}):
        
        # Define the worker's type, which will be used for self identification.
        #   Should be unique among all workers and is the same key used to define 
        #   this worker's settings in the configuration file.
        worker_type = "profanity_worker"

        # Define what this worker can be given and know how to interpret
        # given is usually either [['github_url']] or [['git_url']] (depending if your 
        # worker is exclusive to repos that are on the GitHub platform)
        given = [[]]

        # The name the housekeeper/broker use to distinguish the data model this worker can fill
        #   You will also need to name the method that does the collection for this model
        #   in the format *model name*_model() such as fake_data_model() for example
        models = ['fake_data']

        # Define the tables needed to insert, update, or delete on
        #   The Worker class will set each table you define here as an attribute
        #   so you can reference all of them like self.message_table or self.repo_table
        data_tables = ['message', 'repo']
        # For most workers you will only need the worker_history and worker_job tables
        #   from the operations schema, these tables are to log worker task histories
        operations_tables = ['worker_history', 'worker_job']

        # Run the general worker initialization
        super().__init__(worker_type, config, given, models, data_tables, operations_tables)

        # Do any additional configuration after the general initialization has been run
        self.config.update(config)

        # If you need to do some preliminary interactions with the database, these MUST go
        # in the model method. The database connection is instantiated only inside of each 
        # data collection process

        # Define data collection info
        self.tool_source = 'Fake Template Worker'
        self.tool_version = '0.0.0'
        self.data_source = 'Non-existent API'

    def fake_data_model(self, task, repo_id):
        """ This is just an example of a data collection method. All data collection 
            methods for all workers currently accept this format of parameters. If you 
            want to change these parameters, you can re-define the collect() method to 
            overwrite the Worker class' version of it (which is the method that calls
            this method).

            :param task: the task generated by the housekeeper and sent to the broker which 
            was then sent to this worker. Takes the example dict format of:
                {
                    'job_type': 'MAINTAIN', 
                    'models': ['fake_data'], 
                    'display_name': 'fake_data model for url: https://github.com/vmware/vivace',
                    'given': {
                        'git_url': 'https://github.com/vmware/vivace'
                    }
                }
            :param repo_id: the collect() method queries the repo_id given the git/github url
            and passes it along to make things easier. An int such as: 27869

        """

        # Any initial database instructions, like finding the last tuple inserted or generate the next ID value

        # Collection and insertion of data happens here

        # ...

        # Register this task as completed.
        #   This is a method of the worker class that is required to be called upon completion
        #   of any data collection model, this lets the broker know that this worker is ready
        #   for another task
        self.register_task_completion(task, repo_id, 'fake_data')

	def checkText(textIn):
		f = open('badwords.txt', 'r')
		profane = False
		for line in f:
			if line.strip().lower() in textIn.lower():
				profane = True
				break
		return profane
