import argparse
import scripts

if __name__ == '__main__':
    task = argparse.ArgumentParser()
    task.add_argument('name')
    task.add_argument('--repository')
    task.add_argument('--circle-token')
    task = task.parse_args()
    
    if task.name == 'latest_workflow_status':
        succes = scripts.latest_workflow_status(task.repository, task.circle_token)
        assert succes, 'latest workflow was not successful'
