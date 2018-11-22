pipeline {
    agent any 
    stages {
        stage('Stage 1 - build') {
            steps {
                echo "starting build step in job ${env.JOB_NAME}"
                echo "BUILD_DISPLAY_NAME: ${env.BUILD_DISPLAY_NAME}"
                echo "BUILD_ID: ${env.BUILD_ID}"                
                echo "WORKSPACE: ${env.WORKSPACE}"      
                echo "JENKINS_URLE: ${env.JENKINS_URL}" 
                echo "EXECUTOR_NUMBER: ${env.EXECUTOR_NUMBER}"  
                sh 'printenv'
            }
        }
    }
}
