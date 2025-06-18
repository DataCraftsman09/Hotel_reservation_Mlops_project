pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }
    stages{
        stage("Cloning GitHub repo to Jenkins"){
            steps{
                script{
                    echo 'Cloning GitHub repo to Jenkins.................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/DataCraftsman09/MLOPS_PROJECTS.git']])
                }
            }
        }

        stage("Setting up our Virtual Environment and Istalling dependencies in Jenkins"){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Istalling dependencies in Jenkins.................'
                    sh ''' 
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}