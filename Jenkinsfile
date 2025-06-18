pipeline{
    agent any
    stages{
        stage("Cloning GitHub repo to Jenkins"){
            steps{
                script{
                    echo 'Cloning GitHub repo to Jenkins.................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/DataCraftsman09/MLOPS_PROJECTS.git']])
                }
            }
        }
    }
}