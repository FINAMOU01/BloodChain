pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'finamou'
        IMAGE_PREFIX     = 'bloodchain'
        K3S_SERVER       = '207.180.220.145'
        GIT_BRANCH_NAME  = "${env.BRANCH_NAME}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Cloning repository...'
                checkout scm
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        stage('Detect Changed Services') {
            steps {
                echo '🔍 Detecting which services changed...'
                script {
                    // Get list of changed files in this push
                    def changedFiles = sh(
                        script: "git diff --name-only HEAD~1 HEAD || echo 'services/'",
                        returnStdout: true
                    ).trim()

                    echo "Changed files:\n${changedFiles}"

                    // Detect which services are affected
                    env.BUILD_USER_MGMT     = changedFiles.contains('services/user-management')     ? 'true' : 'false'
                    env.BUILD_DONOR         = changedFiles.contains('services/donor-service')        ? 'true' : 'false'
                    env.BUILD_HOSPITAL      = changedFiles.contains('services/hospital-service')     ? 'true' : 'false'
                    env.BUILD_TRACKING      = changedFiles.contains('services/blood-tracking-service') ? 'true' : 'false'
                    env.BUILD_NOTIFICATIONS = changedFiles.contains('services/notifications-service') ? 'true' : 'false'
                    env.BUILD_REWARDS       = changedFiles.contains('services/rewards-service')      ? 'true' : 'false'
                    env.BUILD_LOCATION      = changedFiles.contains('services/location-service')     ? 'true' : 'false'
                    env.BUILD_BLOCKCHAIN    = changedFiles.contains('services/blockchain-gateway')   ? 'true' : 'false'
                    env.BUILD_WAREHOUSE     = changedFiles.contains('services/data-warehouse')       ? 'true' : 'false'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🐳 Building Docker images for changed services...'
                script {
                    def services = [
                        [name: 'user-management',       path: 'services/user-management',        build: env.BUILD_USER_MGMT],
                        [name: 'donor-service',         path: 'services/donor-service',           build: env.BUILD_DONOR],
                        [name: 'hospital-service',      path: 'services/hospital-service',        build: env.BUILD_HOSPITAL],
                        [name: 'blood-tracking-service',path: 'services/blood-tracking-service',  build: env.BUILD_TRACKING],
                        [name: 'notifications-service', path: 'services/notifications-service',   build: env.BUILD_NOTIFICATIONS],
                        [name: 'rewards-service',       path: 'services/rewards-service',         build: env.BUILD_REWARDS],
                        [name: 'location-service',      path: 'services/location-service',        build: env.BUILD_LOCATION],
                        [name: 'blockchain-gateway',    path: 'services/blockchain-gateway',      build: env.BUILD_BLOCKCHAIN],
                        [name: 'data-warehouse',        path: 'services/data-warehouse',          build: env.BUILD_WAREHOUSE],
                    ]

                    services.each { svc ->
                        if (svc.build == 'true') {
                            echo "Building ${svc.name}..."
                            sh """
                                docker build \
                                  -t ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-${svc.name}:${env.GIT_COMMIT} \
                                  -t ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-${svc.name}:latest \
                                  ${svc.path}
                            """
                        } else {
                            echo "Skipping ${svc.name} — no changes detected."
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests for changed services...'
                script {
                    if (env.BUILD_DONOR == 'true') {
                        sh '''
                            docker run --rm \
                              ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-donor-service:latest \
                              python manage.py test --verbosity=2
                        '''
                    }
                    if (env.BUILD_HOSPITAL == 'true') {
                        sh '''
                            docker run --rm \
                              ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-hospital-service:latest \
                              python manage.py test --verbosity=2
                        '''
                    }
                    if (env.BUILD_TRACKING == 'true') {
                        sh '''
                            docker run --rm \
                              ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-blood-tracking-service:latest \
                              python manage.py test --verbosity=2
                        '''
                    }
                    echo '✅ All tests passed.'
                }
            }
        }

        stage('Push to Docker Hub') {
            // Only push when merging into dev or main
            when {
                anyOf {
                    branch 'dev'
                    branch 'main'
                }
            }
            steps {
                echo '📤 Pushing images to Docker Hub...'
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub-credentials',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'

                        def services = [
                            'user-management', 'donor-service', 'hospital-service',
                            'blood-tracking-service', 'notifications-service',
                            'rewards-service', 'location-service',
                            'blockchain-gateway', 'data-warehouse'
                        ]

                        services.each { name ->
                            sh """
                                docker push ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-${name}:${env.GIT_COMMIT}
                                docker push ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-${name}:latest
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy to K3s') {
            // Only deploy when merging into main
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deploying to K3s cluster...'
                script {
                    withCredentials([
                        sshUserPrivateKey(
                            credentialsId: 'vps-ssh-key',
                            keyFileVariable: 'SSH_KEY'
                        )
                    ]) {
                        sh """
                            ssh -i ${SSH_KEY} \
                                -o StrictHostKeyChecking=no \
                                root@${K3S_SERVER} \
                                'kubectl apply -f /opt/bloodchain/infra/k3s/manifests/ \
                                 && kubectl rollout status deployment \
                                    -n bloodchain --timeout=120s'
                        """
                    }
                }
                echo '✅ Deployment complete.'
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline passed successfully!'
        }
        failure {
            echo '❌ Pipeline failed — check the logs above.'
        }
        always {
            echo '🧹 Cleaning up...'
            sh 'docker system prune -f || true'
        }
    }
}