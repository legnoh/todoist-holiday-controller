import jpholiday,os,yaml
from datetime import datetime
from pytodoist import todoist

def get_task_from_project_by_id(project_tasks, task_id):
    for project_task in tasks:
        if project_task.id == task_id:
            return project_task
    return None

td = todoist.login_with_api_token(os.environ['TODOIST_API_KEY'])
today = datetime.now()

if today.weekday() >= 5:
    print("today is Sat/Sun")
    td.enable_vacation()
else:
    print("today is workday")
    td.disable_vacation()

if not jpholiday.is_holiday(today):
    print("today is a holiday")
    td.enable_vacation()

    with open('config.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    for target_project in config['skip_tasks']:
        project = td.get_project(target_project['project_name'])
        tasks = project.get_uncompleted_tasks()

        for task_id in target_project['tasks']:
            task = get_task_from_project_by_id(project,task_id)
            if task != None:
                task.complete()
                print("{task_id}: completed".format(task_id=task_id))
