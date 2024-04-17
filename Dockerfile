FROM centos:centos7
LABEL author="jy wu <jywu2017@pku.edu.cn>" \
	describe="SComet base image"

RUN mkdir -p /home/wjy/SComet \
	&& yum -y install centos-release-scl epel-release \
	&& yum -y install libevent libevent-devel libtool \
	&& yum -y install zlib zlib-devel bzip2 bzip2-devel gperftools gperftools-devel libdb-cxx-devel libaio-devel \
	&& yum -y install vim wget git zip unzip sudo numactl autoconf  automake make python3 python-pip memcached tcl net-tools \
	&& yum -y install java-1.8.0-openjdk-devel.x86_64 \
	&& yum -y install devtoolset-9-gcc* \
	&& mv /usr/bin/gcc /usr/bin/gcc-4.8.5 \
	&& ln -s /opt/rh/devtoolset-9/root/bin/gcc /usr/bin/gcc \
	&& ln -s /opt/rh/devtoolset-9/root/bin/g++ /usr/bin/g++ \
	&& ln -s /opt/rh/devtoolset-9/root/bin/gfortran /usr/bin/gfortran \
	&& python -m pip install --upgrade pip==10.0.0 && python -m pip install --upgrade pip==18.0 && python -m pip install --upgrade pip==20.3.4 \
	&& python -m pip install numpy && python -m pip install scipy && python -m pip install redis


ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64/ \
	JAVA_HOME=/usr/lib/jvm/java
ENV JRE_HOME=$JAVA_HOME/jre \
	CLASS_PATH=:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib \
	PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin 

WORKDIR /home/wjy
COPY jemalloc jemalloc

RUN cd jemalloc && ./autogen.sh && make && make install \
	&& cd /usr/local/src/ \
	&& wget -t 0 -c http://downloads.sourceforge.net/project/pcre/pcre/8.35/pcre-8.35.tar.gz \
	&& wget -t 0 -c https://nginx.org/download/nginx-1.24.0.tar.gz \
	&& wget -t 0 -c https://www.openssl.org/source/openssl-1.1.1q.tar.gz --no-check-certificate \
	&& tar zxvf pcre-8.35.tar.gz && cd pcre-8.35 && ./configure && make && make install && cd .. \
	&& tar zxvf openssl-1.1.1q.tar.gz &&  cd openssl-1.1.1q && ./config && make && make install && cd .. \
	&& ln -s /usr/local/bin/openssl /usr/bin/openssl \
	&& tar zxvf nginx-1.24.0.tar.gz && cd nginx-1.24.0 \
	&& ./configure --with-http_stub_status_module --with-http_ssl_module --with-pcre=/usr/local/src/pcre-8.35 --with-openssl=/usr/local/src/openssl-1.1.1q \
	&& sed -i '3s/-Werror -g /-g/' objs/Makefile &&make && make install 

	
	




