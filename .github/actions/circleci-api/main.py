import api
import argparse

if __name__ == '__main__':
    task = argparse.ArgumentParser()
    task.add_argument('name')
    task.add_argument('repository')
    task.add_argument('--circle-token')
    task = task.parse_args()
    
    if task.name == 'latest_workflow_status':
        workflow = api.latest_workflow(task.repository, task.circle_token)

        line = '-' * 25
        print('\n', line, ' Latest Status on CircleCI ', line, '\n')
        keys = ['workflow_id', 'workflow_name', 'job_name', 'status']
        print(workflow[keys].to_string(index=False), '\n')

        success = workflow.status.eq('success').all()
        assert success, 'latest workflow was not successful'

    else:
        raise ValueError('task not supported')
