FROM python:3.11-slim

# Create working directory
WORKDIR /usr/src/lanelet2

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy files
COPY . /usr/src/lanelet2

# Install pip packages
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Install conan dependencies
RUN conan profile detect --force
RUN conan install . --build=missing -o shared=True -c tools.cmake.cmaketoolchain:generator=Ninja

# Install package
RUN pip install --no-cache .

CMD ["/bin/bash"]