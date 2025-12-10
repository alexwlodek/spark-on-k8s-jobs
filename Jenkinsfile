pipeline {
    agent {
        // Użyj pod template z label "spark-builder"
        label 'spark-builder'
    }

    environment {
        AWS_REGION       = 'eu-central-1'
        AWS_ACCOUNT_ID   = '474252044333'
        ECR_REPOSITORY   = 'spark-on-k8s-jobs-dev'
        ECR_URL          = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        // Uwaga: to jest nazwa joba w Twoim repo, nie Jenkins JOB_NAME
        JOB_NAME   = 'sample_job'
        IMAGE_TAG  = "${JOB_NAME}-${env.BUILD_NUMBER}"
        IMAGE_FULL = "${ECR_URL}/${ECR_REPOSITORY}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push with Kaniko') {
            steps {
                container(name: 'kaniko', shell: '/busybox/sh') {
                    script {
                        sh """
                            echo '--- Debug: Verifying Context ---'
                            ls -la jobs/${JOB_NAME}

                            /kaniko/executor \\
                              --context \$(pwd)/jobs/${JOB_NAME} \\
                              --dockerfile Dockerfile \\
                              --destination ${IMAGE_FULL} \\
                              --cache=true
                        """
                    }
                }
            }
        }

        stage('Submit SparkApplication') {
            steps {
                // Kontener z kubectl zdefiniowany w values.yaml (name: "kubectl")
                container('kubectl') {
                    script {
                        def sparkAppName = "${JOB_NAME}-${env.BUILD_NUMBER}"

                        // Generujemy manifest SparkApplication
                        writeFile file: 'spark-application.yaml', text: """\
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: ${sparkAppName}
  namespace: spark
spec:
  type: Python
  mode: cluster
  image: ${IMAGE_FULL}
  imagePullPolicy: Always
  mainApplicationFile: local:///opt/app/src/main.py
  sparkVersion: 3.5.0
  restartPolicy:
    type: Never
  driver:
    cores: 1
    memory: "1g"
    serviceAccount: default
    labels:
      app: ${JOB_NAME}
      build-number: "${env.BUILD_NUMBER}"
  executor:
    cores: 1
    instances: 1
    memory: "1g"
    labels:
      app: ${JOB_NAME}
      build-number: "${env.BUILD_NUMBER}"
"""

                        // Apply + podgląd statusu
                        sh """
                            echo "Applying SparkApplication ${sparkAppName} in namespace ci"
                            kubectl apply -f spark-application.yaml

                            echo "Current SparkApplications in ci:"
                            kubectl get sparkapplications -n ci

                            echo "Describe new SparkApplication:"
                            kubectl describe sparkapplication ${sparkAppName} -n ci
                        """

                        // Prosty wait na zakończenie joba (bez {1..60}, żeby na pewno działało w /bin/sh)
                        sh """
                            echo "Waiting for SparkApplication ${sparkAppName} to finish..."
                            i=0
                            while [ \$i -lt 60 ]; do
                              status=\$(kubectl get sparkapplication ${sparkAppName} -n ci -o jsonpath='{.status.applicationState.state}' 2>/dev/null || echo "UNKNOWN")
                              echo "Current state: \$status"
                              if [ "\$status" = "COMPLETED" ] || [ "\$status" = "FAILED" ]; then
                                break
                              fi
                              i=\$((i+1))
                              sleep 10
                            done

                            echo "Final SparkApplication status:"
                            kubectl get sparkapplication ${sparkAppName} -n ci -o yaml
                        """
                    }
                }
            }
        }
    }
}
