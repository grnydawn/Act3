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

        HOST >> docker pull grnydawn/act3_dev:v2


2. Create "act3dev" container with a proper branch name found on this Act3 Github repo. 

	```HOST >> docker create --name act3dev -h act3dev -it -p 8080:8080 -p 9090:9090 grnydawn/act3_dev:v2  [branch]```

	NOTE: This command is also implemented in Act3/bin/create_dev.sh.


2. Start the "act3dev" container. 

	```HOST >> docker start -ai act3dev```

	NOTE: This command is also implemented in Act3/bin/start_dev.sh.
	
	
3. Launch Act3 Components in the container.

	```CONTAINER >> cd /root/Act3/bin```
	
	```CONTAINER >> ./launch.sh name web```


4. Visit Act3 Home page using browser

    4.1 Find IP address to access
    
        LINUX HOST >> ifconfig docker0 | grep "inet addr"
        
        WINDOWS HOST >> docker-machine ip default
        
    4.2 Access Act3 Home page
   
        BROWSER >> Open [IP address found]:8080


5. Create a terminal to work on files in CONTAINER
    
        HOST >> docker exec -it act3dev bash


6. Modify files and push to Github Act3 repo.

        CONTAINER >> git status ; # for checking the status of the repo and the name of a working branch
        
        CONTAINER >> git add .  ; # for staging files before commit
        
        CONTAINER >> git commit -m "commit message..." ; for commiting changes
        
        CONTAINER >> git push origin [branchname] ; push changes to Github Act3 repo.
        

7. Check useful docker commands in /root/Act3/docker/docker.notes
