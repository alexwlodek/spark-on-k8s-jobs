pipeline {
    agent {
        // Points to the pod template defined in values.yaml
        label 'spark-builder' 
    }

    environment {
        AWS_REGION       = 'eu-central-1'
        AWS_ACCOUNT_ID   = '474252044333'
        ECR_REPOSITORY   = 'spark-on-k8s-jobs-dev'
        ECR_URL          = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        JOB_NAME         = ""
        IMAGE_TAG        = "${JOB_NAME}-${env.BUILD_NUMBER}"
        IMAGE_FULL       = "${ECR_URL}/${ECR_REPOSITORY}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push with Kaniko') {
            steps {
                // CRITICAL: Switch to the kaniko container defined in the pod template
                container(name: 'kaniko', shell: '/busybox/sh') {
                    script {
                        // Kaniko handles ECR auth automatically via IRSA (IAM Role)
                        // No need for 'docker login' or 'aws ecr get-login'
                        sh """
                        /kaniko/executor \
                            --context $(pwd)/jobs/${JOB_NAME} \
                            --dockerfile $(pwd)/jobs/${JOB_NAME}/Dockerfile \
                            --destination ${IMAGE_FULL} \
                            --cache=true
                        """
                    }
                }
            }
        }

        stage('Run Spark job') {
            steps {
                // Runs in the default 'jnlp' container which has kubectl/spark-submit tools
                sh """
                  spark-submit \
                    --master k8s://https://C9CF0A3CA8201DB2F8052724BBFA208C.yl4.eu-central-1.eks.amazonaws.com \
                    --deploy-mode cluster \
                    --conf spark.kubernetes.container.image=${IMAGE_FULL} \
                    --conf spark.kubernetes.namespace=ci \
                    local:///opt/app/src/main.py
                """
            }
        }
    }
}