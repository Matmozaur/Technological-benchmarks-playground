# Use a base image with Java JDK
FROM openjdk:11-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Scala source code
COPY app/Main.scala /app

# Install Scala
RUN apt-get update && apt-get install -y scala

# Compile and run the Scala application
CMD ["scala", "-nocompdaemon", "Main.scala"]