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
        JOB_NAME         = "sample_job"
        IMAGE_TAG        = "${JOB_NAME}-${env.BUILD_NUMBER}"
        IMAGE_FULL       = "${ECR_URL}/${ECR_REPOSITORY}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

stage('ECR login (IRSA)') {
  steps {
    container('awscli') {
      sh """
        mkdir -p /kaniko/.docker
        PASS=$(aws ecr get-login-password --region ${AWS_REGION})
        AUTH=$(printf "AWS:%s" "$PASS" | base64)
        cat > /kaniko/.docker/config.json <<EOF
        {
          "auths": {
            "${ECR_URL}": {
              "username": "AWS",
              "password": "$PASS",
              "auth": "$AUTH"
            }
          }
        }
        EOF
      """
    }
  }
}

stage('Build and Push with Kaniko') {
  steps {
    container('kaniko') {
      sh """
        /kaniko/executor \
          --context \$(pwd)/jobs/${JOB_NAME} \
          --dockerfile Dockerfile \
          --destination ${IMAGE_FULL} \
          --cache=true \
          --docker-config=/kaniko/.docker
      """
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