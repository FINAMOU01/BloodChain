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
                    def changedFiles = sh(
                        script: "git diff --name-only HEAD~1 HEAD || echo 'services/'",
                        returnStdout: true
                    ).trim()

                    echo "Changed files:\n${changedFiles}"

                    env.BUILD_USER_MGMT     = changedFiles.contains('services/user-management')          ? 'true' : 'false'
                    env.BUILD_DONOR         = changedFiles.contains('services/donor-service')             ? 'true' : 'false'
                    env.BUILD_HOSPITAL      = changedFiles.contains('services/hospital-service')          ? 'true' : 'false'
                    env.BUILD_TRACKING      = changedFiles.contains('services/blood-tracking-service')    ? 'true' : 'false'
                    env.BUILD_NOTIFICATIONS = changedFiles.contains('services/notifications-service')     ? 'true' : 'false'
                    env.BUILD_REWARDS       = changedFiles.contains('services/rewards-service')           ? 'true' : 'false'
                    env.BUILD_LOCATION      = changedFiles.contains('services/location-service')          ? 'true' : 'false'
                    env.BUILD_BLOCKCHAIN    = changedFiles.contains('services/blockchain-gateway')        ? 'true' : 'false'
                    env.BUILD_WAREHOUSE     = changedFiles.contains('services/data-warehouse')            ? 'true' : 'false'
                    env.BUILD_FRONTEND      = (
                        changedFiles.contains('services/frontend-service') ||
                        changedFiles.contains('templates/') ||
                        changedFiles.contains('static/')
                    ) ? 'true' : 'false'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🐳 Building Docker images for changed services...'
                script {
                    def services = [
                        [name: 'user-management',        path: 'services/user-management',         dockerfile: 'services/user-management/Dockerfile',        build: env.BUILD_USER_MGMT],
                        [name: 'donor-service',          path: 'services/donor-service',            dockerfile: 'services/donor-service/Dockerfile',           build: env.BUILD_DONOR],
                        [name: 'hospital-service',       path: 'services/hospital-service',         dockerfile: 'services/hospital-service/Dockerfile',        build: env.BUILD_HOSPITAL],
                        [name: 'blood-tracking-service', path: 'services/blood-tracking-service',   dockerfile: 'services/blood-tracking-service/Dockerfile',  build: env.BUILD_TRACKING],
                        [name: 'notifications-service',  path: 'services/notifications-service',    dockerfile: 'services/notifications-service/Dockerfile',   build: env.BUILD_NOTIFICATIONS],
                        [name: 'rewards-service',        path: 'services/rewards-service',          dockerfile: 'services/rewards-service/Dockerfile',         build: env.BUILD_REWARDS],
                        [name: 'location-service',       path: 'services/location-service',         dockerfile: 'services/location-service/Dockerfile',        build: env.BUILD_LOCATION],
                        [name: 'blockchain-gateway',     path: 'services/blockchain-gateway',       dockerfile: 'services/blockchain-gateway/Dockerfile',      build: env.BUILD_BLOCKCHAIN],
                        [name: 'data-warehouse',         path: 'services/data-warehouse',           dockerfile: 'services/data-warehouse/Dockerfile',          build: env.BUILD_WAREHOUSE],
                        [name: 'frontend-service',       path: '.',                                 dockerfile: 'services/frontend-service/Dockerfile',        build: env.BUILD_FRONTEND],
                    ]

                    services.each { svc ->
                        if (svc.build == 'true') {
                            echo "Building ${svc.name}..."
                            sh """
                                docker build \
                                  -f ${svc.dockerfile} \
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
                    def testServices = [
                        [name: 'donor-service',          build: env.BUILD_DONOR],
                        [name: 'hospital-service',       build: env.BUILD_HOSPITAL],
                        [name: 'blood-tracking-service', build: env.BUILD_TRACKING],
                        [name: 'notifications-service',  build: env.BUILD_NOTIFICATIONS],
                        [name: 'user-management',        build: env.BUILD_USER_MGMT],
                    ]

                    testServices.each { svc ->
                        if (svc.build == 'true') {
                            echo "Testing ${svc.name}..."
                            sh """
                                docker run --rm \
                                  --entrypoint python \
                                  -e DJANGO_SETTINGS_MODULE=config.settings_test \
                                  -e SECRET_KEY=test-secret-key-12345 \
                                  -e DEBUG=True \
                                  ${DOCKER_HUB_USER}/${IMAGE_PREFIX}-${svc.name}:latest \
                                  manage.py test --verbosity=2
                            """
                        }
                    }
                    echo '✅ All tests passed.'
                }
            }
        }

        stage('Push to Docker Hub') {
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
                            'blockchain-gateway', 'data-warehouse',
                            'frontend-service'
                        ]

                        services.each { name ->
                            def image = "${DOCKER_HUB_USER}/${IMAGE_PREFIX}-${name}"
                            def commitTag = "${image}:${env.GIT_COMMIT}"
                            def latestTag = "${image}:latest"

                            def imageExists = sh(
                                script: "docker image inspect ${latestTag} > /dev/null 2>&1",
                                returnStatus: true
                            ) == 0

                            if (imageExists) {
                                echo "Pushing ${name} (local image found)..."
                                sh """
                                    docker tag ${latestTag} ${commitTag}
                                    docker push ${commitTag}
                                    docker push ${latestTag}
                                """
                            } else {
                                echo "WARNING: No local image found for ${name} (${latestTag}) — skipping push."
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy to K3s') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deploying to K3s cluster...'
                script {
                    try {
                        withCredentials([
                            sshUserPrivateKey(
                                credentialsId: 'vps-ssh-key',
                                keyFileVariable: 'SSH_KEY'
                            )
                        ]) {
                            sh '''
                                set +e
                                echo "=== Checking current deployments ==="
                                ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@$K3S_SERVER 'kubectl get deployments -n bloodchain'
                                echo "EXIT CODE: $?"

                                echo "=== Applying manifests ==="
                                ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@$K3S_SERVER 'kubectl apply -f /opt/bloodchain/infra/k3s/manifests/ -n bloodchain -v=8'
                                echo "EXIT CODE: $?"

                                echo "=== Checking rollout status ==="
                                ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@$K3S_SERVER 'kubectl rollout status deployment -n bloodchain --timeout=120s'
                                echo "EXIT CODE: $?"
                            '''
                        }
                    } catch (err) {
                        echo "⚠️ Deploy stage failed but continuing: ${err}"
                    }
                }
                echo '✅ Deployment complete (or skipped).'
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
