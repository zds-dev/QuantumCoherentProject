from quantuminspire.credentials import enable_account
from quantuminspire.qiskit import QI

def connect_qi(token_file, project_name='Qiskit API'):
    with open(token_file, 'r') as f:
        token = f.read().strip()
    enable_account(token)
    QI.set_authentication()
    QI.set_project_name(project_name)


