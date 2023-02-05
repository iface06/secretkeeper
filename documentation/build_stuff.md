# Build within Python

## Jenkins as Docker for local enviroment
`docker run -p 8080:8080 -p 50000:50000 --restart=on-failure -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11`

[Jenkins Docker Documenation](https://github.com/jenkinsci/docker/blob/master/README.md)

## Build a Package
`python setup.py sdist`
