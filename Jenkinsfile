pipeline {
    agent { label 'jenkins' } // albo inny node label

    environment {
        AWS_REGION       = 'eu-central-1'
        AWS_ACCOUNT_ID   = '474252044333'
        ECR_REPOSITORY   = 'spark-on-k8s-jobs-dev'
        ECR_URL          = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        JOB_NAME         = "sample-job"
        IMAGE_TAG        = "${JOB_NAME}-${env.BUILD_NUMBER}"
        IMAGE_FULL       = "${ECR_URL}/${ECR_REPOSITORY}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Docker build') {
            steps {
                dir("jobs/${JOB_NAME}") {
                    sh "docker build -t ${IMAGE_FULL} ."
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh """
                  aws ecr get-login-password --region ${AWS_REGION} \
                    | docker login --username AWS --password-stdin ${ECR_URL}
                """
            }
        }

        stage('Push image') {
            steps {
                sh "docker push ${IMAGE_FULL}"
            }
        }

        stage('Run Spark job (optional)') {
            steps {
                sh """
                  spark-submit \\
                    --master k8s://https://<TWÓJ_EKS_API> \\
                    --deploy-mode cluster \\
                    --conf spark.kubernetes.container.image=${IMAGE_FULL} \\
                    --conf spark.kubernetes.namespace=default \\
                    local:///opt/app/src/main.py
                """
            }
        }
    }
}
