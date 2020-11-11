pipeline { 
    agent any 
    stages {
        stage('Checkout') { 
            steps { 
                checkout scm
            }
        }
        stage('Test'){
            steps {
                sh 'virtualenv env -p python3'
		sh '. env/bin/activate'
                sh 'env/bin/pip install -r requirements.txt'
            }
        }
        stage('Deploy') {
            steps {
                sh 'python manage.py runserver'
            }
        }
    }
}
