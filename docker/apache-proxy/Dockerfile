# docker/apache-proxy/Dockerfile

FROM httpd:2.4

# Enable necessary Apache modules
RUN sed -i '/#LoadModule proxy_module modules\/mod_proxy.so/s/^#//g' /usr/local/apache2/conf/httpd.conf
RUN sed -i '/#LoadModule proxy_http_module modules\/mod_proxy_http.so/s/^#//g' /usr/local/apache2/conf/httpd.conf
RUN sed -i '/#LoadModule headers_module modules\/mod_headers.so/s/^#//g' /usr/local/apache2/conf/httpd.conf

# Copy the custom proxy configuration to the extra directory
COPY proxy.conf /usr/local/apache2/conf/extra/proxy.conf

# Include the custom proxy configuration in the main httpd.conf
RUN echo "Include conf/extra/proxy.conf" >> /usr/local/apache2/conf/httpd.conf

# Expose the default HTTP port
EXPOSE 80
