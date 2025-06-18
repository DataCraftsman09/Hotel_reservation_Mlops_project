pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "focus-vim-461708-m6"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin" 
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

        stage("Building and Pushing Docker Image to GCR"){
            steps{
                withCredentials([file(credentialsId : 'GCP_Key',variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR...............'
                        sh ''' 
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quite

                        docker build -t gcr.io/${GCP_PROJECT}/ml-Projects_HMRS .

                        docker push gcr.io/${GCP_PROJECT}/ml-Projects_HMRS 
                        '''
                    }
                }
            }
        }
    }
}