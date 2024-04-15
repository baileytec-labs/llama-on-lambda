# Define function directory
ARG FUNCTION_DIR="/function"

FROM --platform=linux/x86-64 ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  python3 \
  python3-pip \
  python3-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY main.py ${FUNCTION_DIR}
COPY modelfile.bin /opt/modelfile.bin
# Install the runtime interface client
RUN pip3 install \
       # --target ${FUNCTION_DIR} \
        awslambdaric

# Install the function's dependencies using file requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${FUNCTION_DIR}"

#COPY ggml-alpaca-7b-q4.bin /opt/
#COPY ggml-alpaca-7b-q4.bin /opt/
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
ENTRYPOINT [ "/usr/bin/python3", "-m", "awslambdaric" ]
CMD [ "main.handler" ]
