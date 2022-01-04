# build docker: 
docker build -t nvcr.io/pyt19:0 .  

# launch docker: 
docker run --gpus all -v /home/xiaohui/:/home/xiaohui/ -it nvcr.io/pyt19:0 bash 
