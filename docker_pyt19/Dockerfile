FROM nvcr.io/nvidia/pytorch:20.02-py3
WORKDIR /opt/pytorch
COPY Anaconda3-2021.05-Linux-x86_64.sh .
RUN apt -y update && apt -y install wget curl vim libgcrypt20 coreutils libgl1-mesa-glx
RUN chmod ouga+xw ./Anaconda3-2021.05-Linux-x86_64.sh
RUN bash ./Anaconda3-2021.05-Linux-x86_64.sh -b -p ./conda
ENV PATH /opt/pytorch/conda/bin:$PATH
RUN conda update -n base -c defaults conda 

RUN conda create -n pvcnn_pyt19 python=3.8 
RUN source activate pvcnn_pyt19 
RUN conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
RUN pip install pillow
RUN pip install cython
RUN pip install matplotlib
RUN pip install tensorboard
RUN pip install tensorboardX
RUN pip install tfrecord  
RUN pip install loguru tabulate comet_ml einops alive_progress calmsize
RUN echo `which python`
RUN echo `python -c "import torch;print(torch.__version__)" ` 
RUN echo `python -c "import torch;print(torch.__file__)" ` 
