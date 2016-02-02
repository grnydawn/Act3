Act3: Automatic Performance Optimizer
==============================


Overview
--------

* T.B.D

Dependencies
------------

* Docker (>=1.9)



Instructions for Development
------------------

1. Download Act3 Development Image from Docker Hub.

        HOST >> docker pull grnydawn/act3_dev:v1


2. Run the image with a proper branch name on this Act3 Github repo. 

	```HOST >> docker run -it -P grnydawn/act3_dev:v1 [branch]```


3. Launch Act3 Components

	```CONTAINER >> cd /root/Act3/bin```
	
	```CONTAINER >> ./launch.sh name web```


4. Visit Act3 Home page using browser

    4.1 Find IP address to access
    
        LINUX HOST >> ifconfig docker0 | grep "inet addr"
        
        WINDOWS HOST >> docker-machine ls or docker-machine ip [virtualmachinename]
        
    4.2 Access Act3 Home page
   
        BROWSER >> Open [IP address found]:8080


5. Create a terminal to work on files in CONTAINER

    5.1 Find Container ID
    
	```HOST >> docker ps```
	
    5.2 Create a terminal
    
        HOST >> docker exec -it [Container ID] bash


6. Modify files and push to Github Act3 repo.

        CONTAINER >> git status ; # for checking the status of the repo and the name of a working branch
        
        CONTAINER >> git add .  ; # for staging files before commit
        
        CONTAINER >> git commit -m "commit message..." ; for commiting changes
        
        CONTAINER >> git push origin [branchname] ; push changes to Github Act3 repo.
        

7. Check useful docker commands in /root/Act3/docker/docker.notes
