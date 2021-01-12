FROM nvidia/cuda:11.1-cudnn8-runtime-ubuntu18.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"


RUN apt update \
    && apt install -y htop gcc python3.7-dev vim wget libevent-dev libcairo2-dev pkg-config protobuf-compiler python-pil python-lxml  libgl1-mesa-glx

# RUN apt-get install -y protobuf-compiler python-pil python-lxml    

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  \
    && mkdir -p root/. conda \
    && sh Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN conda create -y -n ml python=3.7

# COPY /models var_data/ 
# ADD ./models.tar.xz /var_data/

#directory to copy the code
RUN mkdir -p /var_data    
# COPY /models var_data/ 

ADD ./models.tar.xz /var_data/

#directory for mounting having images and for storing the training data
RUN mkdir -p /var_data2

# COPY . var_data/              
RUN /bin/bash -c "cd /var_data/models/research \
    && source activate ml \
    && pip install -r requirements.txt \
    && protoc object_detection/protos/*.proto --python_out=."

# WORKDIR /var_data/models/research
# RUN protoc object_detection/protos/*.proto --python_out=.

    # && cd  /var_data/models/research \
    # && python setup.py build \
    # && python setup.py install \


# RUN python /var_data/models/research/object_detection/operations.py

CMD  /bin/bash -c "source activate ml \
&& cd  /var_data/models/research \
&& python setup.py install \
&& cd  /var_data/models/research/object_detection \
&& python operations.py"
# ENTRYPOINT [source activate ml && python]

    # && protoc object_detection/protos/*.proto --python_out=. 
# RUN  cd /codes && tar -xz models.tar.xz && rm models.tar.xz



# && cd  /var_data/models/research \
# && python setup.py install \