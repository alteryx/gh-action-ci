import argparse
import scripts

if __name__ == '__main__':
    task = argparse.ArgumentParser()
    task.add_argument('name')
    task.add_argument('repository')
    task.add_argument('--circle-token')
    task = task.parse_args()
    
    if task.name == 'latest_workflow_status':
        workflow = scripts.latest_workflow(task.repository, task.circle_token)
        success = workflow.status.eq('success').all()
        assert success, 'latest workflow was not successful'

    else:
        raise ValueError('task not supported')
