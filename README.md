# SDN_Django_framework_for_implementation_network_service_configuration_application
This is a first try to approach a simple NMS using Django as Backedn Framework.
The DockerFile is just for testing purposes. The final app will be deployed on Docker and then on Kubernetes Cluster. The Container infrastructure will be decided.... 

root@TEST:/home/iasonas# docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED        STATUS                    PORTS     NAMES
4d83ba5a90a6   mydjangoapp   "python3 manage.py r…"   17 hours ago   Exited (0) 17 hours ago             elated_fermat
root@TEST:/home/iasonas#
root@TEST:/home/iasonas# docker run -p 8000:8000 mydjangoapp

Build the image docker build -t djangoapp .
Run the container docker run -p 80:8000 djangoapp


***



***

In order for this app to work connection with devices in needed from local machine and also from containers. Make sure to connect devices to your local PC for testing purposes

***
![Topology](https://github.com/Iasimo92/SDN_Django_framework_for_implementation_network_service_configuration_application/blob/main/connection.png)

***

GUI first page

***

![GUI](https://github.com/Iasimo92/SDN_Django_framework_for_implementation_network_service_configuration_application/blob/main/Screenshot%202023-07-24%20123620.png)

***

GUI supplementary pages

***
![GUI](https://github.com/Iasimo92/SDN_Django_framework_for_implementation_network_service_configuration_application/blob/main/controller.png)
***

![GUI](https://github.com/Iasimo92/SDN_Django_framework_for_implementation_network_service_configuration_application/blob/main/statistics.png)

***

